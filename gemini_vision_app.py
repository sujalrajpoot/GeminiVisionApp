import re  # Import regular expressions module for text sanitization
import os
import cv2
import textwrap  
import threading
import tkinter as tk
from dotenv import load_dotenv
from yaspin import yaspin
import google.generativeai as genai
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Load environment variables from .env file
load_dotenv()

with yaspin(text="Initializing...", color="magenta") as spinner:
    try:
        genai.configure(api_key=os.getenv('GENAI_API_KEY'))
        spinner.text = "Initialization Complete!"
        spinner.ok("✔")  # Mark the spinner as successful
    except Exception as e:
        spinner.text = "Initialization Failed"
        spinner.fail("✖")  # Mark the spinner as failed
        print(f"Error: {e}")
    finally:
        spinner.stop()  # Ensure the spinner is stopped after the process

class GeminiVisionApp:
    def __init__(self, root, show_available_models: bool = False):
        """
        Initialize the Gemini Vision application with the given root window and optional flag to show all available models.

        Args:
            root (tkinter.Tk): The root window of the application.
            show_available_models (bool, optional): If True, list all available generative models. Defaults to False.

        Initializes the video capture from the given video source and sets the title of the root window to "Real-Time Gemini Vision".

        If show_available_models is True, fetches all available models from the GenAI API and prints them to the console.

        Initializes the model to use for generating descriptions and sets the running flag to True, automatically starting the webcam and AI description generation.

        Starts the update_frame method after a delay of 0 milliseconds to continuously update the video feed and a background thread to generate descriptions continuously.

        Stores the last successful description in the previous_response attribute for use when an exception occurs during AI description generation.

        """
        self.root = root
        self.root.title("Real-Time Gemini Vision")
        
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        if show_available_models:
            all_models = []
            with yaspin(text="Fetching All Available Models...", color="magenta") as spinner:
                for model in genai.list_models():
                    all_models.append(model.name)
                spinner.stop()
                print(f"All Available Models: {all_models}\n")

        self.model = genai.GenerativeModel("models/gemini-1.5-flash-001", system_instruction="You are a highly advanced real-time vision assistant designed to analyze the surroundings with utmost accuracy and detail. Your goal is to provide a comprehensive, clear, and short description of the surrounding, focusing on key elements such as objects, people, scenes, colors, emotions, and activities. Explain the relationships between objects, estimate the context of the scene, and note any significant visual details that make the surrounding unique. Ensure the description is informative, engaging, and insightful, with the ability to infer deeper meanings when applicable. Prioritize clarity, but do not shy away from complex interpretations when needed, making the response human-like and intuitive.")

        self.running = True  # Automatically start the webcam
        self.current_description = ""  # Initialize description text
        self.previous_response = ""  # Store the last successful description

        # Start webcam feed and AI description generation when the app starts
        self.root.after(0, self.update_frame)
        threading.Thread(target=self.generate_description, daemon=True).start()  # Start background description generation

    def print_available_models(self):
        """
        Prints a list of all available Gemini Vision models that can be used in this application.

        The list includes the model names of the form "models/gemini-<version>-<type>-<model_num>".
        """
        available_models = ["models/gemini-1.5-pro-002","models/gemini-1.5-pro-exp-0801","models/gemini-1.5-pro-exp-0827","models/gemini-1.5-flash-001","models/gemini-1.5-flash-001-tuning","models/gemini-1.5-flash","models/gemini-1.5-flash-exp-0827","models/gemini-1.5-flash-8b-exp-0827","models/gemini-1.5-flash-8b-exp-0924","models/gemini-1.5-flash-002"]
        for index, model_name in enumerate(available_models, start=1):print(f"{index}* {model_name}")

    def update_frame(self):
        # Continuously update the video feed without any pause
        """
        Continuously update the video feed without any pause.

        This function is responsible for reading from the video capture device and displaying the current frame with the description.

        If the app is running, it reads a frame from the video capture device, displays the frame and description, and then calls itself after 10 ms to create a smooth frame update experience.
        """
        if self.running:
            ret, frame = self.vid.read()
            if ret:
                self.display_image(frame, self.current_description)  # Display the current frame and description

            self.root.after(10, self.update_frame)  # Call this function again after 10 ms for smooth frame updates

    def display_image(self, frame, description):
        # Sanitize the description text to remove unsupported characters
        """
        Displays the current frame and description on the Tkinter canvas.

        This function is responsible for sanitizing the description text, converting the frame to RGB, drawing the description text on the frame, and displaying the resulting image on the canvas.

        Args:
            frame (numpy array): The current frame to be displayed.
            description (str): The description text to be displayed on the frame.
        """
        description = self.sanitize_text(description)

        # Convert the frame to RGB for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert frame to PIL image for drawing text
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Wrap the description text to fit the frame width
        max_width = img.width - 20  # Leave a 10-pixel margin on both sides
        font = ImageFont.load_default()  # Default font

        # Split the description into lines that fit within the frame width
        wrapped_text = textwrap.fill(description, width=int(max_width / 6))  # Adjust for font size

        # Set the top position for the text (10 pixels margin from the top)
        text_position = (10, 10)

        # Draw the wrapped text at the top of the frame
        draw.text(text_position, wrapped_text, font=font, fill=(255, 255, 255))  # White text color

        # Convert back to ImageTk for Tkinter display
        img = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def sanitize_text(self, text):
        """
        Remove non-ASCII characters from the description text.
        """
        # Replace non-ASCII characters with a blank space
        sanitized_text = re.sub(r'[^\x00-\x7F]+', '', text)
        return sanitized_text

    def generate_description(self):
        """
        Generate a description of the current frame every few seconds.

        This function captures a frame from the video capture device, saves it as an image, and then sends the image to the model to generate a description.

        The description is then retrieved from the model and displayed on the Tkinter canvas.

        If an exception occurs during the AI description generation, the app reverts to the previous description.

        This function is run in a separate thread to allow continuous frame updates and AI description generation without blocking the Tkinter event loop.

        """
        while self.running:
            # Capture a frame and generate a description every few seconds, allowing continuous frame display
            ret, frame = self.vid.read()
            if ret:
                image_path = "current_image.jpg"
                cv2.imwrite(image_path, frame)  # Save the frame as an image
                self.send_image()

    def send_image(self):
        """
        Send the current frame to the model and get a description.

        This function reads the current frame from the video capture device, saves it as an image, and then sends the image to the model to generate a description.

        The description is then retrieved from the model and displayed on the Tkinter canvas.

        If an exception occurs during the AI description generation, the app reverts to the previous description.

        """
        try:
            # Send the image to the model and get the description
            image = Image.open('./current_image.jpg')
            response = self.model.generate_content(["Describe the surrounding what you are looking at right now?", image], stream=False)
            response.resolve()
            self.previous_response = self.current_description  # Store the last successful description
            self.current_description = response.text  # Update the current description with the new one
            print(f"Gemini: \033[1;93m{self.current_description}\033[0m\n")
        except:
            # If an exception occurs, revert to the previous description
            self.current_description = self.previous_response

    def on_closing(self):
        """
        Stops the video capture and Tkinter event loop when the window is closed.

        This function is called when the window is closed and is responsible for stopping the video capture and quitting the Tkinter event loop.

        """
        self.running = False
        self.vid.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GeminiVisionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()