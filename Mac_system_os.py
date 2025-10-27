import tkinter as tk
from tkinter import messagebox, filedialog
import time
import threading
import os
import winsound
from datetime import datetime

# Main OS Class
class MacMacSystemOS:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mac Mac System OS Boot")
        self.root.configure(bg="black")
        self.root.attributes('-fullscreen', True)

        # Boot Apple logo
        self.apple_logo = tk.Label(self.root, text="", font=("Helvetica", 180), fg="white", bg="black")
        self.apple_logo.pack(pady=200)

        # Loading animation
        self.loading = tk.Label(self.root, text="●", fg="white", bg="black", font=("Arial", 30))
        self.loading.pack()

        # Play boot sound
        threading.Thread(target=self.play_boot_sound).start()
        # Start boot loading animation
        threading.Thread(target=self.boot_loading).start()

        self.root.mainloop()

    def play_boot_sound(self):
        try:
            if os.path.exists("boot.wav"):
                winsound.PlaySound("boot.wav", winsound.SND_FILENAME)
            else:
                winsound.Beep(1000, 500)
        except:
            pass

    def boot_loading(self):
        for i in range(12):
            self.loading.config(text="●" + "." * (i % 4))
            time.sleep(0.3)
        self.root.after(0, self.login_screen)

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Mac Mac System OS - Login")
        self.root.configure(bg="#EAEAEA")

        login_frame = tk.Frame(self.root, bg="white", bd=0, relief="flat")
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
        login_frame.config(highlightthickness=2, highlightbackground="#CCCCCC")

        # Profile Circle
        profile_canvas = tk.Canvas(login_frame, width=100, height=100, bg="white", highlightthickness=0)
        profile_canvas.create_oval(5, 5, 95, 95, fill="#D0D0D0", outline="")
        profile_canvas.create_text(50, 50, text="👤", font=("Arial", 40))
        profile_canvas.pack(pady=20)

        tk.Label(login_frame, text="User", font=("Arial", 16), bg="white").pack()
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 14), width=20, justify="center")
        self.password_entry.pack(pady=10)
        tk.Button(login_frame, text="Login", font=("Arial", 12), command=self.check_password).pack(pady=5)

    def check_password(self):
        if self.password_entry.get() == "1234":
            self.desktop_screen()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    def desktop_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Mac Mac System OS - Desktop")
        self.root.configure(bg="#FFD700")  # Gold-themed desktop

        # Top Bar
        top_bar = tk.Frame(self.root, bg="#FFFFFF", height=40, relief="flat", bd=0)
        top_bar.pack(side="top", fill="x")

        # Apple Button
        apple_button = tk.Button(top_bar, text="", bg="white", font=("Arial", 20), relief="flat",
                                 command=self.show_apple_menu)
        apple_button.pack(side="left", padx=10)

        # Date/Time Display
        self.time_label = tk.Label(top_bar, font=("Arial", 12), bg="white")
        self.time_label.pack(side="right", padx=10)
        self.update_time()

        # Battery and Wi-Fi Icons (simple placeholders)
        battery_label = tk.Label(top_bar, text="🔋 100%", bg="white", font=("Arial", 12))
        battery_label.pack(side="right", padx=5)
        wifi_label = tk.Label(top_bar, text="📶", bg="white", font=("Arial", 12))
        wifi_label.pack(side="right", padx=5)

        # Desktop Interaction (double-click)
        self.root.bind("<Double-1>", self.change_background)

        # Floating Dock / Taskbar
        taskbar = tk.Frame(self.root, bg="#F0F0F0", height=70, relief="flat")
        taskbar.place(relx=0.5, rely=0.95, anchor="s", width=550, height=70)
        taskbar.config(highlightbackground="#DADADA", highlightthickness=2)

        # App Buttons in Taskbar
        tk.Button(taskbar, text="🗂️", font=("Arial", 20), relief="flat", bg="#F0F0F0",
                  command=self.open_file_manager).pack(side="left", padx=20)
        tk.Button(taskbar, text="🌐", font=("Arial", 20), relief="flat", bg="#F0F0F0",
                  command=self.open_web).pack(side="left", padx=20)
        tk.Button(taskbar, text="🛒", font=("Arial", 20), relief="flat", bg="#F0F0F0",
                  command=self.open_store).pack(side="left", padx=20)
        tk.Button(taskbar, text="⚙️", font=("Arial", 20), relief="flat", bg="#F0F0F0",
                  command=self.open_settings).pack(side="left", padx=20)

    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    # Apple Menu
    def show_apple_menu(self):
        menu = tk.Toplevel(self.root)
        menu.overrideredirect(True)
        menu.geometry("150x100+50+50")
        menu.configure(bg="white")

        tk.Button(menu, text="Restart", command=lambda: [menu.destroy(), self.restart_system()],
                  bg="white", relief="flat").pack(fill="x")
        tk.Button(menu, text="Shut Down", command=self.shutdown_system,
                  bg="white", relief="flat").pack(fill="x")
        menu.after(5000, menu.destroy)

    def restart_system(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__()

    def shutdown_system(self):
        self.root.destroy()  # Fully closes the OS simulator

    def change_background(self, event=None):
        color = filedialog.askcolor(title="Choose Desktop Background")[1]
        if color:
            self.root.configure(bg=color)

    # App Windows
    def open_file_manager(self):
        self.play_click_sound()
        win = tk.Toplevel(self.root)
        win.title("File Manager")
        win.geometry("400x300")
        tk.Label(win, text="File Manager App", font=("Arial", 16)).pack(pady=20)

    def open_web(self):
        self.play_click_sound()
        win = tk.Toplevel(self.root)
        win.title("Web Browser")
        win.geometry("400x300")
        tk.Label(win, text="Web Browser App", font=("Arial", 16)).pack(pady=20)

    def open_store(self):
        self.play_click_sound()
        win = tk.Toplevel(self.root)
        win.title("App Store")
        win.geometry("400x300")
        tk.Label(win, text="App Store App", font=("Arial", 16)).pack(pady=20)

    def open_settings(self):
        self.play_click_sound()
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("400x350")
        tk.Label(win, text="Settings App", font=("Arial", 16)).pack(pady=10)

        tk.Button(win, text="Change Background", command=self.change_background).pack(pady=5)
        tk.Button(win, text="Display Settings (Placeholder)", command=lambda: messagebox.showinfo("Display", "Display settings placeholder")).pack(pady=5)
        tk.Button(win, text="About Mac Mac System OS", command=lambda: messagebox.showinfo("About", "Mac Mac System OS v1.0\nCreated in Python")).pack(pady=5)

    # Sounds
    def play_click_sound(self):
        try:
            if os.path.exists("click.wav"):
                winsound.PlaySound("click.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                winsound.Beep(800, 100)
        except:
            pass

if __name__ == "__main__":
    MacMacSystemOS()

