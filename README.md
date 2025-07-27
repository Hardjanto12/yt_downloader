# YouTube Downloader

A simple desktop application to download YouTube videos or audio in various formats and resolutions, built with Python, Tkinter, and yt-dlp.

## Features

- Download YouTube videos as video or audio files
- Choose from multiple formats (mp4, webm, mp3, m4a, etc.)
- Select resolution/quality for downloads
- Simple graphical user interface (GUI)
- Progress and status updates

## Requirements

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Installation

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd yt_download
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Paste the YouTube URL into the input field.
3. Select whether to download as Video or Audio.
4. Choose the desired format and resolution/quality.
5. Select the output folder.
6. Click "Download" to start downloading.

## Notes

- For audio downloads, common formats like mp3, m4a, wav, flac, aac, and opus are supported.
- For video downloads, you can select from available resolutions and formats.
- The application uses `yt-dlp` under the hood, so most YouTube links and many other sites supported by yt-dlp will work.

## License

This project is licensed under the MIT License.
