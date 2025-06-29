from flask import Flask, render_template, request, jsonify, send_file
from src.audioldm_engine import AudioLDMEngine
import os
import threading
import time

app = Flask(__name__)
audio_engine = None
generation_status = {"status": "idle", "progress": 0, "message": ""}

def initialize_audio_engine():
    global audio_engine
    try:
        audio_engine = AudioLDMEngine()
        generation_status["message"] = "AudioLDM Engine ready!"
    except Exception as e:
        generation_status["message"] = f"Error initializing engine: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_audio():
    if not audio_engine:
        return jsonify({"error": "Audio engine not initialized"}), 500
    
    data = request.json
    prompt = data.get('prompt', '')
    duration = float(data.get('duration', 10.0))
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    def generate_async():
        generation_status["status"] = "generating"
        generation_status["progress"] = 50
        generation_status["message"] = f"Generating: {prompt}"
        
        try:
            file_path, gen_time = audio_engine.generate_audio(prompt, duration)
            generation_status["status"] = "complete"
            generation_status["progress"] = 100
            generation_status["message"] = f"Generated in {gen_time:.2f}s"
            generation_status["file_path"] = file_path
        except Exception as e:
            generation_status["status"] = "error"
            generation_status["message"] = str(e)
    
    thread = threading.Thread(target=generate_async)
    thread.start()
    
    return jsonify({"status": "started"})

@app.route('/generate_scene', methods=['POST'])
def generate_scene():
    if not audio_engine:
        return jsonify({"error": "Audio engine not initialized"}), 500
    
    data = request.json
    scene = data.get('scene', '')
    
    if not scene:
        return jsonify({"error": "No scene provided"}), 400
    
    def generate_scene_async():
        generation_status["status"] = "generating"
        generation_status["progress"] = 25
        generation_status["message"] = f"Generating scene: {scene}"
        
        try:
            files = audio_engine.generate_scene_audio(scene)
            generation_status["status"] = "complete"
            generation_status["progress"] = 100
            generation_status["message"] = f"Scene complete! {len(files)} audio files"
            generation_status["files"] = files
        except Exception as e:
            generation_status["status"] = "error"
            generation_status["message"] = str(e)
    
    thread = threading.Thread(target=generate_scene_async)
    thread.start()
    
    return jsonify({"status": "started"})

@app.route('/status')
def get_status():
    return jsonify(generation_status)

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        # Ensure filename is safe and in the generated_audio directory
        safe_filename = os.path.basename(filename)
        full_path = os.path.join('generated_audio', safe_filename)
        
        if os.path.exists(full_path):
            return send_file(full_path, as_attachment=False, mimetype='audio/wav')
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({"error": str(e)}), 404

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    try:
        safe_filename = os.path.basename(filename)
        full_path = os.path.join('generated_audio', safe_filename)
        
        if os.path.exists(full_path):
            return send_file(full_path, mimetype='audio/wav')
        else:
            return jsonify({"error": "Audio file not found"}), 404
    except Exception as e:
        print(f"Audio serve error: {e}")
        return jsonify({"error": str(e)}), 404

if __name__ == '__main__':
    print("🎭 Starting The Bard's Forge...")
    init_thread = threading.Thread(target=initialize_audio_engine)
    init_thread.start()
    app.run(debug=True, host='0.0.0.0', port=5000)