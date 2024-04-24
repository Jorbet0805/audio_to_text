1. Script Overview

This Python script, audio_to_text.py, utilizes the Whisper library to transcribe audio or video files into text. It supports processing both audio (.mp3, .wav) and video (.mp4) formats.

2. Installation

The script requires the following external libraries:

whisper
moviepy

These libraries can be installed using pip:

Bash
pip install whisper moviepy 

Usa el código con precaución.

3. Usage

The script is executed from the command line using the following syntax:

Bash
python audio_to_text.py -f /path/to/your/file.mp4 -m base -o results.txt -c 60

Usa el código con precaución.

4. Arguments

-f (required): Path to the audio or video file.
-m (optional): Whisper model to use ("base", "small", or "large"). Defaults to "base".
-o (optional): Name of the output text file. Defaults to "output.txt".
-c (optional): Size of each audio chunk in seconds when processing videos. Defaults to 30.

5. Script Functionality

The script first defines default values for all arguments.
It then parses the command-line arguments, validating their format and assigning values to corresponding variables.
It checks for the presence of the required argument (-f) and exits with an error message if missing.
The script provides a confirmation message summarizing the chosen options.

The core functionalities are implemented in three functions:

transcribe_audio(audio_path, model="base"): Transcribes a single audio file using Whisper.
split_audio(audio_path, chunk_size): Splits an audio file (extracted from video) into chunks of the specified size.
extract_audio_and_transcribe(video_path, output_filename="output.txt", model="base", chunk_size=30): This is the main function that orchestrates the entire process. It first extracts audio from the video, splits it into chunks, transcribes each chunk using the transcribe_audio function, combines the transcripts, and finally saves the combined transcript to a text file. It also handles cleaning up temporary audio files generated during processing.
The __main__ block serves as the entry point when the script is executed directly. It calls the extract_audio_and_transcribe function with the parsed arguments (or default values if not provided).

6. Error Handling

The script implements basic error handling mechanisms:

It validates the format of command-line arguments and exits with informative messages in case of errors.
It checks for the existence of the input file (-f) and exits with an error message if not found.

7. Logging

Currently, the script uses the logging library but is configured with a logging level of WARNING. You can modify this behavior to enable logging of informational messages by changing the logging level in the logger.setLevel() line.

8. Limitations

The script assumes the temporary chunk files generated during video processing can be removed based on their filenames (chunk_*.wav). A more robust approach would be to implement logic to handle unexpected file naming scenarios.

I hope this comprehensive documentation clarifies the functionality and usage of the audio_to_text.py script.