import enum
from . import _projector
import serial

class ESCVP21_STATE(enum.Enum):
  STATE_STANDBY_NETWORK_OFF = 0
  STATE_LASER_ON = 1
  STATE_WARMUP = 2
  STATE_COOL_DOWN = 3
  STATE_STANDBY_NETWORK_ON = 4

  STATE_ABNORMALITY_STANDBY = 5
  STATE_AV_STANDBY = 6

class ESCVP21(serial.Serial):
  def __init__(self, *args, **kwargs):
      self._port_handle = None
      self._overlapped_read = None
      self._overlapped_write = None
      super(ESCVP21, self).__init__(*args, **kwargs)

  def curr_state(self):


  def power_on(self):
    pass

  def power_off(self):
    pass