import pyttsx3
import speech_recognition as sr
from datetime import datetime as dt
import pywhatkit
import wikipedia
import webbrowser

# Global Setting
debug = True
silent_mode = False
speaker_name = "David"  # default speaker
speed = 210
# gender = "Female"

# Global variables
speaker_name_list = ["david", "zira", "haruka"]
jarvis_end_msg = "See you again Nam ... "
jarvis_ear = sr.Recognizer()
jarvis_mouth = pyttsx3.init()
jarvis_brain = ""

# Constant
weather_api_key = "c7be0a5bd2f32b93384a8c67f65888c0"
football_schedule_url = "https://www.24h.com.vn/bong-da/lich-thi-dau-bong-da-hom-nay-moi-nhat-c48a364371.html"
football_stream_url = "https://90p.live/"
github_url = "https://github.com/ndnam198?tab=repositories"
# Fucntions
def setSpeed(voice_speed):
	jarvis_mouth.setProperty('rate', voice_speed)


def setSpeaker(name):
	new_name = name.capitalize()
	global speaker_name
	voices = jarvis_mouth.getProperty('voices')
	for voice in voices:
		if new_name in voice.name:
			jarvis_mouth.setProperty('voice', voice.id)
			print("Speaker name: " + new_name)
			speaker_name = new_name
			break
	return speaker_name


def jarvisTalk(audio):
	global debug
	if len(audio) != 0:
		if debug == True:
			print(speaker_name + ": " + audio)
		jarvis_mouth.say(audio)
		jarvis_mouth.runAndWait()
	return audio


def jarvisListen():
	# Open mic for speech recognition
	global debug
	global silent_mode
	with sr.Microphone() as mic:
		if silent_mode == True:
			print("\n" + speaker_name + ": Silent mode is ON")
		else:
			print("\n" + speaker_name + ": I'm listenning ...")
		audio = jarvis_ear.listen(mic)
	try:
		# change your speech into text
		your_command = jarvis_ear.recognize_google(audio)
	except:
		your_command = ""
		# Turn speech text to lower text
	if debug == True:
		if (len(your_command) != 0) and (silent_mode == False):
			print("You: " + your_command)
	return your_command


def jarvisExecute(command):
	# jarvis reaction based on your speech's text
	# Time
	if len(command) == 0:
		return -1
	global silent_mode
	if silent_mode == False:
		# Change speaker
		for name in speaker_name_list:
			if name in command:
				setSpeaker(name)
				jarvisTalk("New speaker has been assigned")
				return
		# Ask for date
		if "today" in command:
			today = dt.today()
			jarvis_brain = "Today is " + today.strftime("%B %d, %Y")
		elif "time" in command:
			now = dt.now()
			jarvis_brain = "Current time is " + now.strftime("%I:%M %p")
		# Open football schedule
		elif "football schedule" in command:
			webbrowser.open(football_schedule_url)
			jarvis_brain = "Openning football schedule site"
		# Open football stream site 90p.link
		elif "football live" in command:
			webbrowser.open(football_stream_url)
			jarvis_brain = "Openning football stream site"
		# Play music    
		elif "play" in command:
			song = command.replace("play", "")
			jarvis_brain = "Playing " + song
			pywhatkit.playonyt(song)
		# Search on Internet
		elif "search" in command:
			terminology = command.replace("search", "")
			jarvis_brain = "Searching for" + terminology
			pywhatkit.search(terminology)
		# Get a short description for a terminology
		elif "wikipedia" in command:
			terminology = command.replace("wikipedia", "")
			jarvisTalk("Searching for" + terminology)
			jarvis_brain = wikipedia.summary(terminology, 1)
		elif "my github" in command:
			webbrowser.open(github_url)
			jarvis_brain = "Openning your github repositories"
		elif "weather" in command:
			#TODO add weather funciton
			pass
		# Stop virtual assistance
		elif "goodbye" in command:
			jarvis_brain = jarvis_end_msg
		# Enter silent mode - cannot receive any command except switching back to normal mode
		elif "silent mode" in command:
			silent_mode = True
			jarvis_brain = "Silent mode is ON"
		else:
			jarvis_brain = "I can't hear you, repeat your command please"
	elif silent_mode == True:
		if ("normal mode" in command) or ("off silent mode" in command) or ("disable silent mode" in command):
			silent_mode = False
			jarvis_brain = "Silent mode is OFF"
		else:
			jarvis_brain = "Disable silent mode first"
	jarvisTalk(jarvis_brain)
	return jarvis_brain


def main():
	print("Main function")
	setSpeed(speed)
	setSpeaker(speaker_name)
	jarvisTalk("Welcome back Captain !!! How can I help you sir ?")
	while True:
		you = jarvisListen().lower()
		jarvis_brain = jarvisExecute(you)
		if jarvis_brain == jarvis_end_msg:
			break


if __name__ == '__main__':
	try:
		main()
	except Exception as bug:
		print(bug)

