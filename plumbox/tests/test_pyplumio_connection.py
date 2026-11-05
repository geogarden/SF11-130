"""Connection URLs are passed to the actual 0.7.6 entry point; no boiler required."""
import asyncio
from importlib.metadata import version
from types import SimpleNamespace
import pytest
import pyplumio
from app.config import AppConfig
from app.plum_service import PlumService, TransportPhaseError


@pytest.mark.parametrize('kind,host,path,expected',[
 ('tcp','192.168.1.20','/dev/ttyUSB0','socket://192.168.1.20:8899'),
 ('tcp','::1','/dev/ttyUSB0','socket://[::1]:8899'),
 ('serial','192.168.1.20','/dev/ttyUSB2','/dev/ttyUSB2'),
])
def test_connection_uses_serial_for_url(monkeypatch,kind,host,path,expected):
 assert version('pyplumio')=='0.7.6'
 real_factory=pyplumio.serial_for_url
 calls=[]
 class Connection:
  async def __aenter__(self):raise OSError('No physical connection in test')
  async def close(self):pass
 def factory(url,**kwargs):
  connection=real_factory(url,**kwargs)
  calls.append((connection.url,dict(connection.options),kwargs))
  return Connection()
 monkeypatch.setattr(pyplumio,'serial_for_url',factory)
 config=AppConfig();config.connection.type=kind;config.connection.host=host;config.connection.port=8899;config.connection.serial_device=path;config.connection.baudrate=115200
 service=PlumService(config,SimpleNamespace())
 with pytest.raises(TransportPhaseError):asyncio.run(service._connection_session())
 assert calls[0][0]==expected
 assert calls[0][2]['reconnect_on_failure'] is False
 if kind=='serial':assert calls[0][1]['baudrate']==115200
