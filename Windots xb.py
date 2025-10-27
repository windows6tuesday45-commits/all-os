import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
import threading
import sys
import time

# ---------- CONFIG ----------
BOOT_DELAY = 2
DESKTOP_BG = "#3a6ea5"
TASKBAR_COLOR = "#245edb"
START_COLOR = "#0b4acb"

# ---------- APP ----------
class WindowsXB:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows.xb")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Control-z>", self.unlock_system)

        # State
        self.desktop_icons_visible = True
        self.icon_size = "medium"
        self.recycle_bin_items = ["Old Document.txt", "Photo.png", "Archive.zip"]
        self.locked = False
        self.start_menu_open = False

        # Start boot screen
        self.show_boot_screen()

    # ---------- BOOT SCREEN ----------
    def show_boot_screen(self):
        self.root.config(cursor="none")
        boot_frame = tk.Frame(self.root, bg="black")
        boot_frame.pack(fill="both", expand=True)
        label = tk.Label(boot_frame, text="Windows.xb", fg="white", bg="black",
                         font=("Segoe UI", 40, "bold"))
        label.pack(expand=True)
        bar = ttk.Progressbar(boot_frame, mode="indeterminate", length=300)
        bar.pack(pady=20)
        bar.start(10)
        threading.Thread(target=self.boot_sequence, args=(boot_frame,)).start()

    def boot_sequence(self, frame):
        time.sleep(BOOT_DELAY)
        frame.destroy()
        self.show_desktop()

    # ---------- DESKTOP ----------
    def show_desktop(self):
        self.root.config(cursor="arrow")
        self.desktop = tk.Frame(self.root, bg=DESKTOP_BG)
        self.desktop.pack(fill="both", expand=True)
        self.desktop.bind("<Button-3>", self.show_context_menu)

        # Taskbar
        self.taskbar = tk.Frame(self.desktop, bg=TASKBAR_COLOR, height=40)
        self.taskbar.pack(side="bottom", fill="x")

        # Start button
        self.start_btn = tk.Button(self.taskbar, text="Start", bg=START_COLOR,
                              fg="white", font=("Segoe UI", 10, "bold"),
                              command=self.toggle_start_menu)
        self.start_btn.pack(side="left", padx=5, pady=5)

        # System tray clock
        self.clock_label = tk.Label(self.taskbar, fg="white", bg=TASKBAR_COLOR, font=("Segoe UI", 10))
        self.clock_label.pack(side="right", padx=10)
        self.update_clock()

        self.icon_widgets = []
        self.create_desktop_icons()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    # ---------- DESKTOP ICONS ----------
    def create_desktop_icons(self):
        for w in getattr(self, 'icon_widgets', []):
            w.destroy()
        self.icon_widgets = []
        if not self.desktop_icons_visible:
            return

        size_map = {"small": 30, "medium": 45, "large": 65}
        font_map = {"small": 10, "medium": 11, "large": 13}
        size = size_map[self.icon_size]
        font_size = font_map[self.icon_size]

        icons_data = [
            ("♻️", "Recycle Bin", 50, 100),
            ("🌐", "Browser", 50, 220)
        ]
        for emoji, name, x, y in icons_data:
            icon = self.create_icon(x, y, emoji, name, size, font_size)
            self.icon_widgets.append(icon)

    def create_icon(self, x, y, emoji, text, size, font_size):
        frame = tk.Frame(self.desktop, bg=DESKTOP_BG)
        frame.place(x=x, y=y)
        label_img = tk.Label(frame, text=emoji, font=("Segoe UI Emoji", size), bg=DESKTOP_BG)
        label_img.pack()
        label_text = tk.Label(frame, text=text, fg="white", bg=DESKTOP_BG, font=("Segoe UI", font_size))
        label_text.pack()

        # Dragging
        def start_drag(e):
            frame._drag_x = e.x
            frame._drag_y = e.y
        def do_drag(e):
            dx = e.x - frame._drag_x
            dy = e.y - frame._drag_y
            new_x = frame.winfo_x() + dx
            new_y = frame.winfo_y() + dy
            frame.place(x=new_x, y=new_y)
        label_img.bind("<Button-1>", start_drag)
        label_img.bind("<B1-Motion>", do_drag)
        label_text.bind("<Button-1>", start_drag)
        label_text.bind("<B1-Motion>", do_drag)

        # Double-click
        def open_icon(e):
            if text == "Recycle Bin":
                self.open_recycle_bin()
            else:
                messagebox.showinfo("Windows.xb", f"Opening {text}...")
        label_img.bind("<Double-Button-1>", open_icon)
        label_text.bind("<Double-Button-1>", open_icon)

        # Right-click Recycle Bin
        def right_click(e):
            self.recycle_bin_menu(e)
        frame.bind("<Button-3>", right_click)
        label_img.bind("<Button-3>", right_click)
        label_text.bind("<Button-3>", right_click)
        return frame

    # ---------- RIGHT-CLICK MENUS ----------
    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        view_menu = tk.Menu(menu, tearoff=0)
        view_menu.add_command(label="Large Icons", command=lambda: self.set_icon_size("large"))
        view_menu.add_command(label="Medium Icons", command=lambda: self.set_icon_size("medium"))
        view_menu.add_command(label="Small Icons", command=lambda: self.set_icon_size("small"))
        menu.add_cascade(label="View", menu=view_menu)

        if self.desktop_icons_visible:
            menu.add_command(label="Don't Show Desktop Icons", command=self.toggle_icons)
        else:
            menu.add_command(label="Show Desktop Icons", command=self.toggle_icons)

        menu.add_command(label="Refresh", command=self.refresh_desktop)
        menu.add_command(label="Personalize", command=self.open_personalize)
        menu.tk_popup(event.x_root, event.y_root)

    def recycle_bin_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Open", command=self.open_recycle_bin)
        menu.add_command(label="Empty Recycle Bin", command=self.empty_recycle_bin)
        menu.add_command(label="Personalize", command=self.open_personalize)
        menu.add_command(label="Add New Item", command=self.add_new_item)
        menu.tk_popup(event.x_root, event.y_root)

    def empty_recycle_bin(self):
        if not self.recycle_bin_items:
            messagebox.showinfo("Recycle Bin", "Nothing to delete.")
            return
        if messagebox.askyesno("Recycle Bin", f"Are you sure you want to empty the Recycle Bin? {len(self.recycle_bin_items)} items?"):
            self.recycle_bin_items.clear()

    def add_new_item(self):
        name = simpledialog.askstring("Create Shortcut", "Enter the name of the new item:")
        if name:
            self.recycle_bin_items.append(name)
            messagebox.showinfo("Create Shortcut", f"{name} created.")

    # ---------- Start Menu ----------
    def toggle_start_menu(self):
        if self.start_menu_open:
            self.start_menu.destroy()
            self.start_menu_open = False
        else:
            self.start_menu_open = True
            self.start_menu = tk.Toplevel(self.root)
            self.start_menu.geometry(f"250x450+0+50")
            self.start_menu.overrideredirect(True)
            self.start_menu.configure(bg="#e4e4e4", highlightbackground="black", highlightthickness=2)

            tk.Label(self.start_menu, text="Pinned Apps", font=("Segoe UI", 12, "bold"), bg="#e4e4e4").pack(pady=5)
            apps = ["Browser", "Notepad", "WordPad", "Calendar", "Calculator", "Paint", "Email", "System Explorer"]
            for app in apps:
                btn = tk.Button(self.start_menu, text=app, anchor="w", width=25,
                                bg="white", relief="flat",
                                command=lambda a=app: messagebox.showinfo("Windows.xb", f"Opening {a}..."))
                btn.pack(pady=2, padx=5)

            # Power Options
            tk.Label(self.start_menu, text="Power Options", font=("Segoe UI", 12, "bold"), bg="#e4e4e4").pack(pady=5)
            tk.Button(self.start_menu, text="Lock", anchor="w", command=self.lock_system).pack(fill="x", padx=10)
            tk.Button(self.start_menu, text="Sleep", anchor="w", command=self.sleep_system).pack(fill="x", padx=10)
            tk.Button(self.start_menu, text="Restart", anchor="w", command=self.restart_system).pack(fill="x", padx=10)
            tk.Button(self.start_menu, text="Shutdown", anchor="w", command=self.shutdown_system).pack(fill="x", padx=10)

    # ---------- POWER ACTIONS ----------
    def lock_system(self):
        self.locked = True
        self.desktop.pack_forget()
        self.taskbar.pack_forget()
        self.lock_screen = tk.Frame(self.root, bg="black")
        self.lock_screen.pack(fill="both", expand=True)
        tk.Label(self.lock_screen, text="SYSTEM LOCKED\nPress CTRL+Z to unlock", fg="white", bg="black", font=("Segoe UI", 24)).pack(expand=True)

    def unlock_system(self, event=None):
        if self.locked:
            self.lock_screen.destroy()
            self.show_desktop()
            self.locked = False

    def sleep_system(self):
        self.desktop.pack_forget()
        self.taskbar.pack_forget()
        self.sleep_screen = tk.Frame(self.root, bg="gray20")
        self.sleep_screen.pack(fill="both", expand=True)
        tk.Label(self.sleep_screen, text="SYSTEM SLEEP\nPress Start button to wake", fg="white", bg="gray20", font=("Segoe UI", 24)).pack(expand=True)
        # Wake on start button
        self.start_btn.bind("<Button-1>", self.wake_system)

    def wake_system(self, event=None):
        self.sleep_screen.destroy()
        self.show_desktop()

    def restart_system(self):
        python = sys.executable
        self.root.destroy()
        threading.Thread(target=lambda: sys.exit()).start()

    def shutdown_system(self):
        self.root.destroy()

    # ---------- PERSONALIZE ----------
    def open_personalize(self):
        personalize = tk.Toplevel(self.root)
        personalize.title("Personalize")
        personalize.geometry("400x300")
        personalize.configure(bg="#e4e4e4")
        tk.Label(personalize, text="Choose Theme:", bg="#e4e4e4").pack()
        theme_var = tk.StringVar(value="Luna Blue")
        def apply_theme():
            choice = theme_var.get()
            colors = {"Luna Blue": "#3a6ea5", "Silver": "#c0c0c0", "Olive Green": "#9dbb61"}
            self.desktop.configure(bg=colors.get(choice, "#3a6ea5"))
        for t in ["Luna Blue", "Silver", "Olive Green"]:
            tk.Radiobutton(personalize, text=t, variable=theme_var, value=t,
                           bg="#e4e4e4", command=apply_theme).pack(anchor="w", padx=20)
        tk.Button(personalize, text="Close", command=personalize.destroy).pack(pady=20)

    # ---------- Recycle Bin ----------
    def open_recycle_bin(self):
        bin_win = tk.Toplevel(self.root)
        bin_win.geometry("300x400+200+100")
        bin_win.title("Recycle Bin")
        tk.Label(bin_win, text="Recycle Bin Items", font=("Segoe UI", 12, "bold")).pack(pady=5)

        listbox = tk.Listbox(bin_win)
        for item in self.recycle_bin_items:
            listbox.insert(tk.END, item)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(bin_win, text="Empty Recycle Bin", command=self.empty_recycle_bin).pack(pady=5)
        tk.Button(bin_win, text="Close", command=bin_win.destroy).pack(pady=5)

    # ---------- DESKTOP ICON SIZE ----------
    def set_icon_size(self, size):
        self.icon_size = size
        self.create_desktop_icons()
    def toggle_icons(self):
        self.desktop_icons_visible = not self.desktop_icons_visible
        self.create_desktop_icons()
    def refresh_desktop(self):
        self.create_desktop_icons()

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = WindowsXB(root)
    root.mainloop()

