import tkinter as tk
import random

class TV:
    def __init__(self, root):
        self.root = root
        self.root.title("tvOS Cartoon Simulator")
        self.root.geometry("800x600")
        self.root.config(bg="black")

        self.is_on = False
        self.volume = 50
        self.channel_index = 0

        self.channels = [
            {"name": "News Channel", "type": "news"},
            {"name": "Tom and Jerry", "type": "tomjerry"},
            {"name": "Teen Titans", "type": "cartoon"},
            {"name": "Bob the Builder", "type": "cartoon"},
            {"name": "Captain Crunch", "type": "cartoon"}
        ]

        self.label = tk.Label(root, text="", fg="white", bg="black", font=("Arial", 18))
        self.label.pack(pady=5)

        self.canvas = tk.Canvas(root, width=780, height=480, bg="black")
        self.canvas.pack()

        # Shutdown button
        self.shutdown_button = tk.Button(root, text="Shutdown TV", command=self.shutdown)
        self.shutdown_button.pack(side="bottom", pady=5)

        # Power button to turn on TV
        self.power_button = tk.Button(root, text="Power ON", command=self.power_on)
        self.power_button.place(relx=0.45, rely=0.45, width=100, height=50)

        # Bind keys
        self.root.bind("<Up>", self.volume_up)
        self.root.bind("<Down>", self.volume_down)
        self.root.bind("<Left>", self.prev_channel)
        self.root.bind("<Right>", self.next_channel)
        self.root.bind("<Return>", self.first_channel)

        self.animation_objects = []

    # Power On sequence
    def power_on(self):
        if not self.is_on:
            self.power_button.destroy()
            self.label.config(text="Booting up tvOS...")
            self.root.after(2000, self.start_tv)

    def start_tv(self):
        self.is_on = True
        self.show_channel()

    # Shutdown
    def shutdown(self):
        self.root.destroy()

    # Show current channel
    def show_channel(self):
        if not self.is_on:
            return
        self.canvas.delete("all")
        channel = self.channels[self.channel_index]
        self.label.config(text=f"{channel['name']} | Volume: {self.volume}%")
        self.animation_objects = []

        if channel['type'] == "news":
            self.create_news_shapes()
        elif channel['type'] == "tomjerry":
            self.create_tom_jerry_shapes()
        else:
            self.create_cartoon_shapes()

        self.animate()

    # News shapes
    def create_news_shapes(self):
        for i in range(3):
            x = random.randint(50, 700)
            y = random.randint(50, 450)
            rect = self.canvas.create_rectangle(x, y, x+50, y+100, fill="blue")
            self.animation_objects.append({"id": rect, "dx": 0, "dy": random.choice([-2, 2])})

    # Tom and Jerry shapes
    def create_tom_jerry_shapes(self):
        # Tom as big gray rectangle, Jerry as small brown circle
        tom_x = random.randint(100, 600)
        tom_y = random.randint(100, 400)
        tom = self.canvas.create_rectangle(tom_x, tom_y, tom_x+80, tom_y+120, fill="gray")
        self.animation_objects.append({"id": tom, "dx": random.choice([-3,3]), "dy": random.choice([-3,3])})

        jerry_x = random.randint(100, 600)
        jerry_y = random.randint(100, 400)
        jerry = self.canvas.create_oval(jerry_x, jerry_y, jerry_x+40, jerry_y+40, fill="brown")
        self.animation_objects.append({"id": jerry, "dx": random.choice([-4,4]), "dy": random.choice([-4,4])})

    # Other cartoon shapes
    def create_cartoon_shapes(self):
        for i in range(5):
            x = random.randint(50, 700)
            y = random.randint(50, 450)
            size = random.randint(30, 80)
            color = random.choice(["red", "green", "yellow", "purple", "orange", "pink", "cyan"])
            oval = self.canvas.create_oval(x, y, x+size, y+size, fill=color)
            self.animation_objects.append({"id": oval, "dx": random.choice([-3,3]), "dy": random.choice([-3,3]), "size": size})

    # Animate shapes
    def animate(self):
        for obj in self.animation_objects:
            coords = self.canvas.coords(obj["id"])
            dx, dy = obj["dx"], obj["dy"]
            x1, y1, x2, y2 = coords
            # Bounce off walls
            if x1+dx < 0 or x2+dx > 780:
                obj["dx"] *= -1
            if y1+dy < 0 or y2+dy > 480:
                obj["dy"] *= -1
            self.canvas.move(obj["id"], obj["dx"], obj["dy"])
        self.root.after(30, self.animate)

    # Controls
    def volume_up(self, event=None):
        if self.is_on and self.volume < 100:
            self.volume += 10
            self.label.config(text=f"{self.channels[self.channel_index]['name']} | Volume: {self.volume}%")

    def volume_down(self, event=None):
        if self.is_on and self.volume > 0:
            self.volume -= 10
            self.label.config(text=f"{self.channels[self.channel_index]['name']} | Volume: {self.volume}%")

    def next_channel(self, event=None):
        if self.is_on:
            self.channel_index = (self.channel_index + 1) % len(self.channels)
            self.show_channel()

    def prev_channel(self, event=None):
        if self.is_on:
            self.channel_index = (self.channel_index - 1) % len(self.channels)
            self.show_channel()

    def first_channel(self, event=None):
        if self.is_on:
            self.channel_index = 0
            self.show_channel()

# Main
root = tk.Tk()
tv = TV(root)
root.mainloop()

