#Вики Voice manager v1
import os
import os.path
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
        "music": ('включи музыку','музыка'),
        "fjokes": ('расскажи анекдот','рассмеши меня','ты знаешь анекдоты'),
        "weather": ('скажи погоду в городе', 'какая погода в городе', 'погода в городе', 'погада в городе', 'погуда в городе', 'какая погуда городе'),
        "filework": ('открой документ', 'дакумент', 'окрыть документ', 'документ')
    }
    "acmd": {
        "acmdfile": ('закрыть файл', 'закрытие файла', 'зокрой файл', 'зокрыть файл')


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
   
    elif cmd == 'music':
        # воспроизвести музыку
   
    elif cmd == 'fjokes':
        # рассказать анекдот
        speak("А на ладошах мне не попрыгать? Ахахахаха")
    elif cmd == 'weather':
        print("В каком городе мне узнать погоду?")
        weath = r.listen(voice)
        owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc')
        city = r.recognize_google(weath, language="ru-RU")
        print("[log] Вы сказали: " + city.lower() )

        observ = own.weather_at_place(city)
        w = observ.get_weather()

        temp = w.get_temperature('celsius')["temp"]

        speak("В городе " + city + ": " + w.get_detailed_status() + str(temp) )
    elif cmd == 'filework':
    	voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
    	acmd = voice
    	my_file = "speech.txt"
    	if os.path.isfile(my_file) == True:
    		my_file = open('speech.txt', 'a')
    		my_file.write(voice)
    	else:
    		my_file = open('speech.txt', 'w')
    		my_file.write(voice)
    	acmd = recognize_acmd(acmd)
    	execute_acmd(acmd["acmd"])
    else:
        print('Извините, я не расслышала, что Вы сказали...')

def recognize_acmd(acmd):
    RC = {'acmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['acmd'] = c
                RC['percent'] = vrt
   
    return RC
def execute_acmd(acmd, my_file):
	if acmd == 'acmdfile':
		my_file.close 
# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 4)
 
with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()
 

#voices = speak_engine.getProperty('voices')
#speak_engine.setProperty('voice', voices[4].id)

 
speak("Здравствуйте, пользователь!")
speak("Мое имя Вики")
speak("Жду Ваших указаний...")
 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(1.5) # infinity loop
