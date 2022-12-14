# used for pybpodgui_plugin_waveplayer
# generate wav file containing sine waves
# FB36 - 20120617
import math, wave, array, struct, numpy as np
from pybpodgui_plugin_waveplayer.module_api import WavePlayerModule

amplitude   = 3.0
duration    = 3 # seconds
freq        = 1000 # of cycles per second (Hz) (frequency of the sine waves)
volume      = 100 # percent
sampleRate  = 96000 # of samples per second (standard)
numChan     = 1 # of channels (1: mono, 2: stereo)
dataSize    = 2 # 2 bytes because of using signed short integers => bit depth = 16


samples = np.arange(0, duration, 1/sampleRate)
wave    = amplitude * np.sin(2*math.pi*freq*samples)


"""
data = array.array('h') # signed short integer (-32768 to 32767) data
numSamplesPerCyc = int(sampleRate / freq)
numSamples = sampleRate * duration
for i in range(numSamples):
    
    sample = 32767 * float(volume) / 100
    sample *= math.sin(math.pi * 2 * (i % numSamplesPerCyc) / numSamplesPerCyc)
    data.append(int(sample))
"""

m = WavePlayerModule('/dev/ttyACM0')

print( m.set_sampling_period(sampleRate) )
m.set_output_range(m.RANGE_VOLTS_MINUS5_5)
m.set_loop_mode([False, False, False, False])
m.debug()

print(m.load_waveform(0, wave))

print(m.play(1, 0))