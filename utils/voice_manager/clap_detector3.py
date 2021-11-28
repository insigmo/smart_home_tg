import math
import struct
from time import sleep

import numpy
import pyaudio
from scipy.io.wavfile import read

from utils.devices.smart_bulbs import SmartBulbs
from utils.misc.logging import logger
from utils.voice_manager.herald import Herald
from utils.voice_manager.microphone_templates import clap_template

INITIAL_TAP_THRESHOLD = 0.265
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0 / 32768.0)
CHANNELS = 2
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0 / INPUT_BLOCK_TIME
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0 / INPUT_BLOCK_TIME
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15 / INPUT_BLOCK_TIME


class TapDetector:
    def __init__(self):
        self.microphone = Herald()
        self.stream = self.microphone.open_pyaudio_mic_stream(**clap_template)

        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisy_count = MAX_TAP_BLOCKS + 1
        self.quiet_count = 0
        self.error_count = 0
        self.smart_bulb = SmartBulbs()

    @classmethod
    def get_rms(cls, block):
        a = read("adios.wav")
        numpy.array(a[1], dtype=float)
        count = len(block) / 2
        format = f"{int(count)}h"
        shorts = struct.unpack(format, block)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n

        rms = math.sqrt(sum_squares / count)
        logger.info(f'{rms=}')
        return rms

    def tap_detected(self):
        self.smart_bulb.switch()
        print("tapped")

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except Exception as ex:
            self.error_count += 1
            logger.warning(f"{self.error_count} Error recording: {ex}")
            self.noisy_count = 1
            return

        amplitude = self.get_rms(block)
        if amplitude > self.tap_threshold:
            # noisy block
            self.quiet_count = 0
            self.noisy_count += 1
        else:
            # quiet block.

            if 1 <= self.noisy_count <= MAX_TAP_BLOCKS:
                self.tap_detected()

            self.noisy_count = 0
            self.quiet_count += 1


if __name__ == "__main__":
    tt = TapDetector()

    while True:
        tt.listen()
        sleep(0.1)
