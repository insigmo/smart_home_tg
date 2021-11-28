import pyaudio

from utils.misc.logging import logger


class Herald:
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def stop(self):
        self.stream.close()

    @property
    def device_index(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)

            for keyword in ["mic", "input"]:
                if keyword in devinfo["name"].lower():
                    logger.debug(f"Found an input: device{i}: {devinfo['name']}")
                    device_index = i
                    return device_index

        if device_index is None:
            logger.warning("No preferred input found; using default input device.")

        return device_index

    def open_pyaudio_mic_stream(self, device_index: int = None, **kwargs):
        if not self.stream:
            device_index = device_index if device_index else self.device_index
            self.stream = self.pa.open(input_device_index=device_index, **kwargs)
            return self.stream
