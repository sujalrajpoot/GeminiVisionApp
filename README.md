
# GeminiVisionApp

GeminiVisionApp is a real-time AI-powered vision application built with Python using OpenCV, Tkinter, and Google Generative AI. It captures webcam frames, sends them to a generative AI model to describe the surrounding environment, and overlays the description on the live video feed. This application is designed to provide an intuitive, detailed, and human-like description of the environment, making it a highly advanced vision assistant.
# Table of Contents

- Features
- Requirements
- Installation
- Usage
- API Configuration
- License

# Features

- Real-Time Video Feed: Captures video from the user's webcam and displays it using Tkinter.
- AI-Powered Descriptions: Uses Google Generative AI to describe the surrounding environment in real-time based on the live video feed.
- Text Overlay: Displays the generated AI description directly on the video feed, with text wrapping for better readability.
- Model Selection: Allows listing and selecting different AI models for description generation.
- Threaded Processing: Separates video frame updates and AI description generation into different threads for smooth performance.
- Graceful Shutdown: Properly releases video capture resources when the application is closed.
# Requirements

- Python 3.7+
- OpenCV
- Tkinter (for GUI)
- Google Gemini AI SDK (google-generativeai)
- PIL (Pillow) for image processing
- yaspin for console spinners
- dotenv for environment variable management
# Installation

### Step 1: Clone the Repository
```
git clone https://github.com/your-username/GeminiVisionApp.git
cd GeminiVisionApp
```

### Step 2: Install Dependencies
- Ensure you have Python installed. Then, install the required Python packages:
```
pip install opencv-python Pillow yaspin google-generativeai python-dotenv
```

### Step 3: Configure the API
- You'll need an API key from Google Generative AI to interact with the vision models. Follow the steps in the API Configuration section to set up the environment.
# Usage

### Step 1: Add Your API Key

- Make sure your .env file contains your API key for Google Generative AI. Create a .env file in the root directory of the project:

```bash
touch .env
```

- Add the following to your .env file:
```bash
GENAI_API_KEY=your-google-generative-ai-key
```

### Step 2: Run the Application
- Run the following command to start the application:
```bash
python gemini_vision_app.py
```

- The Tkinter window will open, showing a real-time video feed from your webcam, with AI-generated descriptions overlaid on top of the video.

### Optional: List Available Models
- To see all the available generative models from the API, you can initialize the GeminiVisionApp with show_available_models=True. Example:

```python
app = GeminiVisionApp(root, show_available_models=True)
```

# API Configuration

- The application leverages Google Generative AI to provide real-time descriptions of the video feed. To configure the API:
    - Go to the Google Generative AI platform.
    - Sign in or create an account.
    - Generate your API key.
    - Add your API key to the .env file in the root of the project:

```bash
GENAI_API_KEY=your-api-key-here
```
- Ensure this file is kept safe and never shared publicly.

# Code Overview
### 1. GeminiVisionApp Class

- The main class that handles the entire application logic.

   -  __init__(self, root, show_available_models=False): Initializes the app, sets up the video source, and fetches available models if requested.

    - update_frame(self): Continuously updates the video feed by capturing frames from the webcam and displaying them on the Tkinter canvas.

    - display_image(self, frame, description): Displays the captured frame with the AI-generated description overlaid on it.

    - sanitize_text(self, text): Removes non-ASCII characters from the description to ensure it can be displayed without any issues.

    - generate_description(self): Runs in a separate thread, capturing images from the webcam and sending them to the AI model for generating descriptions.

    - send_image(self): Saves the current video frame as an image and sends it to the model for description generation.

    - on_closing(self): Gracefully shuts down the video capture and exits the Tkinter event loop when the window is closed.

# 2. Model Configuration
- By default, the app uses the gemini-1.5-flash-001 model for generating descriptions. You can modify or expand this functionality to select other models, such as:
```bash
models/gemini-1.5-pro-002
models/gemini-1.5-flash-001-tuning
models/gemini-1.5-flash-8b-exp-0924
```

# 3. Background Threads
- To ensure smooth performance, the app separates frame updates and AI description generation into different threads. The generate_description method runs in a background thread and does not block the main Tkinter event loop, ensuring that the video feed remains responsive.

# 4. Text Display
- The display_image method ensures that the description text fits within the video frame, wrapping it to the width of the frame for better readability. It uses the Pillow library for text rendering.

### Feel free to modify and adjust the content as necessary based on your specific project needs! Let me know if you'd like any changes or additions.
## License

[MIT](https://choosealicense.com/licenses/mit/)
# Hi, I'm Sujal Rajpoot! 👋
## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://sujalrajpoot.netlify.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sujal-rajpoot-469888305/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/sujalrajpoot70)


## 🚀 About Me
I'm a skilled Python programmer and experienced web developer. With a strong background in programming and a passion for creating interactive and engaging web experiences, I specialize in crafting dynamic websites and applications. I'm dedicated to transforming ideas into functional and user-friendly digital solutions. Explore my portfolio to see my work in action.
