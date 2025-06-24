from pyannote.audio import Pipeline
import os

# Fixed configuration (modify these according to your setup)
# AUDIO_BASE_DIR = r"E:\Karya\Audio_outputs"  # From your file path example
AUDIO_EXTENSION = ".wav"  # Update if using different format

def diarize_audio(video_id,output_dir):
    """
    Perform speaker diarization on an audio file.

    Parameters:
    - file_path: Path to the audio file.
    """

    file_name = f"{video_id}{AUDIO_EXTENSION}"
    file_path = os.path.join(output_dir, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found for video ID {video_id} at {file_path}")
    
    hf_token = os.environ.get('HF_TOKEN')

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token  
    )

    try:
        diarization = pipeline(file_path)
        return diarization
        # Basic information
        # print(f"Total speakers: {len(diarization.labels())}")
        # print(f"Speech duration: {diarization.get_timeline().duration():.1f}s")
        # print(f"Speaker distribution:\n{diarization.chart()}")

        # # Detailed segment inspection
        # for segment, track, speaker in diarization.itertracks(yield_label=True):
        #     print(f"Speaker {speaker} spoke from {segment.start:.1f}s to {segment.end:.1f}s")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = "outputs/videoplayback.wav"
    diarize_audio(file_path)