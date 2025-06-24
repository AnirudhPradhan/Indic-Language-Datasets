import yt_dlp
import os
import csv
from googleapiclient.discovery import build
from dotenv import load_dotenv
load_dotenv()
import isodate

API_KEY = os.environ.get('YOUTUBE_API')  # Replace with your actual API key

def get_audio(video_id, output_folder, csv_file, language):
    """
    Downloads audio from a YouTube video and stores metadata in CSV files.
    Skips download if the audio file already exists.
    Args:
        video_id (str): YouTube video ID.
        output_folder (str): Folder to save the WAV file.
        csv_file1 (str): First CSV file to store metadata.
        csv_file2 (str): Second CSV file to store metadata.
        language (str): Language code for metadata extraction.
    """
    os.makedirs(output_folder, exist_ok=True)
    url = "https://www.youtube.com/watch?v=" + video_id

    wav_path = os.path.join(output_folder, f"{video_id}.wav")
    if os.path.exists(wav_path):
        print(f"Audio file already exists: {wav_path}")
        # Retrieve metadata using YouTube Data API
        metadata = get_video_information(video_id, language)
        # Write metadata to CSV files
        write_metadata_to_csv(metadata, csv_file)
        return

    # yt-dlp options for downloading audio, now with cookies.txt
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'noplaylist': True,
        'cookies': 'cookies.txt',  # This line enables cookies.txt usage
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"Downloaded and saved as WAV: {info['title']}")
            # Retrieve metadata using YouTube Data API
            metadata = get_video_information(video_id, language)
            # Write metadata to CSV files
            write_metadata_to_csv(metadata, csv_file)
    except Exception as e:
        print(f"Error: {e}")

def get_video_information(video_id,language):
    """
    Retrieves metadata of a YouTube video using the YouTube Data API.

    Args:
        video_id (str): ID of the YouTube video.

    Returns:
        dict: Metadata including video ID, title, channel ID, and published date.
    """
    youtube = build("youtube", "v3", developerKey=API_KEY)

    response = youtube.videos().list(
        part="contentDetails,snippet",
        id=video_id
    ).execute()

    if "items" in response and len(response["items"]) > 0:
        snippet = response["items"][0]["snippet"]
        duration = isodate.parse_duration(response['items'][0]['contentDetails']['duration']).total_seconds()
        # Fetch AI training status
        trainability_response = youtube.videoTrainability().get(
            id=video_id
        ).execute()

        # Extract trainability status
        ai_training_status_list = trainability_response.get('permitted', ['Unknown'])
        # if ai_training_status_list[0] == 'PERMITTED':
        #     ai_training_status = 'Permitted'
        # elif ai_training_status_list[0] == 'NOT_PERMITTED':
        #     ai_training_status = 'Not Permitted'
        # else:   
        #     ai_training_status = 'Unknown'

        return {
            "Video ID": video_id,
            "Title": snippet.get("title", ""),
            "Channel ID": snippet.get("channelId", ""),
            "Video Duration": duration,
            "Published Date": snippet.get("publishedAt", ""),
            "Language": language,
            "AI Training Status": ai_training_status_list[0] if ai_training_status_list else "Unknown",
        }
    else:
        return None

def write_metadata_to_csv(metadata, csv_file):
    fieldnames = [
        "Video ID",
        "Title",
        "Channel ID",
        "Video Duration",
        "Actual Speech Duration",
        "Published Date",
        "Language",
        "AI Training Status",
        "Number of Speakers",
        "Speaker Distribution",
        "Transcript"
    ]

    row = {field: metadata.get(field, "") for field in fieldnames}
    write_header = not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
        print(f"✅ Metadata saved to {csv_file}")

        
if __name__ == "_main_":
    url = "https://www.youtube.com/watch?v=bYGY1s6VMWs"
    output_folder = "audio_outputs"
    csv_file = "video_metadata.csv"

    get_audio(url, output_folder, csv_file)