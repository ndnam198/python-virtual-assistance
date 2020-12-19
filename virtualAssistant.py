# ------------------------------- Import Module ------------------------------ #
import os
import webbrowser
from googlesearch import search
from datetime import datetime as dt
import re

import pyttsx3
import pywhatkit
import speech_recognition as sr
import wikipedia
import keyboard

# Global Setting
debug = True
silent_mode = False
speaker_name = "Zira"  # default speaker
speed = 210
 
# ----------------------------- Global variables ----------------------------- #
speaker_name_list = ["david", "zira", "haruka"]
assistant_ear = sr.Recognizer()
assistant_mouth = pyttsx3.init()
assistant_brain = ""

# ------------------------------------ URL ----------------------------------- #
weather_api_key = "c7be0a5bd2f32b93384a8c67f65888c0"
football_schedule_url = "https://www.24h.com.vn/bong-da/lich-thi-dau-bong-da-hom-nay-moi-nhat-c48a364371.html"
football_stream_url = "https://90p.live/"
github_url = "https://github.com/ndnam198?tab=repositories"
nihon_url = "https://kantan.vn/kanji.htm"

lol_path = "D:\\Apps\\Garena\\Garena\\Garena\\Garena.exe"
pes_path = "D:\\Games\\PES2019\\New folder\\Pro Evolution Soccer 2019\\PES2019.exe"
# Fucntions

# ------------------------- Print supporting command ------------------------- #
def printCommand():
	print("\
 _____________________________________________________________________________________________________\n\
| Function                 | Description                                                              |\n\
|--------------------------|--------------------------------------------------------------------------|\n\
| Recuit another assistant | Assign another among David(default), Zira, Haruka to be ur new assistant |\n\
| [Silent mode]            | Put the assistant into silent mode: Stop serving                         |\n\
| [Normal mode]            | Disable silent mode                                                      |\n\
| Ask about [date]         | Query the date ìnormation                                                |\n\
| Ask about [time]         | Query the time ìnormation                                                |\n\
| View [Football schedule] | Open football schedule                                                   |\n\
| Watch [Football live]    | Open football stream site                                                |\n\
| Browse [Github]          | Open Github                                                              |\n\
| [Play] specific music    | Play a music video on youtube, song's name included in speech            |\n\
| [Search] for something   | Proceed searching for ur provided terminology                            |\n\
| [Open] specific site     | Open a specific URL based on search results                              |\n\
| [Wiki] something         | Get a short speech description of anything                               |\n\
| Hibernate computer       | Put ur computer into hibernate to save power without losing ur workspace |\n\
| Stop assistant           | Stop assistant by saying [goodbye]                                       |\n\
 -----------------------------------------------------------------------------------------------------\n")


	return

def setSpeed(voice_speed):
	assistant_mouth.setProperty('rate', voice_speed)


def setSpeaker(name):
	new_name = name.capitalize()
	global speaker_name
	voices = assistant_mouth.getProperty('voices')
	for voice in voices:
		if new_name in voice.name:
			assistant_mouth.setProperty('voice', voice.id)
			print("Speaker name: " + new_name)
			speaker_name = new_name
			break
	return speaker_name


def assistantTalk(audio):
	global debug
	if len(audio) != 0:
		if debug == True:
			print(speaker_name + ": " + audio)
		assistant_mouth.say(audio)
		assistant_mouth.runAndWait()
	return audio


def assistantListen():
	# Open mic for speech recognition
	global debug
	global silent_mode
	with sr.Microphone() as mic:
		if silent_mode == True:
			print("\n" + speaker_name + ": Silent mode is ON")
		else:
			print("\n" + speaker_name + ": I'm listenning ...")
		audio = assistant_ear.listen(mic)
	try:
		# change your speech into text
		your_command = assistant_ear.recognize_google(audio)
	except:
		your_command = ""
		# Turn speech text to lower text
	if debug == True:
		if (len(your_command) != 0) and (silent_mode == False):
			print("You: " + your_command)
	return your_command


def assistantExecute(command):
	global assistant_brain
	match = 0
	# assistant reaction based on your speech's text
	# Time
	if len(command) == 0:
		return -1
	global silent_mode
	if silent_mode == False:

# ---------------------- Real time configure assistant ---------------------- #

		# Change speaker
		for name in speaker_name_list:
			if name in command:
				setSpeaker(name)
				assistantTalk("New speaker has been assigned")
				match+=1
				return

		# Enter silent mode - cannot receive any command except switching back to normal mode
		if "on silent mode" in command:
			silent_mode = True
			assistant_brain = "Silent mode is ON"
			match+=1

# ------------------------ Browse general information ------------------------ #

		# Ask for date
		elif "today" in command:
			today = dt.today()
			assistant_brain = "Today is " + today.strftime("%B %d, %Y")
			match+=1

		# Ask for clock
		elif "time" in command:
			now = dt.now()
			assistant_brain = "Current time is " + now.strftime("%I:%M:%S %p")
			match+=1

		elif "set alarm" in command:
			alarm_hour_list = re.findall(r'\d+', command)
			hour = int(alarm_hour_list[0])
			if (len(alarm_hour_list) == 2):
				minute = int(alarm_hour_list[1])
			else:
				minute = 0
			second = 0
			if "p.m" in command:
				hour += 12
			assistant_brain = "Setting your alarm at {:02d}:{:02d}:{:02d}".format(hour, minute, second)
			os.system("start /b python alarm.py {:02d} {:02d} {:02d}".format(hour, minute, second))
			match+=1

		elif "weather" in command:
			match+=1
			#TODO add weather funciton

# ----------------------------- Browse specific URL ---------------------------- #

		# Open football schedule
		elif "football schedule" in command:
			webbrowser.open(football_schedule_url)
			assistant_brain = "Openning football schedule site"
			match+=1

		# Open football stream site 90p.link
		elif "football live" in command:
			webbrowser.open(football_stream_url)
			assistant_brain = "Openning football stream site"
			match+=1

		# Open github
		alike_phrase = ["github", "get up"]
		if any(x in command for x in alike_phrase):
			webbrowser.open(github_url)
			assistant_brain = "Openning your github repositories"
			match+=1

		# Setup workspace for learning Nihongo
		alike_phrase = ["learn japanese","learn nihongo"]
		if any(x in command for x in alike_phrase):
			webbrowser.open(nihon_url)
			assistant_brain = "Setup workspace for learning Japanese"
			match += 1
			
		elif "league of legends" in command:
			assistant_brain = "Openning League of Legends. Have fun"
			match += 1
			try:
				os.startfile(lol_path)
			except Exception:
				assistantTalk("File's not found")
			pass

		alike_phrase = ["path","pes","pass"]
		if any(x in command for x in alike_phrase):
			assistant_brain = "Openning Pro Evolution Soccer 2019. Have fun"
			match += 1
			try:
				os.startfile(pes_path)
			except Exception:
				assistantTalk("File's not found")
				pass

# ------------------ Open site relative to keyword in speech ----------------- #

		# Play music    
		elif "play" in command:
			song = command.replace("play", "")
			assistant_brain = "Playing " + song
			pywhatkit.playonyt(song)
			match+=1
			
		# Search on Internet
		elif "search" in command:
			search_term = command.replace("search", "")
			assistant_brain = "Searching for" + search_term
			pywhatkit.search(search_term)
			match+=1
		
		# Open relative site mentioned
		alike_phrase = ["open","browse"]
		if any(x in command for x in alike_phrase):
			site_name = []
			site_name = command.replace("open", "").replace("browse", "")
			assistant_brain = "Openning" + site_name
			url = search(site_name, num_results=3, lang="en")[0]
			webbrowser.open_new_tab(url)
			match+=1
				

		# Get a short description for a terminology
		alike_phrase = ["wiki","wikipedia"]
		if any(x in command for x in alike_phrase):
			wiki_term = command.replace("wikipedia", "").replace("wiki", "")
			assistantTalk("Searching for" + wiki_term + "definition")
			assistant_brain = wikipedia.summary(wiki_term, 1)
			match+=1
			
		
# ----------------------------- Control computer ----------------------------- #

		# Stop virtual assistant
		alike_phrase = ["goodbye","you are fired"]
		if any(x in command for x in alike_phrase):
			assistantTalk("See you again Nam ... ")
			match += 1
			keyboard.remove_hotkey(printCommand)
			os._exit(0)

		# Hibernate my computer
		elif ("computer" in command) and ("sleep" in command):
			assistantTalk("Putting computer into sleep mode")
			match+=1
			os.system("rundll32.exe powrprof.dll,SetSuspendState Hibernate")

		elif match == 0:
			assistant_brain = "I can't hear you, repeat your command please"

	elif silent_mode == True:
		alike_phrase = ["normal mode","off silent mode", "disable silent mode"]
		if any(x in command for x in alike_phrase):
			silent_mode = False
			assistant_brain = "Silent mode is OFF"
			match+=1
		else:
			assistant_brain = "Silent mode is ON: Service unvailable"

	assistantTalk(assistant_brain)
	return match


def main():
	print("Main function")
	rm = keyboard.add_hotkey('1', printCommand)
	setSpeed(speed)
	setSpeaker(speaker_name)
	assistantTalk("Welcome back Captain !!! How can I help you sir ?")
	while True:
		you = assistantListen().lower()
		assistantExecute(you)


if __name__ == '__main__':
	try:
		main()
	except Exception as bug:
		print(bug)

