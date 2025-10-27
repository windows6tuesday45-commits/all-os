# HandyOS_full_v3.py
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import datetime, random

# ---------------- UTILITY FOR MOVABLE WINDOWS ----------------
class DraggableWindow(tk.Toplevel):
    def __init__(self, parent, title="Window", width=400, height=300, bg="#222222"):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{width}x{height}+300+200")
        self.configure(bg=bg)
        self.overrideredirect(True)  # Remove default title bar
        self._offsetx = 0
        self._offsety = 0

        # Custom title bar
        self.title_bar = tk.Frame(self, bg="#555555", relief="raised", bd=0, height=25)
        self.title_bar.pack(fill="x")
        self.title_label = tk.Label(self.title_bar, text=title, bg="#555555", fg="white")
        self.title_label.pack(side="left", padx=5)
        self.close_btn = tk.Button(self.title_bar, text="X", bg="#ff4444", fg="white", command=self.destroy, bd=0)
        self.close_btn.pack(side="right", padx=5)

        self.title_bar.bind("<Button-1>", self.click_win)
        self.title_bar.bind("<B1-Motion>", self.drag_win)
        self.bind("<Button-1>", self.click_win)
        self.bind("<B1-Motion>", self.drag_win)

    def click_win(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def drag_win(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f"+{x}+{y}")

# ---------------- HANDY OS ----------------
class HandyOS:
    def __init__(self, root):
        self.root = root
        self.root.title("HandyOS")
        self.root.attributes("-fullscreen", True)
        self.user_data = {"color": "#0080ff", "bg": "#003366", "username": "User"}
        self.show_boot()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ---------------- BOOT SCREEN ----------------
    def show_boot(self):
        self.clear()
        self.root.configure(bg="black")
        tk.Label(self.root, text="HandyOS", fg="lightgreen",
                 bg="black", font=("Segoe UI", 40, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(2500, self.show_setup_stage)

    # ---------------- SETUP ----------------
    def show_setup_stage(self):
        self.clear()
        self.root.configure(bg="#001a33")
        tk.Label(self.root, text="HandyOS Setup", fg="lightgreen",
                 bg="#001a33", font=("Segoe UI", 36, "bold")).pack(pady=50)
        tk.Label(self.root, text="Choose Accent Color and Background", fg="white",
                 bg="#001a33", font=("Segoe UI", 18)).pack(pady=20)
        tk.Button(self.root, text="Pick Accent Color", font=("Segoe UI", 14),
                  command=self.pick_accent).pack(pady=10)
        tk.Button(self.root, text="Pick Background Color", font=("Segoe UI", 14),
                  command=self.pick_background).pack(pady=10)
        tk.Label(self.root, text="Username:", fg="white", bg="#001a33", font=("Segoe UI", 14)).pack(pady=10)
        self.username_entry = tk.Entry(self.root, font=("Segoe UI", 14))
        self.username_entry.pack(pady=10)
        tk.Button(self.root, text="Finish Setup ▶", font=("Segoe UI", 16),
                  command=self.finish_setup).pack(pady=30)

    def pick_accent(self):
        color = colorchooser.askcolor(title="Choose Accent Color")
        if color[1]:
            self.user_data["color"] = color[1]

    def pick_background(self):
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:
            self.user_data["bg"] = color[1]
            self.root.configure(bg=color[1])

    def finish_setup(self):
        self.user_data["username"] = self.username_entry.get() or "User"
        self.show_desktop()

    # ---------------- DESKTOP ----------------
    def show_desktop(self):
        self.clear()
        self.root.configure(bg=self.user_data["bg"])
        self.root.bind("<Button-3>", self.show_context_menu)
        # Taskbar
        taskbar = tk.Frame(self.root, bg=self.user_data["color"], height=40)
        taskbar.pack(side="bottom", fill="x")
        start_btn = tk.Button(taskbar, text="Start", bg="#333", fg="white",
                              font=("Segoe UI", 10), command=self.open_start_menu)
        start_btn.pack(side="left")
        self.clock = tk.Label(taskbar, text=datetime.datetime.now().strftime("%H:%M:%S"),
                              fg="white", bg=self.user_data["color"], font=("Segoe UI", 12))
        self.clock.pack(side="right", padx=10)
        self.update_clock()
        # Desktop Icons
        my_comp = tk.Button(self.root, text="My Computer", width=14, height=2, command=self.show_setup_stage)
        my_comp.place(x=100, y=100)
        tk.Button(self.root, text="Recycle Bin", width=14, height=2).place(x=100, y=180)

    def update_clock(self):
        self.clock.config(text=datetime.datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    # ---------------- START MENU ----------------
    def open_start_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("Start Menu")
        menu.geometry("400x500+10+200")
        menu.configure(bg="#1a1a1a")
        sections = [
            ("Programs", self.placeholder_window),
            ("Control Panel", self.control_panel),
            ("Apps", self.placeholder_window),
            ("About", self.about_os),
            ("System", self.system_info),
            ("CMD", self.command_prompt),
            ("Run", self.run_box),
            ("Power", self.power_menu)
        ]
        for text, cmd in sections:
            tk.Button(menu, text=text, width=30, height=2, bg=self.user_data["color"], fg="white",
                      font=("Segoe UI", 12), command=cmd).pack(pady=4)

    # ---------------- RIGHT CLICK ----------------
    def show_context_menu(self, event):
        ctx = tk.Menu(self.root, tearoff=0)
        ctx.add_command(label="Refresh", command=lambda: messagebox.showinfo("Refreshed", "Desktop refreshed"))
        ctx.add_command(label="Change Background", command=self.pick_background)
        ctx.add_command(label="Personalize", command=self.control_panel)
        ctx.post(event.x_root, event.y_root)

    # ---------------- CONTROL PANEL ----------------
    def control_panel(self):
        cp = DraggableWindow(self.root, title="Control Panel", width=600, height=500)
        tk.Label(cp, text="Control Panel", fg="lightgreen", bg="#222222", font=("Segoe UI", 24, "bold")).pack(pady=20)
        options = [
            "Sounds", "User Accounts", "New Hardware", "Display", "Display Colors",
            "System", "Product Activation", "Browser Options", "Network Settings", "Updates"
        ]
        for opt in options:
            tk.Button(cp, text=opt, width=30, height=2, bg=self.user_data["color"], fg="white",
                      font=("Segoe UI", 12), command=lambda o=opt: messagebox.showinfo(o, f"{o} settings coming soon")).pack(pady=4)

    # ---------------- OTHER APPS ----------------
    def about_os(self):
        win = DraggableWindow(self.root, title="About HandyOS", width=400, height=300)
        tk.Label(win, text="HandyOS v10.0 (Simulated)\nCreated by GPT-5", fg="lightgreen", bg="#222222",
                 font=("Segoe UI", 16)).pack(pady=40)

    def system_info(self):
        win = DraggableWindow(self.root, title="System Information", width=400, height=300)
        tk.Label(win, text="System: HandyOS Virtual Machine\nCPU: Simulated\nRAM: 4 GB\nGraphics: Virtual",
                 fg="lightgreen", bg="#222222", font=("Segoe UI", 12), justify="left").pack(pady=30)

    def command_prompt(self):
        cmd = DraggableWindow(self.root, title="Command Prompt", width=600, height=400)
        text = tk.Text(cmd, bg="black", fg="lightgreen", insertbackground="lightgreen")
        text.pack(fill="both", expand=True)
        text.insert("end", "HandyOS CMD v1.0\nType 'help' for commands.\n\nC:\\> ")
        text.bind("<Return>", lambda e: text.insert("end", "\nC:\\> "))

    def run_box(self):
        rb = DraggableWindow(self.root, title="Run", width=400, height=150)
        tk.Label(rb, text="Type the name of a program:", fg="white", bg="#222222", font=("Segoe UI", 12)).pack(pady=10)
        entry = tk.Entry(rb, font=("Segoe UI", 12))
        entry.pack(pady=5)
        tk.Button(rb, text="OK", bg=self.user_data["color"], fg="white",
                  command=lambda: messagebox.showinfo("Run", f"Running: {entry.get()}")).pack(pady=5)

    def power_menu(self):
        pwr = DraggableWindow(self.root, title="Power Options", width=300, height=200)
        tk.Button(pwr, text="Shutdown", bg="red", fg="white", font=("Segoe UI", 14),
                  command=lambda: self.shutdown(pwr)).pack(pady=10)
        tk.Button(pwr, text="Restart", bg="orange", fg="white", font=("Segoe UI", 14),
                  command=lambda: self.restart(pwr)).pack(pady=10)

    def shutdown(self, win):
        win.destroy()
        self.clear()
        self.root.configure(bg="black")
        tk.Label(self.root, text="Shutting down HandyOS...", fg="white", bg="black", font=("Segoe UI", 24)).pack(pady=300)
        self.root.after(2500, self.root.quit)

    def restart(self, win):
        win.destroy()
        self.show_boot()

    # Placeholder
    def placeholder_window(self):
        messagebox.showinfo("Coming Soon", "This feature is under development.")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HandyOS(root)
    root.mainloop()
