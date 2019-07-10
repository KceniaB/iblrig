import logging
import time

import iblrig.alyx as alyx
import task_settings
import user_settings
from iblrig.frame2TTL import Frame2TTL
from session_params import SessionParamHandler

log = logging.getLogger('iblrig')
# import iblrig.fake_user_settings as user_settings  # PyBpod creates this file on run.
# task_settings.IBLRIG_FOLDER = Path(__file__).parent.parent.parent

sph = SessionParamHandler(task_settings, user_settings)
f2ttl = Frame2TTL(sph.COM['FRAME2TTL'])

sph.start_screen_color()
sph.set_screen(rgb=[255, 255, 255])
time.sleep(1)
f2ttl.measure_white()
sph.set_screen(rgb=[0, 0, 0])
time.sleep(1)
f2ttl.measure_black()
resp = f2ttl.calc_recomend_thresholds()
if resp != -1:
    f2ttl.set_recommendations()

    patch = {'F2TTL_COM': f2ttl.serial_port,
             'F2TTL_DARK_THRESH': f2ttl.recomend_dark,
             'F2TTL_LIGHT_THRESH': f2ttl.recomend_light}

    alyx.update_board_params(sph.PYBPOD_BOARD, patch)

sph.stop_screen_color()

print('Done')
