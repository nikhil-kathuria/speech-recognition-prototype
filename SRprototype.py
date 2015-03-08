"""
SRprototype.py
A Speech reconginition prototype using python as development language and
google speech reconginition API, and Open Weather API. Both API's mentioned
give response only when reqesting client has a valid key.

There is limit of 50 calls per day to API as of now and politenes is expected
in making use of free service offered by Google and openweathermap.org
Moreover use of API key for anything other than personal or testing purposes
is not recomended

The SRprototype.py has functionality to display route from current location to
destination via chrome browser. Morevoer using openweathermap it can tell the
weather update of any city. It can play any .wav file present on filesystem,
for now the directory where the file is SRprototype.py is kept. It is a
prototype with limited and fixed functionality
"""


"""
DEPENDENCIES
Python modules used directly
os
time
pyowm
glob
MIMEText from email.mime.text

Python modules used by other imported API
io, os, subprocess, wave
math, audioop, collections
json

SRprototype requires the python PyAudio is installed. The PlayMusic_API
requires both python pyaudio and wave module installed and imported into file.

For errors and exceptions
originating from SR_API please consult the documented page at
https://github.com/Uberi/speech_recognition
"""


"""
Copyright (c) 2014, Nikhil Kathuria
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the Nikhil Kathuria nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Nikhil Kathuria BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


# Import the python modules and other project related api

from SR_API import Recognizer, Microphone
from PlayMusic_API import AudioFile
import os
import time
import pyowm
from glob import glob
from email.mime.text import MIMEText


"""
processor function which takes initialize inputs in main() as parameters
"""


def processor(r, m, v, c, url, me):
    os.system(v + 'Hello, how may I help you?')
    time.sleep(.5)
    print("Tell me something..")
    with m as source:
        audio = r.listen(source)
    print("Captured what you said..")
    # Check in catch block to handle exceptions gracefully
    try:
        text = r.recognize(audio)
        print("You said, " + text)
        words = text.split()
        # Check the presensce of keyword
        for itr in xrange(0, len(words)):
            """
            Block for presence of any of 'music', 'song', 'play' word
            in speech decoded by google speech api. In case any of the
            above word matches the user is asked for song name. The song
            name is checked against all .wav files present in current directory
            """
            if words[itr] == c[7] or words[itr] == c[8] or words[itr] == c[9]:
                # Check for all the wave files in present directory
                os.system(v + 'Tell me the song name')
                time.sleep(.5)
                print("Tell me the song name")
                with m as source:
                    audio = r.listen(source)
                print("Captured what you said..")
                try:
                    text = r.recognize(audio)
                    song = glob('*' + text + '*.wav')
                    if song:
                        for song in glob('*' + text + '*.wav'):
                            print('Playing, ' + song)
                            os.system(v + 'Playing, ' + song)
                            time.sleep(.5)
                            file = AudioFile(song)
                            file.play()
                            file.close()
                    else:
                        print ('No media named ' + text + ' found')
                        os.system(v + 'No media named ' + text + ' found')
                except LookupError:
                    print ('I am sorry I cannot help you with that')
                    os.system(v + 'I am sorry I cannot help you with that')
                    time.sleep(.5)
                break
                """
                Block for presence of any of 'navigate', 'navigation', 'route'
                word in speech decoded by google speech api. In case any of
                the above word matches then the user is asked for destination
                the google maps route is displayed in chrome browser from
                current location determined by chrome
                """
            elif words[itr] == c[10] or words[itr] == c[11] or words[itr] == c[12]:
                os.system(v + 'To which place you want to go?')
                time.sleep(.5)
                print("To which place you want to go?")
                with m as source:
                    audio = r.listen(source)
                print("Captured what you said..")
                try:
                    text2 = r.recognize(audio)
                    print("You said, " + text2)
                    os.system(v + 'Navigating to ' + text2)
                    text3 = text2.split()
                    if len(text3) == 1:
                        os.system(url + text2)
                    elif len(text3) > 1:
                        text3 = text2.replace(" ", "+")
                        os.system(url + text3)
                except LookupError:
                    print ('I am sorry I cannot help you with that')
                    os.system(v + 'I am sorry I cannot help you with that')
                    time.sleep(.5)
                break
                """
                Block for presence of any of 'email' , 'mail'
                word in speech decoded by google speech api. In case any of
                the above word matches then the user is asked for receipient
                subject and message. After this as of now the MIMEText of
                email is shown on display.
                """
            elif words[itr] == c[3] or words[itr] == c[4]:
                os.system(v + 'Whom should I send it to?')
                time.sleep(.5)
                print("Tell me the receipient")
                with m as source:
                    audio = r.listen(source)
                try:
                    text = r.recognize(audio)
                    print("The receipient, " + text)
                    to = text
                except LookupError:
                    print ('I am sorry I cannot help you with that')
                    os.system(v + 'I am sorry I cannot help you with that')
                    time.sleep(.5)

                os.system(v + 'What is the subject?')
                time.sleep(.5)
                print("Tell me the subject")
                with m as source:
                    audio = r.listen(source)
                try:
                    text = r.recognize(audio)
                    print("The subject," + text)
                    sub = text
                except LookupError:
                    print ('I am sorry I cannot help you with that')
                    os.system(v + 'I am sorry I cannot help you with that')
                    time.sleep(.5)

                os.system(v + 'What is the message?')
                time.sleep(.5)
                print("Tell me the message")
                with m as source:
                    audio = r.listen(source)
                try:
                    text = r.recognize(audio)
                    print("You said, " + text)
                    os.system(v + 'You said, ' + text)
                    msg = MIMEText(str(text))
                    msg['Subject'] = sub
                    msg['To'] = to
                    msg['From'] = me
                    print ("Your Email" + "\n")
                    print msg
                except LookupError:
                    print ('I am sorry I cannot help you with that')
                    os.system(v + 'I am sorry I cannot help you with that')
                    time.sleep(.5)
                break
                """
                Block for presence of any of 'climate', 'weather'
                word in speech decoded by google speech api. In case any of
                the above word matches then the user is asked for city
                After this the user is responded with both voice and
                text on console regarding the status and temperature
                of the input city
                """
            elif words[itr] == c[5] or words[itr] == c[6]:
                os.system(v + 'Please specify city')
                time.sleep(.5)
                print ('Tell me the city')
                with m as source:
                    audio = r.listen(source)
                try:
                    print("Captured what you said..")
                    text = r.recognize(audio)
                    city = str(text)
                    print("You said, " + city)
                    os.system(v + 'Getting weather for' + city)
                    owm = pyowm.OWM('387f0630ab1d2475ee41231c86a4de14')
                    observation = owm.weather_at_place(city)
                    w = observation.get_weather()
                    rt = w.get_temperature('fahrenheit')
                    rec = "Now " + str(w.get_status()) + " and " + str(rt['temp']) + " degree fahrenheit at " + city
                    print (rec)
                    os.system(v + rec)
                    time.sleep(.5)
                except LookupError:
                    print ('I am sorry I cannot help you with that')
                    os.system(v + 'I am sorry I cannot help you with that')
                    time.sleep(.5)
                break

    except LookupError:
        print ('I am sorry I cannot help you with that')
        os.system(v + 'I am sorry I cannot help you with that')
        time.sleep(.5)


"""
Initialize the Recognizer and Mircrophone object. Initialize the
array for possible functionality supportede by prototype
Assign Mac OS voice of Daniel to variable v as os command.
Assign the value of url as os command
"""


if __name__ == "__main__":
    r = Recognizer()
    m = Microphone()
    v = "/usr/bin/say -v Daniel "
    c = ['write', 'dictate', 'note', 'email', 'mail',
         'climate', 'weather', 'music', 'song', 'play',
         'navigate', 'navigation', 'route']
    url = '/usr/bin/open -a Google\ Chrome http://google.com/maps/dir/My+Location/'
    me = "HappyMike@gmail.com"

    # Uncomment below to start execution of the program
    # processor(r, m, v, c, url, me)
