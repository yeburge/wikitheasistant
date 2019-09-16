#Вики Voice maager v1
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import pyowm


 
# настройки
opts = {
    "alias": ('вики','вик','век','викусь','векусь','веке',
              'веки','вике','вика','века','вэка'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),
        "music": ('включи музыку','воспроизведи радио','включи радио'),
        "fjokes": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
        "weather": ('скажи погоду в городе', 'какая погода в городе', 'погода в городе', 'погада в городе', 'погуда в городе', 'какая погуда городе')
    }
}
 
# функции
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
            # обращаются к Кеше
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
   
    elif cmd == 'music':
        # воспроизвести радио
        os.system("D:\\Projects\\Python\\neural\\res\\music\\LD.m3u")
   
    elif cmd == 'fjokes':
        # рассказать анекдот
        speak("А на ладошах мне не попрыгать? Ахахахаха")
    elif cmd == 'weather':
    	print("В каком городе мне узнать погоду?")
    	r = sr.Recognizer()
    	with sr.Microphone(device_index = 20) as source1:
    		weath = r.listen(source1)
        owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc')
    	city = r.recognize_google(weath, language="ru-RU")
    	print("[log] Вы сказали: " + city.lower() )

    	observ = own.weather_at_place(city)
    	w = observ.get_weather()

    	temp = w.get_temperature('celsius')["temp"]

    	speak("В городе " + city + ": " + w.get_detailed_status() + str(temp) )
    else:
        print('Извините, я не расслышала, что Вы сказали...')
 
# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 20)
 
with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()
 

#voices = speak_engine.getProperty('voices')
#speak_engine.setProperty('voice', voices[4].id)

 
speak("Здравствуйте, пользователь!")
speak("Мое имя Вики")
speak("Жду Ваших указаний...")
 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop