import pyaudio

clap_template = {
    "format": pyaudio.paInt16,
    "channels": 2,
    "rate": 44100,
    "input": True,
    "frames_per_buffer": int(44100 * 0.05)
}
