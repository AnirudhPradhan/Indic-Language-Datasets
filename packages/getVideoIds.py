import os
from googleapiclient.discovery import build

API_KEY = os.environ.get('YOUTUBE_API')  # Replace with your actual API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_channel_ids(search_query):
    """
    Fetches channel IDs and titles for the given search query.
    """
    search_response = youtube.search().list(
        q=search_query,
        part='id,snippet',
        maxResults=10,
        type='channel'
    ).execute()

    channels = []
    for item in search_response.get('items', []):
        channel_id = item['id']['channelId']
        channel_title = item['snippet']['title']
        channels.append({'id': channel_id, 'title': channel_title})
    return channels

def get_video_ids(channel_id, limit):
    """
    Returns a list of YouTube video IDs for the given channel ID.
    """
    # Get the uploads playlist ID
    channel_response = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()
    
    if not channel_response['items']:
        raise ValueError(f"No channel found with ID: {channel_id}")
    
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    video_ids = []
    next_page_token = None
    
    while len(video_ids) < limit:
        playlist_items_response = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='contentDetails',
            maxResults=30,  # Max is 50
            pageToken=next_page_token
        ).execute()
        
        video_ids += [item['contentDetails']['videoId'] for item in playlist_items_response['items']]
        
        next_page_token = playlist_items_response.get('nextPageToken')
        if not next_page_token:
            break
    
    return video_ids[:limit]

def main():
    # Get channel IDs for the search query
    channels = get_channel_ids("comedy videos")
    
    print(f"Found {len(channels)} channels for query comedy videos:")
    for channel in channels:
        print(f"Channel ID: {channel['id']}, Title: {channel['title']}")
    
    # Fetch video IDs for the first channel as an example
    if channels:
        first_channel_id = channels[0]['id']
        print(f"\nFetching video IDs for channel: {channels[0]['title']} (ID: {first_channel_id})")
        video_ids = get_video_ids(first_channel_id, limit=10)
        print(f"Video IDs: {video_ids}")

if __name__ == "__main__":
    main()
