import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import requests
from datetime import datetime

class DiscordMessenger:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Server Messenger")
        self.root.geometry("900x750")
        self.root.resizable(True, True)

        # Variables
        self.is_running = False
        self.messages_sent = 0
        self.messages_failed = 0
        self.threads_list = []

        # Color scheme
        self.bg_primary = "#2c2f33"
        self.bg_secondary = "#23272a"
        self.bg_tertiary = "#1e2124"
        self.accent = "#7289da"
        self.accent_hover = "#677bc4"
        self.success = "#43b581"
        self.error = "#f04747"
        self.text_primary = "#ffffff"
        self.text_secondary = "#b9bbbe"

        self.root.config(bg=self.bg_primary)

        # Set icon if available
        try:
            self.root.iconbitmap("logo.ico")
        except:
            pass

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.bg_primary)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg=self.bg_primary)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        title = tk.Label(title_frame, text="Discord Server Messenger",
                        font=("Segoe UI", 24, "bold"),
                        bg=self.bg_primary, fg=self.accent)
        title.pack()

        subtitle = tk.Label(title_frame, text="Automated message sender for your Discord server",
                           font=("Segoe UI", 10),
                           bg=self.bg_primary, fg=self.text_secondary)
        subtitle.pack()

        # Configuration Panel
        config_frame = tk.LabelFrame(main_frame, text=" Configuration ",
                                     font=("Segoe UI", 11, "bold"),
                                     bg=self.bg_secondary, fg=self.text_primary,
                                     relief=tk.FLAT, padx=15, pady=15)
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # Webhook URL
        tk.Label(config_frame, text="Webhook URL:",
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_secondary, fg=self.text_primary).grid(row=0, column=0, sticky="w", pady=5)

        self.webhook_entry = tk.Entry(config_frame, width=60,
                                      font=("Segoe UI", 10),
                                      bg=self.bg_tertiary, fg=self.text_primary,
                                      insertbackground=self.text_primary,
                                      relief=tk.FLAT, highlightthickness=1,
                                      highlightbackground=self.accent)
        self.webhook_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Custom Message
        tk.Label(config_frame, text="Custom Message:",
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_secondary, fg=self.text_primary).grid(row=1, column=0, sticky="w", pady=5)

        self.message_entry = tk.Entry(config_frame, width=60,
                                      font=("Segoe UI", 10),
                                      bg=self.bg_tertiary, fg=self.text_primary,
                                      insertbackground=self.text_primary,
                                      relief=tk.FLAT, highlightthickness=1,
                                      highlightbackground=self.accent)
        self.message_entry.insert(0, "Server notification from automated messenger")
        self.message_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Number of threads
        tk.Label(config_frame, text="Threads:",
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_secondary, fg=self.text_primary).grid(row=2, column=0, sticky="w", pady=5)

        self.thread_entry = tk.Entry(config_frame, width=10,
                                     font=("Segoe UI", 10),
                                     bg=self.bg_tertiary, fg=self.text_primary,
                                     insertbackground=self.text_primary,
                                     relief=tk.FLAT, highlightthickness=1,
                                     highlightbackground=self.accent)
        self.thread_entry.insert(0, "1")
        self.thread_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Messages per thread
        tk.Label(config_frame, text="Messages per thread:",
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_secondary, fg=self.text_primary).grid(row=3, column=0, sticky="w", pady=5)

        self.count_entry = tk.Entry(config_frame, width=10,
                                    font=("Segoe UI", 10),
                                    bg=self.bg_tertiary, fg=self.text_primary,
                                    insertbackground=self.text_primary,
                                    relief=tk.FLAT, highlightthickness=1,
                                    highlightbackground=self.accent)
        self.count_entry.insert(0, "10")
        self.count_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # Sleep time
        tk.Label(config_frame, text="Delay (seconds):",
                font=("Segoe UI", 10, "bold"),
                bg=self.bg_secondary, fg=self.text_primary).grid(row=4, column=0, sticky="w", pady=5)

        self.sleep_entry = tk.Entry(config_frame, width=10,
                                    font=("Segoe UI", 10),
                                    bg=self.bg_tertiary, fg=self.text_primary,
                                    insertbackground=self.text_primary,
                                    relief=tk.FLAT, highlightthickness=1,
                                    highlightbackground=self.accent)
        self.sleep_entry.insert(0, "2")
        self.sleep_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        config_frame.columnconfigure(1, weight=1)

        # Control Buttons
        button_frame = tk.Frame(main_frame, bg=self.bg_primary)
        button_frame.pack(fill=tk.X, pady=(0, 15))

        self.start_button = tk.Button(button_frame, text="▶ Start Sending",
                                      command=self.start_sending,
                                      font=("Segoe UI", 11, "bold"),
                                      bg=self.success, fg=self.text_primary,
                                      activebackground=self.accent_hover,
                                      relief=tk.FLAT, cursor="hand2",
                                      padx=20, pady=10)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_frame, text="⏹ Stop Sending",
                                     command=self.stop_sending,
                                     font=("Segoe UI", 11, "bold"),
                                     bg=self.error, fg=self.text_primary,
                                     activebackground=self.error,
                                     relief=tk.FLAT, cursor="hand2",
                                     padx=20, pady=10, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(button_frame, text="Clear Log",
                                      command=self.clear_log,
                                      font=("Segoe UI", 10),
                                      bg=self.bg_secondary, fg=self.text_primary,
                                      activebackground=self.bg_tertiary,
                                      relief=tk.FLAT, cursor="hand2",
                                      padx=15, pady=10)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Statistics Panel
        stats_frame = tk.LabelFrame(main_frame, text=" Statistics ",
                                    font=("Segoe UI", 11, "bold"),
                                    bg=self.bg_secondary, fg=self.text_primary,
                                    relief=tk.FLAT, padx=15, pady=10)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_inner = tk.Frame(stats_frame, bg=self.bg_secondary)
        stats_inner.pack(fill=tk.X)

        # Sent count
        sent_frame = tk.Frame(stats_inner, bg=self.bg_secondary)
        sent_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(sent_frame, text="Messages Sent",
                font=("Segoe UI", 9),
                bg=self.bg_secondary, fg=self.text_secondary).pack()
        self.sent_label = tk.Label(sent_frame, text="0",
                                   font=("Segoe UI", 18, "bold"),
                                   bg=self.bg_secondary, fg=self.success)
        self.sent_label.pack()

        # Failed count
        failed_frame = tk.Frame(stats_inner, bg=self.bg_secondary)
        failed_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(failed_frame, text="Failed",
                font=("Segoe UI", 9),
                bg=self.bg_secondary, fg=self.text_secondary).pack()
        self.failed_label = tk.Label(failed_frame, text="0",
                                     font=("Segoe UI", 18, "bold"),
                                     bg=self.bg_secondary, fg=self.error)
        self.failed_label.pack()

        # Success rate
        rate_frame = tk.Frame(stats_inner, bg=self.bg_secondary)
        rate_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(rate_frame, text="Success Rate",
                font=("Segoe UI", 9),
                bg=self.bg_secondary, fg=self.text_secondary).pack()
        self.rate_label = tk.Label(rate_frame, text="0%",
                                   font=("Segoe UI", 18, "bold"),
                                   bg=self.bg_secondary, fg=self.accent)
        self.rate_label.pack()

        # Status
        status_frame = tk.Frame(stats_inner, bg=self.bg_secondary)
        status_frame.pack(side=tk.LEFT, padx=15)
        tk.Label(status_frame, text="Status",
                font=("Segoe UI", 9),
                bg=self.bg_secondary, fg=self.text_secondary).pack()
        self.status_label = tk.Label(status_frame, text="Idle",
                                     font=("Segoe UI", 12, "bold"),
                                     bg=self.bg_secondary, fg=self.text_secondary)
        self.status_label.pack()

        # Log Panel
        log_frame = tk.LabelFrame(main_frame, text=" Activity Log ",
                                 font=("Segoe UI", 11, "bold"),
                                 bg=self.bg_secondary, fg=self.text_primary,
                                 relief=tk.FLAT, padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_box = scrolledtext.ScrolledText(log_frame, height=15,
                                                 font=("Consolas", 9),
                                                 bg=self.bg_tertiary, fg=self.text_primary,
                                                 insertbackground=self.text_primary,
                                                 relief=tk.FLAT, wrap=tk.WORD)
        self.log_box.pack(fill=tk.BOTH, expand=True)

        # Configure log tags for colored output
        self.log_box.tag_config("success", foreground=self.success)
        self.log_box.tag_config("error", foreground=self.error)
        self.log_box.tag_config("info", foreground=self.accent)
        self.log_box.tag_config("warning", foreground="#faa61a")

        self.log("Discord Server Messenger initialized", "info")
        self.log("Configure your webhook and message settings above", "info")

    def log(self, message, tag="info"):
        """Add a message to the log with timestamp and color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{timestamp}] ", "info")
        self.log_box.insert(tk.END, f"{message}\n", tag)
        self.log_box.see(tk.END)

    def clear_log(self):
        """Clear the log box"""
        self.log_box.delete(1.0, tk.END)
        self.log("Log cleared", "info")

    def update_stats(self):
        """Update statistics display"""
        total = self.messages_sent + self.messages_failed
        success_rate = (self.messages_sent / total * 100) if total > 0 else 0

        self.sent_label.config(text=str(self.messages_sent))
        self.failed_label.config(text=str(self.messages_failed))
        self.rate_label.config(text=f"{success_rate:.1f}%")

    def start_sending(self):
        """Start sending messages"""
        webhook = self.webhook_entry.get().strip()
        message = self.message_entry.get().strip()

        try:
            threads = int(self.thread_entry.get())
            count = int(self.count_entry.get())
            sleep_time = float(self.sleep_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for threads, count, and delay.")
            return

        if not webhook:
            messagebox.showerror("Missing Webhook", "Please enter a webhook URL.")
            return

        if not webhook.startswith("https://discord.com/api/webhooks/") and not webhook.startswith("https://discordapp.com/api/webhooks/"):
            response = messagebox.askyesno("Invalid Webhook",
                                          "The webhook URL doesn't look like a Discord webhook. Continue anyway?")
            if not response:
                return

        if not message:
            messagebox.showerror("Missing Message", "Please enter a message to send.")
            return

        if threads < 1 or threads > 10:
            messagebox.showerror("Invalid Threads", "Number of threads must be between 1 and 10.")
            return

        if count < 1 or count > 1000:
            messagebox.showerror("Invalid Count", "Messages per thread must be between 1 and 1000.")
            return

        # Reset stats
        self.messages_sent = 0
        self.messages_failed = 0
        self.update_stats()

        # Update UI state
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Running", fg=self.success)

        self.log(f"Starting message sender with {threads} thread(s)", "info")
        self.log(f"Sending {count} message(s) per thread with {sleep_time}s delay", "info")

        # Start threads
        for i in range(threads):
            thread = threading.Thread(target=self.send_messages,
                                     args=(webhook, message, count, sleep_time, i+1),
                                     daemon=True)
            thread.start()
            self.threads_list.append(thread)

    def send_messages(self, webhook, message, count, sleep_time, thread_id):
        """Send messages in a thread"""
        for i in range(count):
            if not self.is_running:
                self.log(f"Thread {thread_id} stopped", "warning")
                break

            try:
                response = requests.post(webhook, json={'content': message}, timeout=10)

                if response.status_code == 204:
                    self.messages_sent += 1
                    self.log(f"[Thread {thread_id}] Message sent successfully ({i+1}/{count})", "success")
                else:
                    self.messages_failed += 1
                    self.log(f"[Thread {thread_id}] Failed with status {response.status_code}", "error")

                self.update_stats()

            except requests.exceptions.Timeout:
                self.messages_failed += 1
                self.log(f"[Thread {thread_id}] Request timed out", "error")
                self.update_stats()
            except Exception as e:
                self.messages_failed += 1
                self.log(f"[Thread {thread_id}] Error: {str(e)}", "error")
                self.update_stats()

            if i < count - 1:  # Don't sleep after last message
                time.sleep(sleep_time)

        # Check if all threads are done
        self.check_completion()

    def check_completion(self):
        """Check if all threads have completed"""
        if not self.is_running:
            return

        # Check if any threads are still alive
        active = any(t.is_alive() for t in self.threads_list)

        if not active:
            self.log("All messages sent!", "info")
            self.finish_sending()

    def stop_sending(self):
        """Stop sending messages"""
        self.is_running = False
        self.log("Stopping message sender...", "warning")
        self.finish_sending()

    def finish_sending(self):
        """Clean up after sending is complete or stopped"""
        self.is_running = False
        self.threads_list.clear()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Idle", fg=self.text_secondary)

# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordMessenger(root)

    # Show welcome message
    messagebox.showinfo("Discord Server Messenger",
                       "Discord Server Messenger v2.0\n\nAutomated message sender for Discord servers")

    root.mainloop()
