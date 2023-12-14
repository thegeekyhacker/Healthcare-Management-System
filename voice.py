
import os
import platform

def text_to_speech(text):
    system_platform = platform.system()
    if system_platform == 'Darwin':  # For Mac
        os.system(f'say "{text}"')
    elif system_platform == 'Windows':  # For Windows
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        print("Text-to-speech not supported on this operating system.")

# text_to_speech("God")
