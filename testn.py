#micro&bot test
#(device_index=27)
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone(device_index=20) as source:
    print("Скажи что-нибудь...")
    audio = r.listen(source)

query = r.recognize_google(audio, language="ru-Ru")
print("Тестовое предложение: " + query.lower()) 
