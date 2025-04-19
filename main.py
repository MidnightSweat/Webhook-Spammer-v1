import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
import requests

def start_spam():
    webhook = webhook_entry.get().strip()
    try:
        th = int(thread_entry.get())
        sleep_time = float(sleep_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Threads and Sleep time must be numbers.")
        return

    if not webhook:
        messagebox.showerror("Missing Info", "Please enter a webhook.")
        return

    def spam():
        count = 0
        while count < 50:
            try:
                msg = random.choice([
                    "This is a test message.",
                    "Another line here.",
                    "Moonlight vibes.",
                    "Test message.",
                    "Midnight sends greetings!"
                ])
                response = requests.post(webhook, json={'content': msg})
                if response.status_code == 204:
                    log_box.insert(tk.END, f"[+] Sent: {msg}\n")
                else:
                    log_box.insert(tk.END, f"[!] Failed ({response.status_code}): {msg}\n")
            except Exception as e:
                log_box.insert(tk.END, f"[x] Error: {e}\n")
            count += 1
            time.sleep(sleep_time)

    for _ in range(th):
        threading.Thread(target=spam, daemon=True).start()

# --- GUI ---
app = tk.Tk()
app.title("Moonlight Sender by Midnight")
app.geometry("700x600")
app.resizable(True, True)

# Show version popup
messagebox.showinfo("Moonlight Sender", "Moonlight Sender v1 - Created by Midnight")

# Set icon if available
try:
    app.iconbitmap("logo.ico")
except:
    pass

# Foreground frame (input fields and buttons)
frame = tk.Frame(app, bg="#000000", padx=10, pady=10)
frame.place(relx=0.5, rely=0.5, anchor="center")

def create_entry(label_text, default="", width=50):
    tk.Label(frame, text=label_text, bg="#000000", fg="white", font=("Consolas", 11)).pack(anchor="w")
    entry = tk.Entry(frame, width=width, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 11))
    entry.insert(0, default)
    entry.pack(pady=5)
    return entry

# Entry widgets
webhook_entry = create_entry("Webhook URL:")
thread_entry = create_entry("Number of Threads:", "2", 10)
sleep_entry = create_entry("Sleep Time (secs):", "3", 10)

# Start button
start_button = tk.Button(frame, text="Start Spamming", command=start_spam,
                         bg="#00ffcc", fg="black", font=("Consolas", 12, "bold"))
start_button.pack(pady=10)

# Log box
tk.Label(frame, text="Log Output:", bg="#000000", fg="white", font=("Consolas", 11)).pack(anchor="w")
log_box = tk.Text(frame, height=10, width=70, bg="#1e1e1e", fg="white", insertbackground="white", font=("Consolas", 10))
log_box.pack()

# Set background color of the entire window to black
app.config(bg="#000000")

app.mainloop()
