import tkinter as tk
from tkinter import messagebox
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
        choice = int(input("Enter the number corresponding to the desired video quality: "))
        selected_stream = streams[choice - 1]

        # Download selected video stream
        selected_stream.download(output_path)
        messagebox.showinfo("Download Complete", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

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

        messagebox.showinfo("Conversion Complete", f"Conversion to {output_format} completed! Saved as: {output_path}")

        # Clean up temporary file
        os.remove(temp_file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def handle_action(action, video_url, output_path):
    if action == 'Download':
        download_video(video_url, output_path)
    elif action == 'Convert to MP3':
        convert_youtube_to_audio(video_url, output_format='mp3')
    elif action == 'Convert to WAV':
        convert_youtube_to_audio(video_url, output_format='wav')

def on_submit():
    video_url = entry_url.get()
    output_path = entry_output.get()
    action = variable_action.get()

    if not video_url or not output_path:
        messagebox.showwarning("Warning", "Please provide both video URL and output path.")
        return

    handle_action(action, video_url, output_path)

# Create GUI window
window = tk.Tk()
window.title("YouTube Video Downloader & Converter")

# Video URL entry
label_url = tk.Label(window, text="YouTube Video URL:")
label_url.pack()
entry_url = tk.Entry(window, width=50)
entry_url.pack()

# Output path entry
label_output = tk.Label(window, text="Output Path:")
label_output.pack()
entry_output = tk.Entry(window, width=50)
entry_output.pack()

# Action selection (Download, Convert to MP3, Convert to WAV)
actions = ['Download', 'Convert to MP3', 'Convert to WAV']
variable_action = tk.StringVar(window)
variable_action.set(actions[0])
option_menu = tk.OptionMenu(window, variable_action, *actions)
option_menu.pack()

# Submit button
button_submit = tk.Button(window, text="Submit", command=on_submit)
button_submit.pack()

# Start GUI event loop
window.mainloop()
