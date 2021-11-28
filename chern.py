# from utils.constants.devices import Devices
# from utils.db_api.db_manager import DBManager
#
# d = DBManager()
#
# d.add_device(Devices.YEELIGHT, ip='192.168.1.3', device_type='smart_bulb', token='3d30dda82fac2d2d8e7d4cfc62315070')


# class multifilter:
#     def judge_half(pos, neg):
#         return pos >= neg
#
#     def judge_any(pos, neg):
#         return pos >= 1
#
#     def judge_all(pos, neg):
#         return neg == 0
#
#     def __init__(self, iterable, *funcs, judge=judge_any):
#         self.iterable = iterable
#         self.funcs = funcs
#         self.judge = judge
#
#     def __iter__(self):
#         for i in self.iterable:
#             pos = 0
#             neg = 0
#             for func in self.funcs:
#                 if func(i):
#                     pos += 1
#                 else:
#                     neg += 1
#
#             if self.judge(pos, neg):
#                 yield i
#
#
# def mul2(i):
#     return i % 2 == 0
#
#
# def mul3(x):
#     return x % 3 == 0
#
#
# def mul5(x):
#     return x % 5 == 0
#
#
# a = [i for i in range(31)]  # [0, 1, 2, ... , 30]
#
# print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all)))

#
# import string
#
# stroke = input()
# start, end = stroke.strip(' ').split('-')
# start_index = string.ascii_letters.index(start)
# end_index = string.ascii_letters.index(end) + 1
#
# print(string.ascii_letters[start_index: end_index])

# import pyttsx3
#
#
# text = 'Betal!'
#
# speak_engine = pyttsx3.init()
# voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[-1].id)
#
#
# speak_engine.say(text)
# speak_engine.runAndWait()
# speak_engine.stop()
# from playsound2 import playsound
# from gtts import gTTS
#
#
# from gtts import gTTS
# from playsound2 import playsound
#
#
# def play_voice(text: str):
#     file_name = "voice.mp3"
#
#     tts = gTTS(text=text, lang='ru')
#     tts.save(file_name)
#     playsound(file_name)
#
#
# play_voice('Привет детка')
#
from utils.devices.smart_bulbs import SmartBulbs

smart_bulb = SmartBulbs()
smart_bulb.switch()
