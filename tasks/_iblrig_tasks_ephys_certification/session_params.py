#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Niccolò Bonacchi
# @Date: Thursday, June 6th 2019, 11:42:40 am
import logging

from pythonosc import udp_client

import iblrig.iotasks as iotasks
import iblrig.user_input as user_input
import iblrig.frame2TTL as frame2TTL
from iblrig.path_helper import SessionPathCreator
from iblrig.misc import make_square_dvamat

log = logging.getLogger('iblrig')


class SessionParamHandler(object):
    """Session object imports user_settings and task_settings
    will and calculates other secondary session parameters,
    runs Bonsai and saves all params in a settings file.json"""

    def __init__(self, task_settings, user_settings):
        # =====================================================================
        # IMPORT task_settings, user_settings, and SessionPathCreator params
        # =====================================================================
        ts = {i: task_settings.__dict__[i]
              for i in [x for x in dir(task_settings) if '__' not in x]}
        self.__dict__.update(ts)
        us = {i: user_settings.__dict__[i]
              for i in [x for x in dir(user_settings) if '__' not in x]}
        self.__dict__.update(us)
        self = iotasks.deserialize_pybpod_user_settings(self)
        spc = SessionPathCreator(self.IBLRIG_FOLDER, self.IBLRIG_DATA_FOLDER,
                                 self.PYBPOD_SUBJECTS[0],
                                 protocol=self.PYBPOD_PROTOCOL,
                                 board=self.PYBPOD_BOARD, make=True)
        self.__dict__.update(spc.__dict__)

        # =====================================================================
        # OSC CLIENT
        # =====================================================================
        self.OSC_CLIENT_PORT = 7110
        self.OSC_CLIENT_IP = '127.0.0.1'
        self.OSC_CLIENT = udp_client.SimpleUDPClient(self.OSC_CLIENT_IP,
                                                     self.OSC_CLIENT_PORT)
        # =====================================================================
        # frame2TTL
        # =====================================================================
        self.F2TTL_GET_AND_SET_THRESHOLDS = frame2TTL.get_and_set_thresholds(self)
        # =====================================================================
        # PROBES + WEIGHT
        # =====================================================================
        self.FORM_DATA = user_input.session_form(mouse_name=self.SUBJECT_NAME)
        self = user_input.parse_form_data(self)
        # =====================================================================
        # VISUAL STIM
        # =====================================================================
        self.VISUAL_STIMULUS_FILE = None
        self.VISUAL_STIMULI = {
            0: 'SPACER',
            1: 'receptive_field_mapping',
            2: 'orientation-direction_selectivity',
            3: 'contrast_reversal',
            4: 'task_stimuli',
            5: 'spontaneous_activity',
        }

        self.STIM_ORDER = [0, 5, 0, 2, 0, 1, 0, 3, 0, 4, 0, 5, 0, 2, 0]
        self.VISUAL_STIM_0 = {

        }
        self.VISUAL_STIM_1 = {
            'patch_shape': 'square',
            'patch_dva': 8,
            'stim_file_name': '_iblrig_RFMapStim.raw.bin',
            'stim_file_shape': [15, 15, 'nframes'],
            'stim_npatches': 225,
            'dva_mat': make_square_dvamat(size=15, dva=8),

        }
        # =====================================================================
        # SAVE SETTINGS FILE AND TASK CODE
        # =====================================================================
        iotasks.copy_task_code(self)
        iotasks.save_task_code(self)
        iotasks.save_session_settings(self)

    # =========================================================================
    # METHODS
    # =========================================================================

    # =========================================================================
    # JSON ENCODER PATCHES
    # =========================================================================
    def reprJSON(self):
        d = self.__dict__.copy()
        d['OSC_CLIENT'] = str(d['OSC_CLIENT'])
        return d


if __name__ == '__main__':
    import task_settings
    import iblrig.fake_user_settings as user_settings
    from pathlib import Path
    iblrig_folder = Path(__file__).parent.parent.parent
    task_settings.IBLRIG_FOLDER = iblrig_folder
    user_settings.PYBPOD_PROTOCOL = '_iblrig_tasks_ephys_certification'
    sph = SessionParamHandler(task_settings, user_settings)
    print("Done!")
