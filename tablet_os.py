import tkinter as tk
from tkinter import ttk
import time
import threading
import random
from math import sin, cos, radians

# ======================
# Tablet OS - Powered by Python
# ======================

class TabletOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Tablet OS")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")
        self.state = "boot"
        self.battery_level = 75
        self.charging = False
        self.create_boot_screen()
        self.control_panel_visible = False
        self.panel_frame = None

        self.root.bind("<Escape>", self.open_power_menu)

    # ---------------------- BOOT SCREEN ----------------------
    def create_boot_screen(self):
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.boot_text = self.canvas.create_text(
            self.root.winfo_screenwidth()//2,
            self.root.winfo_screenheight()//2 + 100,
            text="Tablet OS",
            fill="white",
            font=("Segoe UI", 40, "bold"),
            state="hidden"
        )
        self.powered_text = self.canvas.create_text(
            self.root.winfo_screenwidth()//2,
            self.root.winfo_screenheight()//2 + 160,
            text="Powered by Python",
            fill="white",
            font=("Segoe UI", 20),
            state="hidden"
        )

        threading.Thread(target=self.boot_animation).start()

    def boot_animation(self):
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        radius = 80
        for i in range(90):
            self.canvas.delete("wave")
            for j in range(12):
                angle = radians(i * 4 + j * 30)
                x = w//2 + radius * cos(angle)
                y = h//2 + radius * sin(angle)
                self.canvas.create_oval(x-10, y-10, x+10, y+10,
                                        fill=f"#{int(155+100*sin(i/10))%255:02x}{int(200):02x}{int(255):02x}",
                                        width=0, tags="wave")
            time.sleep(0.05)
            self.canvas.update()

        for alpha in range(100, 0, -5):
            self.canvas.configure(bg=f"#{alpha:02x}{alpha:02x}{alpha:02x}")
            time.sleep(0.03)
            self.canvas.update()

        self.canvas.itemconfigure(self.boot_text, state="normal")
        self.canvas.itemconfigure(self.powered_text, state="normal")
        time.sleep(2)
        self.load_lock_screen()

    # ---------------------- LOCK SCREEN ----------------------
    def load_lock_screen(self):
        self.state = "lock"
        self.canvas.destroy()
        self.lock_frame = tk.Frame(self.root, bg="#add8e6")
        self.lock_frame.pack(fill="both", expand=True)

        self.clock_label = tk.Label(self.lock_frame, text="", font=("Segoe UI", 60), bg="#add8e6")
        self.clock_label.place(relx=0.5, rely=0.4, anchor="center")

        self.battery_label = tk.Label(self.lock_frame, text="🔋 75%", font=("Segoe UI", 18), bg="#add8e6")
        self.battery_label.place(relx=0.9, rely=0.05)

        self.wifi_label = tk.Label(self.lock_frame, text="📶 Connected", font=("Segoe UI", 18), bg="#add8e6")
        self.wifi_label.place(relx=0.05, rely=0.05)

        self.lock_frame.bind("<Button-1>", self.swipe_up)
        self.update_clock()
        self.update_battery()

    def update_clock(self):
        if self.state != "lock":
            return
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def update_battery(self):
        if self.state not in ["lock", "home"]:
            return
        change = random.choice([-1, 0, 1])
        self.battery_level = max(0, min(100, self.battery_level + change))
        icon = "⚡" if self.charging else "🔋"
        if self.state == "lock":
            self.battery_label.config(text=f"{icon} {self.battery_level}%")
        elif self.state == "home":
            self.home_battery_label.config(text=f"{icon} {self.battery_level}%")
        self.root.after(3000, self.update_battery)

    def swipe_up(self, event):
        for i in range(30):
            self.lock_frame.place_configure(rely=0 - (i / 30))
            self.root.update()
            time.sleep(0.01)
        self.load_home_screen()

    # ---------------------- HOME SCREEN ----------------------
    def load_home_screen(self):
        self.state = "home"
        self.lock_frame.destroy()
        self.home = tk.Frame(self.root, bg="#b0e0e6")
        self.home.pack(fill="both", expand=True)

        title = tk.Label(self.home, text="Tablet OS Home", font=("Segoe UI", 28, "bold"), bg="#b0e0e6")
        title.pack(pady=30)

        # Icons same as lock screen
        self.home_battery_label = tk.Label(self.home, text=f"🔋 {self.battery_level}%", font=("Segoe UI", 16), bg="#b0e0e6")
        self.home_battery_label.place(relx=0.9, rely=0.05)
        self.home_wifi_label = tk.Label(self.home, text="📶 Connected", font=("Segoe UI", 16), bg="#b0e0e6")
        self.home_wifi_label.place(relx=0.05, rely=0.05)

        # App buttons
        apps = ["Browser", "Gallery", "Settings", "Notes", "Music"]
        for app in apps:
            b = ttk.Button(self.home, text=app, command=lambda a=app: self.open_app(a))
            b.pack(pady=10)

        # Hold home screen to open widget/wallpaper menu
        self.home.bind("<ButtonPress-1>", self.start_hold)
        self.home.bind("<ButtonRelease-1>", self.end_hold)
        self.hold_start = None

        # Swipe down for control panel
        self.home.bind("<B1-Motion>", self.detect_swipe)

        self.update_battery()

    def start_hold(self, event):
        self.hold_start = time.time()

    def end_hold(self, event):
        if self.hold_start and time.time() - self.hold_start >= 1.5:
            self.open_widget_menu()
        self.hold_start = None

    def open_widget_menu(self):
        popup = tk.Toplevel(self.root)
        popup.geometry("400x400+700+300")
        popup.title("Widgets & Wallpaper")
        popup.configure(bg="#d0e8f0")
        tk.Label(popup, text="Add Widgets / Change Wallpaper", font=("Segoe UI", 16, "bold"), bg="#d0e8f0").pack(pady=20)
        ttk.Button(popup, text="Add Clock Widget").pack(pady=10)
        ttk.Button(popup, text="Change Wallpaper to Blue", command=lambda: self.home.configure(bg="#b0e0e6")).pack(pady=10)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=20)

    # ---------------------- CONTROL PANEL ----------------------
    def detect_swipe(self, event):
        if event.y > 100 and not self.control_panel_visible:
            self.show_control_panel()
        elif event.y < 50 and self.control_panel_visible:
            self.hide_control_panel()

    def show_control_panel(self):
        if self.panel_frame:
            self.panel_frame.destroy()
        self.panel_frame = tk.Frame(self.home, bg="#d0e8f0", height=300)
        self.panel_frame.pack(fill="x", side="top")
        self.control_panel_visible = True

        tk.Label(self.panel_frame, text="Control Panel", font=("Segoe UI", 20, "bold"), bg="#d0e8f0").pack(pady=10)
        ttk.Label(self.panel_frame, text=f"Wi-Fi: Connected").pack(pady=5)
        ttk.Label(self.panel_frame, text=f"Battery: {self.battery_level}%").pack(pady=5)
        ttk.Button(self.panel_frame, text="Toggle Charging", command=self.toggle_charging).pack(pady=5)

    def hide_control_panel(self):
        if self.panel_frame:
            self.panel_frame.destroy()
        self.control_panel_visible = False

    def toggle_charging(self):
        self.charging = not self.charging

    # ---------------------- POWER MENU ----------------------
    def open_power_menu(self, event=None):
        if self.state not in ["home", "lock"]:
            return
        popup = tk.Toplevel(self.root)
        popup.geometry("300x300+800+400")
        popup.title("Power Menu")
        popup.configure(bg="#222222")
        tk.Label(popup, text="Power Options", font=("Segoe UI", 18, "bold"), fg="white", bg="#222222").pack(pady=30)
        ttk.Button(popup, text="Restart", command=lambda: self.restart_os(popup)).pack(pady=10)
        ttk.Button(popup, text="Shutdown", command=lambda: self.shutdown_os(popup)).pack(pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(pady=10)

    def shutdown_os(self, popup):
        popup.destroy()
        fade = tk.Frame(self.root, bg="black")
        fade.place(relx=0, rely=0, relwidth=1, relheight=1)
        for i in range(0, 255, 10):
            fade.configure(bg=f"#{i:02x}{i:02x}{i:02x}")
            self.root.update()
            time.sleep(0.02)
        self.root.destroy()

    def restart_os(self, popup):
        popup.destroy()
        fade = tk.Frame(self.root, bg="black")
        fade.place(relx=0, rely=0, relwidth=1, relheight=1)
        for i in range(0, 255, 10):
            fade.configure(bg=f"#{i:02x}{i:02x}{i:02x}")
            self.root.update()
            time.sleep(0.02)
        fade.destroy()
        self.home.destroy()
        self.create_boot_screen()

    # ---------------------- APPS ----------------------
    def open_app(self, app_name):
        app_win = tk.Toplevel(self.root)
        app_win.title(app_name)
        app_win.geometry("600x400")
        label = tk.Label(app_win, text=f"{app_name} App Running...", font=("Segoe UI", 20))
        label.pack(expand=True)
        ttk.Button(app_win, text="Close", command=app_win.destroy).pack(pady=10)


# ---------------------- RUN OS ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TabletOS(root)
    root.mainloop()
