#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Niccolò Bonacchi
# @Date: Friday, September 13th 2019, 2:57:40 pm
import datetime
import json
import logging
import re
import shutil
from pathlib import Path

from ibllib.graphic import strinput
from pybpodgui_api.models.project import Project

import iblrig.alyx as alyx
import iblrig.logging_  # noqa
import iblrig.path_helper as ph

log = logging.getLogger("iblrig")

# TODO: Add keys for logging all other tests
# Add new keys to this, create optional asker/getter
EMPTY_BOARD_PARAMS = {
    "NAME": None,  # str
    "IBLRIG_VERSION": None,  # str
    "COM_BPOD": None,  # str
    "COM_ROTARY_ENCODER": None,  # str
    "COM_F2TTL": None,  # str
    "F2TTL_DARK_THRESH": None,  # float
    "F2TTL_LIGHT_THRESH": None,  # float
    "F2TTL_CALIBRATION_DATE": None,  # str
    "SCREEN_FREQ_TARGET": 60,  # int (Hz)
    "SCREEN_FREQ_TEST_STATUS": None,  # str
    "SCREEN_FREQ_TEST_DATE": None,  # str
    "WATER_CALIBRATION_RANGE": None,  # [min, max]
    "WATER_CALIBRATION_OPEN_TIMES": None,  # [float, float, ...]
    "WATER_CALIBRATION_WEIGHT_PERDROP": None,  # [float, float, ...]
    "WATER_CALIBRATION_DATE": None,  # str
    "BPOD_TTL_TEST_STATUS": None,
    "BPOD_TTL_TEST_DATE": None,
}


def ensure_all_keys_present(loaded_params, upload=True):
    for k in EMPTY_BOARD_PARAMS:
        if k in loaded_params:
            pass
        elif k not in loaded_params:
            loaded_params.update({k: None})

    write_params(loaded_params, force=True, upload=upload)
    return loaded_params


def create_new_params_dict():
    params = EMPTY_BOARD_PARAMS
    params["NAME"] = get_pybpod_board_name()
    params["IBLRIG_VERSION"] = get_iblrig_version()
    params["COM_BPOD"] = get_board_comport()
    return params


def get_iblrig_version():
    ph.get_iblrig_folder()
    # Find version number from `__init__.py` without executing it.
    file_path = Path(ph.get_iblrig_folder()) / "setup.py"
    with open(file_path, "r") as f:
        version = re.search(r"version=\"([^\"]+)\"", f.read()).group(1)
    return version


def get_pybpod_board_name():
    iblproject_path = Path(ph.get_iblrig_params_folder()) / "IBL"
    p = Project()
    p.load(str(iblproject_path))
    return p.boards[0].name


def get_board_name():
    params_file = Path(ph.get_iblrig_params_folder()) / ".iblrig_params.json"
    pybpod_board_name = get_pybpod_board_name()
    if not params_file.exists():
        return pybpod_board_name

    pars = load_params_file()
    if pybpod_board_name != pars["NAME"]:
        pars["NAME"] = pybpod_board_name
        update_params_file(data=pars)
    return pars["NAME"]


def get_pybpod_board_comport():
    iblproject_path = Path(ph.get_iblrig_params_folder()) / "IBL"
    p = Project()
    p.load(str(iblproject_path))
    return p.boards[0].serial_port


def get_board_comport():
    params_file = Path(ph.get_iblrig_params_folder()) / ".iblrig_params.json"
    pybpod_board_comport = get_pybpod_board_comport()
    if not params_file.exists():
        return pybpod_board_comport
    pars = load_params_file()

    if pybpod_board_comport != pars["COM_BPOD"]:
        pars["COM_BPOD"] = pybpod_board_comport
        update_params_file(data=pars)
    return pars["COM_BPOD"]


def write_params_file(data: dict = None, force: bool = False) -> dict:
    """write_params_file wirtes .iblrig_params.json file to default location
    (iblrig/../iblrig_params/.iblrig_params.json)
    If data is None will assume a dict with the default keys and empty values
    write_params_file(data=None, force=True) to reset to empty parameters
    write_params_file(data=some_dict, force=True) to reset to some_dict
    Use update_params_file for upding the values or adding keys

    :param data: Data to write to file, defaults to None i.e. All keys empty
    :type data: dict, optional
    :param force: Force write of data? , defaults to False
    :type force: bool, optional
    :return: params written to file, creates file on disk
    :rtype: dict
    """
    iblrig_params = Path(ph.get_iblrig_params_folder())
    fpath = iblrig_params / ".iblrig_params.json"
    if fpath.exists() and not force:
        log.warning(f"iblrig params file already exists {fpath}. Not writing...")
        return
    if data is None:
        data = create_new_params_dict()
    with open(fpath, "w") as f:
        log.info(f"Writing {data} to {fpath}")
        json.dump(data, f, indent=1)
    return data


def load_params_file() -> dict:
    """load_params_file loads the .iblrig_params.json file from default location
     (iblrig/../iblrig_params/.iblrig_params.json), will create default params
     file if file is not found

    :return: .iblrig_params.json contents
    :rtype: dict
    """
    iblrig_params = Path(ph.get_iblrig_params_folder())
    fpath = iblrig_params / ".iblrig_params.json"
    bpod_comports = iblrig_params / ".bpod_comports.json"
    if fpath.exists():
        with open(fpath, "r") as f:
            out = json.load(f)
        return ensure_all_keys_present(out, upload=False)
    elif not fpath.exists() and bpod_comports.exists():
        log.warning(
            f"Params file does not exist, found old bpod_comports file. Trying to migrate..."
        )
        try_migrate_to_params()
        return load_params_file()
    elif not fpath.exists() and not bpod_comports.exists():
        log.warning(f"Could not load params file does not exist. Creating...")
        out = ask_params_comports(write_params_file())
        return out


def update_params_file(data: dict, force: bool = False) -> None:
    """update_params_file updates the values of the params file
    If force will add unknown keys to the file, otherwise it will only add known keys.

    :param data: data to update, keys must be known if force=False
    :type data: dict
    :param force: add unknown keys to file?, defaults to False
    :type force: bool, optional
    :return: Noting, updates file on disk
    :rtype: None
    """
    old = load_params_file()
    if old is None:
        log.info("iblrig params file not found, creating...")
        write_params_file()
        old = load_params_file()

    for k in data:
        if k in old.keys():
            old[k] = data[k]
            log.info(f"Updated {k} with value {data[k]}")
        else:
            if not force:
                log.info(f"Unknown key {k}: skipping key...")
                continue
            elif force:
                log.info(
                    f"Adding new key {k} with value {data[k]} to .iblrig_params.json"
                )
                old[k] = data[k]
    write_params_file(data=old, force=True)
    log.info("Updated params file")

    return old


def ask_params_comports(data: dict) -> dict:
    patch = {}
    for k in data:
        if "COM" in k and not data[k]:
            newcom = strinput(
                "RIG CONFIG",
                f"Please insert {k.strip('COM_')} COM port (e.g. COM9): ",
                default="COM",
            )
            patch.update({k: newcom})

    if patch:
        data.update(patch)
        update_params_file(data=patch)
        log.debug(f"Updating params file with: {patch}")

    return data


# Methods for tasks from alyx w/ fallback
def update_params(data: dict) -> None:
    update_params_file(data=data)
    try:
        alyx.update_alyx_params(data=data)
    except Exception as e:
        log.warning(
            f"Could not update board params on Alyx. Saved locally:\n{data}\n{e}"
        )


def load_params() -> dict:
    params_local = load_params_file()
    params_alyx = alyx.load_alyx_params(params_local["NAME"])
    if params_alyx is None:
        log.warning(f"Could not load board params from Alyx.")
    if params_alyx != params_local:
        log.warning(f"Local data and Alyx data mismatch. Trying to update Alyx.")
        alyx.update_alyx_params(data=params_local, force=True)
    return params_local


def write_params(data: dict = None, force: bool = False, upload: bool = True) -> None:
    write_params_file(data=data, force=force)
    if upload:
        try:
            alyx.write_alyx_params(data=data, force=force)
        except Exception as e:
            log.warning(
                f"Could not write board params to Alyx. Written to local file:\n{e}"
            )
    return


def try_migrate_to_params(force=False):
    params_file = Path(ph.get_iblrig_params_folder()) / ".iblrig_params.json"
    comports_file = Path(ph.get_iblrig_params_folder()) / ".bpod_comports.json"
    # See if file exists:
    if params_file.exists() and not force:
        log.info(f"No steps taken - File exists: {params_file}")
        return
    # Get .bpod_comports file and set the COM values
    if comports_file.exists():
        with open(comports_file, "r") as f:
            com_data = json.load(f)
        com_dict = {
            "COM_BPOD": com_data["BPOD"],  # str
            "COM_ROTARY_ENCODER": com_data["ROTARY_ENCODER"],  # str
            "COM_F2TTL": com_data["FRAME2TTL"],
        }  # str
    else:
        com_dict = {
            "COM_BPOD": get_board_comport(),
            "COM_F2TTL": "",
            "COM_ROTARY_ENCODER": "",
        }
    # Find latest H2O calib and set WATER values
    water_dict = {
        "WATER_CALIBRATION_RANGE": "",  # [min, max]
        "WATER_CALIBRATION_OPEN_TIMES": "",  # [float, float, ...]
        "WATER_CALIBRATION_WEIGHT_PERDROP": "",  # [float, float, ...]
        "WATER_CALIBRATION_DATE": "",
    }  # str
    range_file = ph.get_water_calibration_range_file()
    func_file = ph.get_water_calibration_func_file()
    if (str(func_file) != "." and str(range_file) != ".") and (
        func_file.parent == range_file.parent
    ):
        water_dict.update(ph.load_water_calibraition_range_file(range_file))
        water_dict.update(ph.load_water_calibraition_func_file(func_file))
        water_dict.update(
            {"WATER_CALIBRATION_DATE": func_file.parent.parent.parent.name}
        )
    if str(func_file) != ".":
        water_dict.update(ph.load_water_calibraition_func_file(func_file))
        water_dict.update(
            {"WATER_CALIBRATION_DATE": func_file.parent.parent.parent.name}
        )
    # Find latest F2TTL calib and set F2TTL values
    f2ttl_params = alyx.load_alyx_params(get_pybpod_board_name())
    if f2ttl_params is None:
        f2ttl_dict = {
            "F2TTL_DARK_THRESH": "",
            "F2TTL_LIGHT_THRESH": "",
            "F2TTL_CALIBRATION_DATE": "",
        }
    else:
        f2ttl_dict = {
            "F2TTL_DARK_THRESH": f2ttl_params["F2TTL_DARK_THRESH"],
            "F2TTL_LIGHT_THRESH": f2ttl_params["F2TTL_LIGHT_THRESH"],
            "F2TTL_CALIBRATION_DATE": datetime.datetime.now().date().isoformat(),
        }
        if "COM_F2TTL" in f2ttl_params:
            f2ttl_dict.update({"COM_F2TTL": f2ttl_params["COM_F2TTL"]})
        elif "F2TTL_COM" in f2ttl_params:
            f2ttl_dict.update({"COM_F2TTL": f2ttl_params["F2TTL_COM"]})
        if "F2TTL_CALIBRATION_DATE" in f2ttl_params:
            f2ttl_dict.update(
                {"F2TTL_CALIBRATION_DATE": f2ttl_params["F2TTL_CALIBRATION_DATE"]}
            )

    # Save locally
    final_dict = {}
    final_dict.update({"NAME": get_board_name()})  # from GUI
    final_dict.update(com_dict)
    final_dict.update(f2ttl_dict)
    final_dict.update(water_dict)
    write_params_file(data=final_dict, force=True)
    # upload to Alyx board
    alyx.write_alyx_params(data=final_dict, force=True)
    # Delete old comports file
    if comports_file.exists():
        bk = Path(ph.get_iblrig_params_folder()) / ".bpod_comports.json_bk"
        shutil.copy(str(comports_file), str(bk))
        comports_file.unlink()
    return


if __name__ == "__main__":
    # try_migrate_to_params(force=True)
    # try_migrate_to_params(force=False)
    params = load_params_file()
    print(".")
