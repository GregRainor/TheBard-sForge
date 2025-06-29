# Project: RPG Ambiance - Action Plan for AI Assistant

## 1. Mandate and Role

You are my expert programming assistant. Your role is to help me develop a soundscape generation application for tabletop role-playing games. You are an expert in **Python**, specializing in **audio processing**, **AI models (NLP and audio generation)**, and **application development**.

We will work together in "pair programming" mode. I will be the "driver" (giving instructions and making strategic decisions), and you will be the "navigator" (writing the code, suggesting optimizations, and identifying potential issues).

## 2. Final Objective

The final objective is to create a software application capable of generating an immersive and dynamic real-time soundscape from a simple text prompt (e.g., "dark, haunted forest in the rain").

## 3. Our Collaboration Methodology

To ensure our collaboration is effective, we will adhere to the following principles (inspired by best practices for AI-assisted development):

* **Full Context:** At the beginning of each major new task, I will provide you with the complete source code of the relevant files. I will not assume you have a perfect memory of our previous conversations.
* **Atomic Tasks:** I will break down our goals into small, clear, and precise tasks. Instead of "Build the audio player," I will ask, "Write a Python function `play_sound(filepath)` that uses library X to play a sound."
* **Iterative (Top-Down) Development:** We will first build the application's skeleton with empty functions or placeholders, and then we will fill them in one by one.
* **Clear Examples:** For each function or module, I will provide an example of the expected input and output.
* **Plan Before Code:** For complex tasks, I will first ask you to outline your action plan in pseudo-code or logical steps before writing the final code. This will allow us to align.
* **Error Handling:** If you generate code that produces an error, I will provide you with the exact code I ran and the full error message so you can debug it.

## 4. Target Tech Stack

* **Language:** Python 3.10+
* **Environment Management:** `venv`
* **Audio Playback/Mixing:** We'll start with `pygame.mixer` for its simplicity (V0.1), then we can evaluate more robust libraries like `sounddevice` + `numpy` if needed.
* **Text Analysis (NLP):** Hugging Face `transformers` library (using a model like DistilBERT or similar).
* **Audio Generation (later stage):** We will explore models like `AudioCraft` (Meta) or `Stable Audio` (Stability AI).
* **GUI (optional, later stage):** `PyQt6` or `Tkinter`.

## 5. Detailed Action Plan (Roadmap)

We will build the project step by step. Here is the sequence.

---

### **Step 1: V0.1 - The Proof of Concept (POC) - The Basic Audio Player**

**Goal:** Validate that we can play and layer sounds in a controlled manner. No AI at this stage.

* **Task 1.1: Project Initialization**
    * Create the following folder structure:
        ```
        /rpg-ambiance
        |-- /src
        |   |-- main.py
        |-- /assets
        |   |-- /sounds
        |       |-- tavern_ambiance.wav
        |       |-- clinking_mugs.wav
        |-- requirements.txt
        |-- claude.md
        ```
    * Generate the content for `requirements.txt`, including `pygame`.
    * Generate the shell commands to create and activate a Python virtual environment.

* **Task 1.2: The Initial Audio Engine**
    * In `src/main.py`, write an `AudioEngine` class.
    * This class should have an `__init__()` method that initializes `pygame.mixer`. Consider managing the number of available channels (e.g., `pygame.mixer.set_num_channels(16)`).
    * It should have a method `play_sound(filepath, loop=False, volume=1.0)` that loads a sound and plays it on the first available channel. It should return the `Channel` object for future control.
    * It should have a method `stop_all_sounds()`.

* **Task 1.3: The Main Loop**
    * Following the class, in `main.py`, create a main execution block `if __name__ == "__main__":`.
    * Instantiate the `AudioEngine`.
    * Play the tavern ambiance sound on a loop.
    * Create a `while True` loop that waits for simple user input in the terminal (e.g., "press 'c' to hear mugs clinking").
    * If the user presses 'c', play the clinking mugs sound once.
    * If the user presses 'q', stop all sounds and exit the program.

---

### **Step 2: V0.2 - The Smart Orchestrator (Local Library)**

**Goal:** Replace the manual user input with a scene-based system that manages multiple sound layers.

* **Task 2.1: Define the Scene Structure**
    * We will define scenes in a JSON file. Propose a structure for a `scenes.json` file that would describe the "Tavern" scene. It must include a base ambiance track ("bed") and a list of punctual sounds ("one-shots") with their probability of occurrence per second.
    * Example of what I expect: `{ "tavern": { "bed": "assets/sounds/...", "oneshots": [ { "file": "assets/...", "prob_per_sec": 0.1, "volume_min": 0.8, "volume_max": 1.0 } ] } }`

* **Task 2.2: Create the Orchestrator**
    * Create a new `Orchestrator` class in a new file `src/orchestrator.py`.
    * The `Orchestrator` will take an `AudioEngine` instance as an argument in its `__init__`.
    * It will have a method `load_scenes_from_file(filepath)` to load the JSON file.
    * It will have a method `play_scene(scene_name)` that:
        1.  Stops all previously playing sounds.
        2.  Plays the scene's "bed" sound in a loop.
    * It will have an `update()` method, which must be called in every frame of the main loop. This method will iterate through the active scene's "one-shots" and, based on their probability, play the sounds randomly.

* **Task 2.3: Update `main.py`**
    * Modify the main loop to initialize and use the `Orchestrator`.
    * Instead of waiting for manual input, simply start the "tavern" scene and let the orchestrator's `update()` method run inside the main loop. Don't forget to add a `time.sleep()` to prevent the loop from using 100% CPU.

---

### **Step 3: V0.3 - The Interpreter (NLP)**

**Goal:** Understand a natural language prompt to select the correct scene.

*(We will tackle this step in more detail once V0.2 is functional. It will involve using Hugging Face to transform a sentence into tags, and then mapping those tags to our defined scenes.)*

---

### **Step 4: V1.0 - The Generative Leap (Text-to-Audio)**

**Goal:** Replace some (or all) of our library sounds with sounds generated on the fly.

*(This is the most complex and exciting step, which will make full use of the 5090 GPU. We will approach this once the rest of the application is solid.)*

# Using Gemini CLI for Large Codebase Analysis

When analyzing large codebases or multiple files that might exceed context limits, use the Gemini CLI with its massive
context window. Use `gemini -p` to leverage Google Gemini's large context capacity.

## File and Directory Inclusion Syntax

Use the `@` syntax to include files and directories in your Gemini prompts. The paths should be relative to WHERE you run the
  gemini command:

### Examples:

**Single file analysis:**
gemini -p "@src/main.py Explain this file's purpose and structure"

Multiple files:
gemini -p "@package.json @src/index.js Analyze the dependencies used in the code"

Entire directory:
gemini -p "@src/ Summarize the architecture of this codebase"

Multiple directories:
gemini -p "@src/ @tests/ Analyze test coverage for the source code"

Current directory and subdirectories:
gemini -p "@./ Give me an overview of this entire project"

# Or use --all_files flag:
gemini --all_files -p "Analyze the project structure and dependencies"

Implementation Verification Examples

Check if a feature is implemented:
gemini -p "@src/ @lib/ Has dark mode been implemented in this codebase? Show me the relevant files and functions"

Verify authentication implementation:
gemini -p "@src/ @middleware/ Is JWT authentication implemented? List all auth-related endpoints and middleware"

Check for specific patterns:
gemini -p "@src/ Are there any React hooks that handle WebSocket connections? List them with file paths"

Verify error handling:
gemini -p "@src/ @api/ Is proper error handling implemented for all API endpoints? Show examples of try-catch blocks"

Check for rate limiting:
gemini -p "@backend/ @middleware/ Is rate limiting implemented for the API? Show the implementation details"

Verify caching strategy:
gemini -p "@src/ @lib/ @services/ Is Redis caching implemented? List all cache-related functions and their usage"

Check for specific security measures:
gemini -p "@src/ @api/ Are SQL injection protections implemented? Show how user inputs are sanitized"

Verify test coverage for features:
gemini -p "@src/payment/ @tests/ Is the payment processing module fully tested? List all test cases"

When to Use Gemini CLI

Use gemini -p when:
- Analyzing entire codebases or large directories
- Comparing multiple large files
- Need to understand project-wide patterns or architecture
- Current context window is insufficient for the task
- Working with files totaling more than 100KB
- Verifying if specific features, patterns, or security measures are implemented
- Checking for the presence of certain coding patterns across the entire codebase

Important Notes

- Paths in @ syntax are relative to your current working directory when invoking gemini
- The CLI will include file contents directly in the context
- No need for --yolo flag for read-only analysis
- Gemini's context window can handle entire codebases that would overflow Claude's context
- When checking implementations, be specific about what you're looking for to get accurate results