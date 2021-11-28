from time import sleep

import arrow
from fuzzywuzzy import fuzz
from gtts import gTTS
from playsound import playsound
from speech_recognition import Recognizer, Microphone, UnknownValueError, RequestError

from utils.devices.smart_bulbs import SmartBulbs
from utils.misc.logging import logger
from utils.voice_manager.herald import Herald

options = {
    "alias": ('сэм', '7', 'сэми', 'семь', 'сайт', 'сам'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "smart_bulb_on": ('включи', 'включи лампу'),
        "smart_bulb_off": ('выключи', 'выключи лампу'),
        "set_red_color": ('красный цвет', 'поставь красный цвет'),
        "gerara": ('арсен', 'арсен шогенов', 'что нужно сказать Арсену'),
    }
}


class VoiceAssistant:
    def __init__(self):
        self.herald = Herald()
        self.speak_engine = None

        # запуск
        self.recognizer = Recognizer()
        self.microphone = Microphone(device_index=self.herald.device_index)

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.smart_bulb = SmartBulbs()

    @classmethod
    def speak(cls, text: str):
        file_name = "voice.mp3"

        tts = gTTS(text=text, lang='ru')
        tts.save(file_name)
        playsound(file_name)

    @classmethod
    def recognize_cmd(cls, command: str):
        percent = 0
        cmd = ''

        for call_cmd, variants in options['cmds'].items():
            for variant in variants:
                delta = fuzz.ratio(command, variant)
                if delta > percent:
                    cmd = call_cmd
                    percent = delta

        return cmd

    def execute_cmd(self, cmd):
        if cmd == 'ctime':
            now = arrow.now()
            self.speak(f"Сейчас {now.hour} : {now.minute}")

        elif cmd == 'smart_bulb_on':
            self.smart_bulb.turn_on()

        elif cmd == 'smart_bulb_off':
            self.smart_bulb.turn_off()

        elif cmd == 'gerara':
            self.speak("Паашел ты")

        else:
            error_msg = 'Команда не распознана, повторите!'
            logger.debug(error_msg)

    def __callback(self, recognizer, audio):
        try:
            voice = recognizer.recognize_google(audio, language="ru-RU").lower()
            logger.info("[log] Распознано: " + voice)

            # if voice.startswith(options["alias"]):
            cmd = ''
            for alias in options['alias']:
                cmd = voice.replace(alias, "").strip()

            for x in options['tbr']:
                cmd = voice.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = self.recognize_cmd(cmd)
            self.execute_cmd(cmd)

        except UnknownValueError:
            logger.info("[log] Голос не распознан!")
        except RequestError:
            logger.info("[log] Неизвестная ошибка, проверьте интернет!")

    def run(self):
        self.speak("Cэм слушает")

        stop_listening = self.recognizer.listen_in_background(self.microphone, self.__callback)
        while stop_listening:
            sleep(0.1)  # infinity loop


if __name__ == '__main__':
    v = VoiceAssistant()
    v.run()
