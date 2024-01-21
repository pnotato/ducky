import tkinter as tk
import asyncio
import numpy as np
from PIL import Image, ImageTk
import random

class Pet:
    def __init__(self):
        # WINDOW ---------------------------------------
        # Create empty window
        self.window = tk.Tk()
        self.window.resizable(0, 0)

        # Disable window background and make it transparent
        self.window.overrideredirect(1)
        self.window.wm_attributes("-transparent", "orange") # change orange to True if on macos

        # Create canvas, position at bottom center, and pack
        self.canvas = tk.Canvas(self.window, width=300, height=300, bg="orange", highlightthickness=0)
        self.window.attributes("-topmost", True)
        self.canvas.pack()

        # Create pet using image from assets folder
        self.start_frame = Image.open("Assets/idle1.png")
        self.start_frame = ImageTk.PhotoImage(self.start_frame)
        self.current_frame = self.canvas.create_image(150, 150, image=self.start_frame)

        # Initialize animations (normal and flipped)
        self.run_animation = [Image.open("Assets/running" + f"{i}" + ".png") for i in range(1, 4)]
        self.idle_animation = [Image.open("Assets/idle" + f"{i}" + ".png") for i in range(1, 2)]
        self.grabbed_animation = [Image.open("Assets/grabbed" + f"{i}" + ".png") for i in range(1, 3)]

        # Make images twice as small
        self.run_animation = [image.resize((image.width // 2, image.height // 2)) for image in self.run_animation]
        self.idle_animation = [image.resize((image.width // 2, image.height // 2)) for image in self.idle_animation]
        self.grabbed_animation = [image.resize((image.width // 2, image.height // 2)) for image in self.grabbed_animation]

        # Flip the images horizontally
        self.run_animation_flipped = [image.transpose(Image.FLIP_LEFT_RIGHT) for image in self.run_animation]
        self.idle_animation_flipped = [image.transpose(Image.FLIP_LEFT_RIGHT) for image in self.idle_animation]  # Add this line
        self.grabbed_animation_flipped = [image.transpose(Image.FLIP_LEFT_RIGHT) for image in self.grabbed_animation]  # Add this line

        self.run_animation = [ImageTk.PhotoImage(image) for image in self.run_animation]
        self.run_animation_flipped = [ImageTk.PhotoImage(image) for image in self.run_animation_flipped]
        self.idle_animation = [ImageTk.PhotoImage(image) for image in self.idle_animation]
        self.idle_animation_flipped = [ImageTk.PhotoImage(image) for image in self.idle_animation_flipped]  # Add this line
        self.grabbed_animation = [ImageTk.PhotoImage(image) for image in self.grabbed_animation]
        self.grabbed_animation_flipped = [ImageTk.PhotoImage(image) for image in self.grabbed_animation_flipped]  # Add this line
                
        # Initialize frame and animation variables
        self.frame = 0
        self.frame_rounded = 0
        self.current_animation = self.run_animation

        # PHYSICS --------------------------------------
        # Initialize velocity and acceleration
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

        # BIND MOUSE EVENTS ------------------------------
        # Bind mouse events to window for dragging
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_release)

        self.isDragged = False

        self.update()

    def update(self):
        # ANIMATION ------------------------------------
        # Change animation frame based on current animation and velocity
        if self.velocity[0] > 0:
            # Moving right
            self.current_animation = self.run_animation_flipped
        elif self.velocity[0] < 0:
            # Moving left
            self.current_animation = self.run_animation

        #print(f"Playing frame {self.frame} of animation")
        self.canvas.itemconfig(self.current_frame, image=self.current_animation[self.frame_rounded])

        # Increment frame
        self.frame += 0.1
        self.frame_rounded = int(self.frame)
        self.frame_rounded %= len(self.current_animation)
        self.canvas.update()

        # PHYSICS --------------------------------------
        # Update acceleration based on gravity
        if not self.isDragged:
            self.acceleration = np.array([0, 4])
        else:
            self.acceleration = np.array([0, 0])

        # Update velocity based on acceleration
        self.velocity += self.acceleration

        # Update position of window based on velocity
        x = int(self.window.winfo_x() + self.velocity[0])
        y = int(self.window.winfo_y() + self.velocity[1])
        self.window.geometry(f"+{x}+{y}")

        # If the pet reaches the bottom of the screen, freeze y velocity
        bottom = self.window.winfo_screenheight() - self.window.winfo_height()
        if y > bottom:
            self.velocity[1] = 0
            self.window.geometry(f"+{x}+{bottom}")

        # If the pet reaches the edges of the screen, freeze x velocity
        left = 0
        right = self.window.winfo_screenwidth() - self.window.winfo_width()
        if x < left:
            self.velocity[0] = 0
            self.window.geometry(f"+{left}+{y}")
        elif x > right:
            self.velocity[0] = 0
            self.window.geometry(f"+{right}+{y}")

    def play_animation(self, animation):
        # Change current animation and reset frame
        self.current_animation = animation
        self.frame = 0
        self.frame_rounded = 0


    def on_drag_start(self, event):
        # Record the starting position of the mouse when clicked
        self.start_x = event.x_root
        self.start_y = event.y_root

        self.isDragged = True
        self.play_animation(self.grabbed_animation)

    def on_drag_motion(self, event):
        # Calculate the movement of the mouse
        delta_x = event.x_root - self.start_x
        delta_y = event.y_root - self.start_y

        # set pet's velocity and acceleration to zero
        self.set_velocity([0, 0])
        self.set_acceleration([0, 0])

        # Move the window accordingly
        self.window.geometry(f"+{self.window.winfo_x() + delta_x}+{self.window.winfo_y() + delta_y}")

        # Update the starting position for the next movement
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_drag_release(self, event):
        self.isDragged = False


    def set_velocity(self, velocity):
        self.velocity = np.array(velocity)

    def set_acceleration(self, acceleration):
        self.acceleration = np.array(acceleration)

    def idle(self):
        if self.velocity[0] > 0:
            self.play_animation(self.idle_animation_flipped)
        else:
            self.play_animation(self.idle_animation)

        self.set_velocity([0, self.velocity[1]])
        self.set_acceleration([0, self.acceleration[1]])

    def say(self, text):
        # Create new top level window
        speech_window = tk.Toplevel(self.window)
        speech_window.resizable(0, 0)

        # Remove close/minimize bar on the top
        speech_window.overrideredirect(1)

        # Create speech bubble background (rounded white rectangle)
        speech_bubble = tk.Canvas(speech_window, width=300, height=100, bg="white", highlightthickness=0)
        speech_bubble.create_rectangle(0, 0, 300, 100, fill="white", outline="white")

        # Create text
        speech_text = tk.Label(speech_bubble, text=text, font=("Arial", 12), wraplength=280, justify="center")
        speech_text.pack()

        # Pack speech bubble after packing the text
        speech_bubble.pack()

        # Resize window to fit text on screen
        speech_window.update()
        speech_window.geometry(f"{speech_bubble.winfo_width()}x{speech_bubble.winfo_height()}")

        # Destroy the window after a time proportional to the amount of words
        speech_window.after(int(len(text.split()) * 200), speech_window.destroy)
