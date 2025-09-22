import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
import yt_dlp
import webbrowser

root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("550x300")
root.configure(bg="#1e1e2f")

# ---------- UI ----------
title_label = tk.Label(root, text="YouTube Downloader",
                       font=("Segoe UI", 16, "bold"), bg="#1e1e2f", fg="white")
title_label.pack(pady=10)

url_entry = tk.Entry(root, width=60, font=("Segoe UI", 12))
url_entry.pack(pady=5)

# Combobox برای انتخاب کیفیت
format_var = tk.StringVar()
format_box = ttk.Combobox(root, textvariable=format_var, state="readonly", width=55)
format_box.pack(pady=10)

def get_formats():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    def worker():
        try:
            with yt_dlp.YoutubeDL({}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = []
                for f in info.get("formats", []):
                    if f.get("vcodec") != "none" and f.get("acodec") != "none":
                        # نمایش رزولوشن + فرمت
                        desc = f"{f['format_id']} - {f.get('ext')} - {f.get('height','?')}p"
                        formats.append(desc)
                if formats:
                    format_box["values"] = formats
                    format_box.current(0)
                else:
                    messagebox.showinfo("Info", "No combined video+audio formats found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    threading.Thread(target=worker, daemon=True).start()


def download_video():
    url = url_entry.get().strip()
    choice = format_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return
    if not choice:
        messagebox.showerror("Error", "Please select a format first.")
        return

    format_id = choice.split(" - ")[0]  # گرفتن format_id
    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    output_template = os.path.join(download_folder, '%(title)s.%(ext)s')

    def worker():
        try:
            ydl_opts = {
                'format': format_id,
                'outtmpl': output_template,
                'noprogress': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

            # پیام قابل کلیک
            def open_folder(event=None):
                folder = os.path.dirname(file_path)
                if os.name == 'nt':
                    os.startfile(folder)
                elif os.name == 'posix':
                    import subprocess
                    subprocess.Popen(['xdg-open', folder])
                else:
                    webbrowser.open(folder)

            popup = tk.Toplevel(root)
            popup.title("Download Completed")
            popup.configure(bg="#1e1e2f")
            tk.Label(popup, text="✅ Download completed!",
                     font=("Segoe UI", 14), bg="#1e1e2f", fg="white").pack(pady=10)
            link = tk.Label(popup, text=file_path, fg="cyan", bg="#1e1e2f",
                            cursor="hand2", wraplength=500)
            link.pack(pady=5)
            link.bind("<Button-1>", open_folder)

        except Exception as e:
            messagebox.showerror("Download Failed", str(e))

    threading.Thread(target=worker, daemon=True).start()


btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Get Formats", command=get_formats,
          bg="#5c5cff", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Download", command=download_video,
          bg="#28a745", fg="white", width=15).grid(row=0, column=1, padx=10)

root.mainloop()