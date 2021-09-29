#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File: iblrig/envs.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Tuesday, September 28th 2021, 11:51:11 am
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MC = (
    "conda"
    if "mamba" not in str(subprocess.check_output([os.environ["CONDA_EXE"], "list", "-n", "base", "--json"]))
    else "mamba"
)


def get_env_folder(env_name: str = "iblenv") -> str:
    """get_env_folder Return conda folder of [env_name] environment

    :param env_name: name of conda environment to look for, defaults to 'iblenv'
    :type env_name: str, optional
    :return: folder path of conda environment
    :rtype: str
    """
    all_envs = subprocess.check_output([f"{MC}", "env", "list", "--json"], shell=True)
    all_envs = json.loads(all_envs.decode("utf-8"))
    pat = re.compile(f"^.+{env_name}$")
    env = [x for x in all_envs["envs"] if pat.match(x)]
    env = env[0] if env else None
    return env


def _get_env_python_ou_pip(env_name: str = "iblenv", rpip=False):
    env = get_env_folder(env_name=env_name)
    if sys.platform in ["Windows", "windows", "win32"]:
        pip = os.path.join(env, "Scripts", "pip.exe")
        python = os.path.join(env, "python.exe")
    else:
        pip = os.path.join(env, "bin", "pip")
        python = os.path.join(env, "bin", "python")

    return python if not rpip else pip


def get_env_python(env_name: str = "iblenv"):
    return _get_env_python_ou_pip(env_name=env_name, rpip=False)


def get_env_pip(env_name: str = "iblenv"):
    return _get_env_python_ou_pip(env_name=env_name, rpip=True)


def get_base_python():
    return os.environ["CONDA_PYTHON_EXE"]


def get_base_pip():
    if sys.platform in ["Windows", "windows", "win32"]:
        return Path(os.environ["CONDA_PYTHON_EXE"]).parent.joinpath("Scripts", "pip.exe")
    elif sys.platform in ["Linux", "linux"]:
        return Path(os.environ["CONDA_PYTHON_EXE"]).parent.joinpath("pip")
    else:
        raise ValueError("Unsupported platform")
