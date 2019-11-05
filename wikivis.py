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
from tkinter import *
root = Tk()
text = Text(width=50, height=10)
frames = [PhotoImage(file="res/viki.gif", format='gif -index %i' %i) for i in range(37)]
def update(ind):
    frame = frames[ind]
    ind += 1
    label.configure(image=frame)
    root.after(100, update, ind)


label = Label(root)
label.pack()
text.pack()
root.after(0, update, 0)



 
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
    text.insert(1.0, what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        text.insert(1.0, "[log] Вы сказали: " + voice + "\n")
   
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
        text.insert(1.0, "[log] Голос не распознан!\n")
    except sr.RequestError as e:
        text.insert(1.0, "[log] Неизвестная ошибка!\n")
 
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
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute) + "\n")
        stop_listening
   
    elif cmd == 'facts':
        # рассказать анекдот
        facts = ['Гепард может развивать скорость 120 километров в час', 'В Средние века листы для рукописей делали из шкур животных', 'Нельзя кипятить воду больше одного раза. При повторном кипячении выделяется диоксин, ядовитое вещество, вызывающее рак', 'Ученые доказали, что 90% болезней возникают от стресса', 'Яд скорпиона - самая дорогая жидкость в мире', 'Пчёл и ос можно научить искать взрывчатые вещества и наркотики, как собак']
        speak(random.choice(facts) + "\n")
        stop_listening
    elif cmd == 'weather':
        text.insert(1.0, "В каком городе мне узнать погоду?\n")
        weath = r.listen(m)
        own = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc')
        city = r.recognize_google(weath, language="ru-RU").title()
        text.insert(1.0, "[log] Вы сказали: " + city + "\n" )

        observ = own.weather_at_place(city)
        w = observ.get_weather()

        temp = w.get_temperature('celsius')["temp"]

        text.insert(1.0, "В городе " + city + ": " + w.get_detailed_status() + str(temp) + "\n" )
        if temp < 15:
            speak("Температура на улице ниже 15 градусов. Советую одеться потеплее\n")
            stop_listening
        elif temp < 25:
            speak("Температура в районе " + str(temp) +  " градусов тепла. Сегодня можно одеть только ветровку\n")
            stop_listening
        elif temp > 25:
            speak("Температура на улице больше 25 градусов. Можно одеть шорты и футболку\n")
            stop_listening
    elif cmd == 'filework':
        text.insert(1.0, "[log] Говорите...")
        sound = r.listen(m)
        voice = r.recognize_google(sound, language = "ru-RU").lower()
        my_file = "C:/RecordedFile/speech.doc"
        if os.path.isfile(my_file) == True:
            my_file = open('C:/RecordedFile/speech.doc', 'a')
            text.insert(1.0, "[log] Вы сказали: " + voice + "\n")
            my_file.write(voice)
            my_file.close()
            text.insert(1.0, "[log] Файл был перезаписан!\n")
            stop_listening
        else:
            my_file = open('C:/RecordedFile/speech.doc', 'w')
            text.insert(1.0, "[log] Вы сказали: " + voice + "\n")
            my_file.write(voice)
            my_file.close()
            text.insert(1.0, "[log] Файл был создан в папке C:/RecordedFile \n")
            stop_listening
    elif cmd == 'search':
        text.insert(1.0, "Скажите запрос\n")
        voice = r.listen(m)
        search = r.recognize_google(voice, language="ru-RU").lower()
        url = "https://www.google.com/search?q="+search
        webbrowser.open(url)
        text.insert(1.0, "[log] Вы сказали: " + search + "\n")
        speak("Вот, что мне удалось найти\n\n")
        stop_listening
    elif cmd == 'openexe':
        text.insert(1.0, "[log] Внимание! Ярлыки файлов должны быть в C:/Program Files/programs (!!! нижний регистр !!!)\n")
        text.insert(1.0, "Скажите название файла(без рассширения)\n")
        voice = r.listen(m)
        exe = r.recognize_google(voice, language="en-EN").lower()
        text.insert(1.0, "[log] Открытие " + exe +".exe\n")
        os.startfile("C:/programs/" + exe + ".lnk")
        stop_listening

    else:
        speak('Извините, я не расслышала, что вы сказали\n')
        stop_listening

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 20)


 
with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()


speak("Здравствуйте пользователь!\n")
speak("Мое имя Вики\n")
speak("Жду Ваших указаний...\n")


 
stop_listening = r.listen_in_background(m, callback)
root.mainloop()
while True: time.sleep(1.5) # infinity loop
