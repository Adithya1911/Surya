import pyttsx3,pyautogui,pyjokes
import os
import datetime,wikipedia,psutil
import smtplib
import speech_recognition as sr
import webbrowser as wb

 
engine=pyttsx3.init()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


#speak('This is Surya, Ai Assistant')
def time():
    Time=datetime.datetime.now().strftime("%I:%M:%S")
    speak("The Current Time is")
    speak(Time)
    # speak(datetime.datetime.now())
    print(datetime.datetime.now())

#time()


def date():
    year=int(datetime.datetime.now().year)
    month=int(datetime.datetime.now().month)
    date=int(datetime.datetime.now().day)
    speak("The Current Date is") 
    speak(date)
    speak(month)
    speak(year)


def wishme():
    speak("hello Sir!")
    
    time()
    
    date()


#wishme()

def screenshot():
    img = pyautogui.screenshot()
    img.save('D:\memory card\scrennshots\ss.jpg')
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        audio=r.listen(source)

    try:
        print('Recongnizing..')
        query=r.recognize_google(audio,language='en-in')
        speak(query)
    

    except Exception as e:
        print(e)
        speak("say again")
        return 'None'
    return query
#takeCommand()
def cpu():
    usage=str(psutil.cpu_percent())
    speak('cpu is at'+ usage)
    battery=psutil.sensors_battery()
    speak('Battery is at  ')
    speak(battery.percent)

def sendmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('testit.5325@gmail.com','lmrahualeocdmgof')
    server.sendmail('testit.5325@gmail.com',to,content)

if __name__=="__main__":
    #wishme()
    while True:
        query=takeCommand().lower()
        if 'time' in query:
            time()
        elif 'wikipedia' in query:
            speak('Searching...')
            query=query.replace('wikipedia','')
            result=wikipedia.summary(query,sentences=1)
            print(result)
            speak(result)
        


        elif 'search in chrome' in query:
            speak("what should i Search!!!?")
            chromepath='C:\Program Files\Google\Chrome\Application\chrome.exe %s'
            Search=takeCommand().lower()
            wb.get(chromepath).open_new_tab(Search + '.com')
        elif 'logout' in query:
            os.system('shutdown -l')
        elif 'shutdown' in query:
            os.system('shutdown /s /t 1')
        elif 'restart' in query:
            os.system('shutdown /r /t 1')

        elif 'play songs' in query:
            songs_dir = 'D:\memory card\Music'
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir,songs[0])) 
        
        elif 'screenshot' in query:
            screenshot()
            speak('done')

        elif 'cpu' in query:cpu()


        elif 'remember that' in query:
            speak('What should i Remeber ?')
            data =takeCommand()
            speak('You said me to remember that' + data)
            remember=open('data.txt','w')
            remember.write(data)
            remember.close()

        
        elif 'do you know anything' in query:
            remember=open('data.txt','r')
            speak('you said me to remember that'+remember.read())

  
        

        elif 'send mail' in query:
            try:
                speak('What should I Say?')
                content= takeCommand()
                to=input(speak('enter the reciver"s email:'))
                sendmail(to,content)
                speak('Email has been sent!')
            except Exception as e:
                print(e)
                speak('Unable to Send the email')
            
        elif 'joke' in query:speak(pyjokes.get_joke())

        elif 'date' in query:date()
        elif 'offline' in query:quit() 
