import logging

from pybpodapi.protocol import Bpod

log = logging.getLogger("iblrig")


if __name__ == "__main__":
    bpod = Bpod()
    msg = BpodMessageCreator(bpod)