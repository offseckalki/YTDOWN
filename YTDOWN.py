from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        
        # Display available stream options
        streams = yt.streams.filter(progressive=True)
        print("Available video qualities:")
        for i, stream in enumerate(streams, start=1):
            print(f"{i}. {stream.resolution} ({stream.mime_type})")

        # Prompt user to choose a quality
        choice = input("Enter the number corresponding to the desired video quality: ")
        selected_stream = streams[int(choice) - 1]

        # Download selected video stream
        selected_stream.download(output_path)
        print("Download completed!")
    except Exception as e:
        print(f"Error: {e}")

def convert_youtube_to_audio(video_url, output_format='mp3'):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Download audio stream and save to a temporary file
        temp_file_path = audio_stream.download()

        # Load audio file using moviepy
        audio_clip = AudioFileClip(temp_file_path)

        # Define output filename based on video title
        output_filename = f"{yt.title}.{output_format}"
        output_path = output_filename.replace('.mp4', f'.{output_format}')

        # Export audio file to desired format
        audio_clip.write_audiofile(output_path)

        print(f"Conversion to {output_format} completed! Saved as: {output_path}")

        # Clean up temporary file
        os.remove(temp_file_path)
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        print("\nWelcome to the Youtube Video Downloader and Converter!:")
        print("\nMenu:")
        print("1. Download YouTube Video")
        print("2. Convert YouTube Video to MP3")
        print("3. Convert YouTube Video to WAV(Highest Quality Possible!😎)")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            video_url = input("Enter YouTube video URL: ")
            output_path = input("Enter download location: ")
            download_video(video_url, output_path)
        elif choice == '2':
            video_url = input("Enter YouTube video URL: ")
            convert_youtube_to_audio(video_url, output_format='mp3')
        elif choice == '3':
            video_url = input("Enter YouTube video URL: ")
            convert_youtube_to_audio(video_url, output_format='wav')
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
