from iblpybpod.pybpodapi.settings import TARGET_BPOD_FIRMWARE_VERSION


if TARGET_BPOD_FIRMWARE_VERSION == "20":
    from iblpybpod.pybpodapi.bpod.hardware.events.bpod0_7_9_fw20 import EventName
elif TARGET_BPOD_FIRMWARE_VERSION == "17":
    from iblpybpod.pybpodapi.bpod.hardware.events.bpod0_7_9_fw13 import EventName
elif TARGET_BPOD_FIRMWARE_VERSION == "15":
    from iblpybpod.pybpodapi.bpod.hardware.events.bpod0_7_9_fw13 import EventName
elif TARGET_BPOD_FIRMWARE_VERSION == "13":
    from iblpybpod.pybpodapi.bpod.hardware.events.bpod0_7_9_fw13 import EventName
elif TARGET_BPOD_FIRMWARE_VERSION == "9":
    from iblpybpod.pybpodapi.bpod.hardware.events.bpod0_7_5_fw9 import EventName
else:
    from iblpybpod.pybpodapi.bpod.hardware.events.bpod0_7_9_fw20 import EventName
