#uses NumPy, sounddevice and soundfile packages to record audio
import sounddevice as sd
import soundfile as sf
import io
import os
import subprocess
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-file.json'
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import keyboard
#samplerate needs to be 44100 for google to accept it
samplerate = 44100  # Hertz
duration = 5  # seconds
filename = 'output.wav'
#need to be mono channel (1)


while True:
	
	
	print("You can now minimize the terminal script window and use F11 to make the program start listening or \nPress CTRL+C to exit the program \nHint: To say 'google-chrome-stable' say google dash chrome dash stable \nThis currently does not support commands with multiple words unless they're separated by a dash, slash or dot")


	print ("Press F11 to start listening")
	keyboard.add_hotkey('F11', print, args=['F11 was pressed!'])
	keyboard.wait('F11')

	recording = sd.rec(int(samplerate * duration), samplerate,
                channels=1, blocking=True)
	sf.write(filename, recording, samplerate)

	#initializes new client
	client = speech.SpeechClient()

	#gets the filepath of the filename
	file_name = os.path.dirname(filename)
 
	# Loads the audio into memory
	with io.open(filename, 'rb') as audio_file:
    		content = recording.read()
	audio = types.RecognitionAudio(content=content)

	config = types.RecognitionConfig(
  		encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    		sample_rate_hertz=samplerate,
   	 	language_code='en-US')

	# Detects speech in the audio file

	response = client.recognize(config, audio)

	#Debugging:
	for result in response.results:
    		print('What you said: {}'.format(result.alternatives[0].transcript))

#Execute what you said on the command line:
	subprocess.call(result.alternatives[0].transcript.lower().replace(" ", "").replace("dash","-").replace("dot.","."))
