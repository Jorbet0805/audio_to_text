# Dependencias 
# pip install speechrecognition pydub

import speech_recognition as sr
from pydub import AudioSegment
import moviepy.editor as mp

def transcribe_chunk(audio_file, chunk_start, chunk_end):
  """Transcribes a chunk of audio file."""
  # Open audio file with Pydub
  sound = AudioSegment.from_mp3(audio_file)  # Change to your audio format

  # Extract the chunk
  chunk = sound[chunk_start:chunk_end]

  # Save the chunk to a temporary file
  chunk_file = "chunk.wav"
  chunk.export(chunk_file, format="wav")

  # Use SpeechRecognition to transcribe the chunk
  recognizer = sr.Recognizer()
  with sr.AudioFile(chunk_file) as source:
    audio = recognizer.record(source)
  try:
    text = recognizer.recognize_google(audio)
  except sr.UnknownValueError:
    print("Could not understand audio")
    text = ""
  finally:
    # Remove temporary file
    import os
    os.remove(chunk_file)
  return text

def transcribe_audio(audio_file, chunk_length_ms=10000):
  """Transcribes a long audio file by splitting it into chunks."""

  # Get audio duration in milliseconds
  sound = AudioSegment.from_mp3(audio_file)  # Change to your audio format
  audio_duration_ms = sound.duration_seconds * 1000

  # Initialize variables
  transcript = ""
  chunk_start = 0

  while chunk_start < audio_duration_ms:
    # Define chunk end (adjusted for not exceeding audio duration) 
    chunk_end = min(chunk_start + chunk_length_ms, audio_duration_ms)

    # Transcribe the chunk and append to transcript
    chunk_text = transcribe_chunk(audio_file, chunk_start, chunk_end)
    transcript += chunk_text + " "

    # Update chunk start for next iteration
    chunk_start += chunk_length_ms

  return transcript


def extract_and_transcribe(video_file, chunk_length_ms=10000):
    """Extracts audio from a video and transcribes it."""

    # Extract audio from video
    video_clip = mp.VideoFileClip(video_file)
    video_clip.audio.write_audiofile("extracted_audio.wav")  # Change format if needed

    # Transcribe the extracted audio
    audio_file = "extracted_audio.wav"
    text = transcribe_audio(audio_file, chunk_length_ms)

    # Remove temporary audio file
    import os
    os.remove(audio_file)

    return text

# Example audio of video to text
video_filepath = "Vivir Programando tus Propios Productos.mp4"  # Replace with your video path
text = extract_and_transcribe(video_filepath)
print(text)


# Example of audio to text
#audio_filepath = "path/to/your/audio.mp3"  # Replace with your audio path
#text = transcribe_audio(audio_filepath)
#print(text)