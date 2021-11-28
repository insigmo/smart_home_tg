import struct
from time import sleep

import math
import pyaudio

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


class ClapAnalyzer:
    def __init__(self, note_lengths: list = None, deviation_threshold: float = 0.1):
        """
        :param note_lengths: Relative note lengths in the rhythmic pattern. F.ex. [2, 1, 1, 2, 2]
        :param deviation_threshold: How much deviation from the pattern should be considered failure
        :return:
        """
        if note_lengths is None:
            note_lengths = [1. / 4, 1. / 8, 1. / 8, 1. / 4, 1. / 4]

        self.buffer_size = len(note_lengths)
        self.pattern = self.note_lengths_to_normalized_pauses(note_lengths)
        self.pattern_sum = sum(self.pattern)

        self.min_pattern_time = .1 * self.pattern_sum  # min 100 ms between fastest clap in sequence
        self.max_pattern_time = .5 * self.pattern_sum  # max 500 ms between fastest clap in sequence

        self.clap_times = [None] * self.buffer_size
        self.deviation_threshold = deviation_threshold
        self.current_index = 0

        self.clap_listeners = set()
        self.clap_sequence_listeners = set()

        self.microphone = Herald()
        self.stream = self.microphone.open_pyaudio_mic_stream(**clap_template)

        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisy_count = MAX_TAP_BLOCKS + 1
        self.quiet_count = 0
        self.error_count = 0

    @staticmethod
    def note_lengths_to_normalized_pauses(note_lengths):
        note_lengths.pop()  # Because the length of the last note doesn't matter
        min_note_length = float(min(note_lengths))
        return map(lambda x: x / min_note_length, note_lengths)

    def on_clap(self, fn):
        self.clap_listeners.add(fn)

    def on_clap_sequence(self, fn):
        self.clap_sequence_listeners.add(fn)

    def clap(self, time):
        """
        Tell ClapAnalyzer that a clap has been detected at the specified time
        :param time: Absolute time in seconds. Must be float.
        :return:
        """
        for fn in self.clap_listeners:
            fn()

        self.current_index = (self.current_index + 1) % self.buffer_size
        self.clap_times[self.current_index] = time

        first_clap_in_sequence = self.clap_times[self.current_index - self.buffer_size + 1]
        if first_clap_in_sequence is None:
            return 0

        time_diff = time - first_clap_in_sequence
        avg_time_per_clap_unit = time_diff / self.pattern_sum
        if self.min_pattern_time <= time_diff <= self.max_pattern_time:
            total_deviation = 0
            j = 0
            for i in range(self.current_index - self.buffer_size + 1, self.current_index):
                clap_time_diff = self.clap_times[i + 1] - self.clap_times[i]
                relative_clap_time_diff = clap_time_diff / avg_time_per_clap_unit
                total_deviation += (relative_clap_time_diff - self.pattern[j]) ** 2
                j += 1

            if total_deviation < self.deviation_threshold:
                for fn in self.clap_sequence_listeners:
                    fn()
                return 1
            else:
                return 0
        else:
            return 0

    @classmethod
    def get_rms(cls, block):
        count = len(block) / 2
        format = f"{int(count)}h"
        shorts = struct.unpack(format, block)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n

        rms = math.sqrt(sum_squares / count)
        print(f'{rms=}')
        return rms

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except Exception as ex:
            self.error_count += 1
            print(f"{self.error_count} Error recording: {ex}")
            self.noisy_count = 1
            return

        amplitude = self.get_rms(block)

        claps = list(map(lambda x: self.clap(self.get_rms(block)), range(10)))

        if amplitude > self.tap_threshold:
            # noisy block
            self.quiet_count = 0
            self.noisy_count += 1
        else:
            # quiet block.

            if 1 <= sum(claps) // len(claps) <= MAX_TAP_BLOCKS:
                self.tap_detected()

            self.noisy_count = 0
            self.quiet_count += 1

    def tap_detected(self):
        print("tapped")


if __name__ == '__main__':
    c = ClapAnalyzer()
    while True:
        c.listen()
        sleep(0.1)
