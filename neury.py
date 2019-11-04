#Вики Voice manager v1.5(Новый Оброзец!!!!!!!)
import os
import os.path
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import pyowm
import webbrowser
import random
import platform
import subprocess


 
# настройки
opts = {
    "alias": ('вики','вик','век','викусь','векусь','веке',
              'веки','вике','вика','века','вэка'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
        "music": ('включи музыку','музыка'),
        "facts": ('расскажи факты','интересные факты','факты'),
        "weather": ('скажи погоду', 'какая погода', 'погода', 'погада', 'погуда', 'какая погуда'),
        "filework": ('открой документ', 'дакумент', 'окрыть документ', 'документ'),
        "search": ('начать поиск', 'поиск', 'искать'),
        "openexe": ('открыть файл', 'открой файл', 'файл', 'фойл', 'фуйл')
    }
}
 
# functions
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Вы сказали: " + voice)
   
        if voice.startswith(opts["alias"]):
            #interacting with Viki
            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
           
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
           
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
 
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка!")
 
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
        stop_listening
   
    elif cmd == 'facts':
        # рассказать анекдот
        facts = ['Гепард может развивать скорость 120 километров в час', 'В Средние века листы для рукописей делали из шкур животных', 'Нельзя кипятить воду больше одного раза. При повторном кипячении выделяется диоксин, ядовитое вещество, вызывающее рак', 'Ученые доказали, что 90% болезней возникают от стресса', 'Яд скорпиона - самая дорогая жидкость в мире', 'Пчёл и ос можно научить искать взрывчатые вещества и наркотики, как собак']
        speak(random.choice(facts))
        stop_listening
    elif cmd == 'weather':
        print("В каком городе мне узнать погоду?")
        weath = r.listen(m)
        own = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc')
        city = r.recognize_google(weath, language="ru-RU").title()
        print("[log] Вы сказали: " + city )

        observ = own.weather_at_place(city)
        w = observ.get_weather()

        temp = w.get_temperature('celsius')["temp"]

        print("В городе " + city + ": " + w.get_detailed_status() + str(temp) )
        if temp < 15:
        	speak("Температура на улице ниже 15 градусов. Советую одеться потеплее")
        	stop_listening
        if temp < 25:
        	speak("Температура в районе " + str(temp) +  " градусов тепла. Сегодня можно одеть только ветровку")
        	stop_listening
        if temp > 25:
        	speak("Температура на улице больше 25 градусов. Можно одеть шорты и футболку")
        	stop_listening
    elif cmd == 'filework':
    	sound = r.listen(m)
    	voice = r.recognize_google(sound, language = "ru-RU").lower()
    	my_file = "C:/RecordedFile/speech.txt"
    	print("[log] Говорите...")
    	if os.path.isfile(my_file) == True:
    		my_file = open('C:/RecordedFile/speech.txt', 'a')
    		print("[log] Вы сказали: " + voice)
    		my_file.write(voice)
    		my_file.close()
    		stop_listening
    	else:
    		my_file = open('C:/RecordedFile/speech.txt', 'w')
    		print("[log] Вы сказали: " + voice)
    		my_file.write(voice)
    		my_file.close()
    		stop_listening
    elif cmd == 'search':
    	print("Скажите запрос")
    	voice = r.listen(m)
    	search = r.recognize_google(voice, language="ru-RU").lower()
    	url = "https://www.google.com/search?q="+search
    	webbrowser.open(url)
    	speak("Вот, что мне удалось найти")
    	stop_listening
    elif cmd == 'openexe':
    	print("[log] Внимание! Ярлыки файлов должны быть в C:/Program Files/programs (!!! нижний регистр !!!)")
    	print("Скажите название файла(без рассширения)")
    	voice = r.listen(m)
    	exe = r.recognize_google(voice, language="en-EN").lower()
    	print("[log] Открытие " + exe +".exe")
    	os.startfile("C:/programs/" + exe + ".lnk")
    	stop_listening

    else:
        speak('Извините, я не расслышала, что вы сказали')
        stop_listening

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 11)
 
with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()



speak("Здравствуйте пользователь!")
speak("Мое имя Вики")
speak("Жду Ваших указаний...")
 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(1.5) # infinity loop
