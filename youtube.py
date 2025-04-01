import os
import pytube
from pytube import YouTube
from datetime import datetime

def download_youtube_video(url, output_dir='youtube_videos'):
    """Download a YouTube video"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        yt = YouTube(url)
        
        stream = yt.streams.get_highest_resolution()
        
        title = ''.join(c if c.isalnum() or c in ' -_' else '' for c in yt.title)
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"{timestamp}_{title}.mp4"
        
        print(f"Downloading: {yt.title}...")
        stream.download(output_path=output_dir, filename=filename)
        
        print(f"Successfully downloaded: {filename}")
        return os.path.join(output_dir, filename)
    
    except pytube.exceptions.PytubeError as e:
        print(f"Failed to download video: {str(e)}")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    download_youtube_video(url)
