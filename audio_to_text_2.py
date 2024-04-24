# The original Whisper model from OpenAI struggles with audio files larger than 25MB.

import whisper
import moviepy.editor as mp

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

def extract_audio_and_transcribe(video_path, output_filename="output.txt", model="base"):
  """
  Extracts audio from a video file, transcribes it using Whisper, and saves the transcript to a text file.

  Args:
      video_path: Path to the video file.
      output_filename: Name of the output text file. Defaults to "output.txt".
      model: Whisper model to use ("base", "small", or "large"). Defaults to "base".
  """
  video_clip = mp.VideoFileClip(video_path)
  audio_clip = video_clip.audio
  audio_clip.write_audiofile(f"extracted_audio.wav")

  transcript = transcribe_audio(f"extracted_audio.wav", model)

  # Save transcript to text file
  with open(output_filename, "w", encoding="utf-8") as f:
    f.write(transcript)

  # Clean up temporary audio file
  audio_clip.close()
  video_clip.close()

# Example usage
# Transcribe an audio file
#audio_path = "your_audio.mp3"
#transcript = transcribe_audio(audio_path)
#print(transcript)

# Extract audio from video and transcribe
video_path = "Vivir Programando tus Propios Productos.mp4"
extract_audio_and_transcribe(video_path)
print(f"Transcript saved to: output.txt")