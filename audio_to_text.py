import whisper
import moviepy.editor as mp
import os
import sys
import logging
import pdb

"""
The goal of this script is recibe an audio or a video file and transform it to text. 

Instalation pip install whisper moviepy logging pdb

Example usage python process_file.py -f /path/to/your/file.mp3 -m advanced -o results.txt -c 60

This script defines default values for all arguments. 

It then iterates through provided arguments (excluding the script name) 
and assigns values to variables based on flags (-f, -m, -o, -c).
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# Define default values
default_model = "base"
default_output_filename = "output.txt"
default_chunk_size = 30

# Extract arguments from sys.argv
file_path = None
model = default_model
output_filename = default_output_filename
chunk_size = default_chunk_size

# Process arguments (excluding script name at index 0)
for i in range(1, len(sys.argv), 2):
  arg_name = sys.argv[i]
  if arg_name not in ["-f", "-m", "-o", "-c"]:
    print(f"Invalid argument: {arg_name}")
    exit(1)

  value = sys.argv[i + 1]
  if arg_name == "-f":
    file_path = value
  elif arg_name == "-m":
    model = value
  elif arg_name == "-o":
    output_filename = value
  elif arg_name == "-c":
    try:
      chunk_size = int(value)
      if chunk_size <= 0:
        print("Chunk size must be a positive integer")
        exit(1)
    except ValueError:
      print("Chunk size must be a number")
      exit(1)

# Check if required argument (-f) is missing
if not file_path:
  print("Missing required argument: -f (file path)")
  exit(1)

# Print confirmation message with provided options
print(f"""
Summary of options:
  File Path: {file_path}
  Model: {model}
  Output Filename: {output_filename}
  Chunk Size: {chunk_size}
""")


def transcribe_audio(audio_path, model="base"):
  """
  Transcribes an audio file using Whisper.

  Args:
      audio_path: Path to the audio file.
      model: Whisper model to use ("base", "small", or "large"). Defaults to "base".

  Returns:
      The transcribed text.
  """
  model = whisper.load_model(model)
  result = model.transcribe(audio_path)
  return result["text"]

def split_audio(audio_path, chunk_size):
  """
  Splits an audio file into chunks of the specified size.
  
  Args:
      audio_path: Path to the audio file.
      chunk_size: Size of each chunk in seconds.
  """
  
  try:
      video_clip = mp.VideoFileClip(audio_path)
      audio_clip = video_clip.audio
  except:
      audio_clip = mp.AudioFileClip(audio_path)
      
  total_duration = audio_clip.duration
  #pdb.set_trace()
  num_chunks = int(total_duration / chunk_size) + 1
  
  print("Making Chunks")
  for i in range(num_chunks):
    start_time = i * chunk_size
    end_time = min((i + 1) * chunk_size, total_duration)
    chunk_clip = audio_clip.subclip(start_time, end_time)
    if i == 0:
        print("Duration of each Chunks: ", chunk_clip.duration, 's')
    chunk_clip.write_audiofile(f"chunk_{i}.wav", write_logfile=False, verbose=False, logger=None) #Logger='bar'

  # Clean up video clip
  try:
      video_clip.close()
  except:
     pass

def extract_audio_and_transcribe(video_path, output_filename="output.txt", model="base", chunk_size=30):
  """
  Extracts audio from a video file, splits it into chunks, transcribes each chunk using Whisper,
  and saves the combined transcript to a text file.

  Args:
      video_path: Path to the video file.
      output_filename: Name of the output text file. Defaults to "output.txt".
      model: Whisper model to use ("base", "small", or "large"). Defaults to "base".
      chunk_size: Size of each audio chunk in seconds. Defaults to 30.
  """
  # Split audio into chunks
  split_audio(video_path, chunk_size)

  # Combine transcripts
  transcript = ""
  for i in range(int(mp.AudioFileClip(video_path).duration / chunk_size) + 1):
    chunk_transcript = transcribe_audio(f"chunk_{i}.wav", model)
    transcript += chunk_transcript

  # Save transcript to text file
  print(f'Writing transcript in {output_filename}')  
  with open(output_filename, "w", encoding="utf-8") as f:
    f.write(transcript)

  # Clean up temporary audio files (implement logic to remove chunk files)
  # Clean up temporary audio files
  print("Removing temporal Chunks")
  for i in range(int(mp.AudioFileClip(video_path).duration / chunk_size) + 1):
    os.remove(f"chunk_{i}.wav")  # Remove each chunk file

if __name__ == '__main__':
  
    print("** Processing the file... **")
    # Assuming the lecture video is in lectures/lecture1.mp4
    
    extract_audio_and_transcribe(file_path, output_filename, model, chunk_size)
    #extract_audio_and_transcribe("extracted_audio.wav", "Vivir Programando tus Propios Productos 2.txt", chunk_size=60)
    print("** Processing completed. **")