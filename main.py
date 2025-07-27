import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        self.create_widgets()

    def create_widgets(self):
        # URL Input
        url_label = tk.Label(self.root, text="YouTube URL:")
        url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # Format Type Selection (Video/Audio)
        format_type_label = tk.Label(self.root, text="Download As:")
        format_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.format_type_combobox = ttk.Combobox(self.root, values=["Video", "Audio"], state="readonly")
        self.format_type_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.format_type_combobox.set("Video") # Default to Video
        self.format_type_combobox.bind("<<ComboboxSelected>>", self.update_format_combobox)

        # Format Selection (mp4, webm, mp3, m4a, etc.)
        format_label = tk.Label(self.root, text="Format:")
        format_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.format_combobox = ttk.Combobox(self.root, state="readonly")
        self.format_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.format_combobox["values"] = []
        self.format_combobox.bind("<<ComboboxSelected>>", self.update_resolution_options)

        # Resolution/Quality Selection
        resolution_label = tk.Label(self.root, text="Resolution/Quality:")
        resolution_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.resolution_combobox = ttk.Combobox(self.root, state="readonly")
        self.resolution_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        self.resolution_combobox["values"] = []
        self.url_entry.bind("<FocusOut>", self.fetch_media_info)
        self.url_entry.bind("<Return>", self.fetch_media_info)

        # Output Folder
        output_label = tk.Label(self.root, text="Output Folder:")
        output_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = tk.Entry(self.root, width=50)
        self.output_entry.grid(row=4, column=1, padx=10, pady=10)
        self.output_button = tk.Button(self.root, text="Browse", command=self.browse_output_folder)
        self.output_button.grid(row=4, column=2, padx=10, pady=10)

        # Download Button
        self.download_button = tk.Button(self.root, text="Download", command=self.start_download_thread)
        self.download_button.grid(row=5, column=1, pady=20)

        # Status/Progress
        self.status_text = tk.Text(self.root, height=10, width=60, state="disabled")
        self.status_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def log_message(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

    def fetch_media_info(self, event=None):
        url = self.url_entry.get()
        if not url:
            self.format_combobox["values"] = []
            self.resolution_combobox["values"] = []
            return

        self.log_message("Fetching media information...")
        try:
            ydl_opts = {'quiet': True, 'simulate': True, 'force_generic_extractor': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])

                self.available_formats = {
                    "Video": {},
                    "Audio": {}
                }

                for f in formats:
                    ext = f.get('ext')
                    if not ext: continue

                    # Video formats
                    if f.get('vcodec') != 'none':
                        if ext not in self.available_formats["Video"]:
                            self.available_formats["Video"][ext] = set()
                        if f.get('height'):
                            self.available_formats["Video"][ext].add(f'{f["height"]}p')
                        elif f.get('format_note'):
                            self.available_formats["Video"][ext].add(f['format_note'])

                    # Audio formats
                # For audio, we offer common output formats that yt-dlp can convert to
                common_audio_formats = ["mp3", "m4a", "wav", "flac", "aac", "opus"]
                for audio_ext in common_audio_formats:
                    if audio_ext not in self.available_formats["Audio"]:
                        self.available_formats["Audio"][audio_ext] = set()
                    # For audio quality, we can offer common bitrates or just 'best'
                    self.available_formats["Audio"][audio_ext].add('best')
                    self.available_formats["Audio"][audio_ext].add('320k')
                    self.available_formats["Audio"][audio_ext].add('256k')
                    self.available_formats["Audio"][audio_ext].add('192k')
                    self.available_formats["Audio"][audio_ext].add('128k')

                # Sort resolutions/qualities for each format
                for type_key in self.available_formats:
                    for ext_key in self.available_formats[type_key]:
                        if type_key == "Video":
                            self.available_formats[type_key][ext_key] = sorted(list(self.available_formats[type_key][ext_key]), key=lambda x: int(x[:-1]) if x.endswith('p') else 0, reverse=True)
                        elif type_key == "Audio":
                            self.available_formats[type_key][ext_key] = sorted(list(self.available_formats[type_key][ext_key]), key=lambda x: int(x[:-1]) if x.endswith('k') else 0, reverse=True)

                self.update_format_combobox()
                self.log_message("Media information fetched.")
        except Exception as e:
            self.log_message(f"Error fetching media information: {e}")
            self.format_combobox["values"] = []
            self.resolution_combobox["values"] = []

    def update_format_combobox(self, event=None):
        format_type = self.format_type_combobox.get()
        if format_type in self.available_formats:
            formats = sorted(list(self.available_formats[format_type].keys()))
            self.format_combobox["values"] = formats
            if formats:
                self.format_combobox.set(formats[0])
            else:
                self.format_combobox.set("")
        else:
            self.format_combobox["values"] = []
            self.format_combobox.set("")
        self.update_resolution_options() # Update resolutions after format type or format changes

    def update_resolution_options(self, event=None):
        format_type = self.format_type_combobox.get()
        selected_format = self.format_combobox.get()

        if format_type in self.available_formats and selected_format in self.available_formats[format_type]:
            resolutions = self.available_formats[format_type][selected_format]
            self.resolution_combobox["values"] = resolutions
            if resolutions:
                self.resolution_combobox.set(resolutions[0])
            else:
                self.resolution_combobox.set("")
        else:
            self.resolution_combobox["values"] = []
            self.resolution_combobox.set("")

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_selected)

    def start_download_thread(self):
        download_thread = threading.Thread(target=self.download_video)
        download_thread.start()

    def download_video(self):
        url = self.url_entry.get()
        resolution = self.resolution_combobox.get()
        output_path = self.output_entry.get()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        if not resolution:
            messagebox.showerror("Error", "Please select a resolution.")
            return
        if not output_path:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        self.log_message(f"Starting download for {url} at {resolution}...")
        self.download_button.config(state="disabled")

        try:
            format_type = self.format_type_combobox.get()
            selected_format = self.format_combobox.get()
            selected_resolution = self.resolution_combobox.get()

            ydl_opts = {
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'postprocessors': [],
            }

            if format_type == "Video":
                # For video, we want to download the best video stream at the selected resolution
                # and the best audio stream, then merge them.
                if selected_resolution.endswith('p'):
                    ydl_opts['format'] = f'bestvideo[ext={selected_format}][height<={selected_resolution[:-1]}] + bestaudio[ext=m4a]/best[ext={selected_format}]'
                else:
                    # Fallback for cases where resolution is not 'p' (e.g., format_note)
                    ydl_opts['format'] = f'bestvideo[ext={selected_format}] + bestaudio[ext=m4a]/best[ext={selected_format}]'

            elif format_type == "Audio":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': selected_format,
                    'preferredquality': selected_resolution.replace('k', '') if selected_resolution.endswith('k') else '192',
                })
                ydl_opts['outtmpl'] = f'{output_path}/%(title)s.{selected_format}'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log_message("Download complete!")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            self.log_message(f"Download failed: {e}")
            messagebox.showerror("Error", f"Download failed: {e}")
        finally:
            self.download_button.config(state="normal")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            filename = d.get('filename', 'Unknown')
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)

            if total_bytes > 0:
                percent = downloaded_bytes / total_bytes * 100
                self.log_message(f"Downloading: {filename} - {percent:.1f}%")
            else:
                self.log_message(f"Downloading: {filename} - {downloaded_bytes / (1024*1024):.2f}MB")
        elif d['status'] == 'finished':
            self.log_message(f"Finished downloading: {d['filename']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
