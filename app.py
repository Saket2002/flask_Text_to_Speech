from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import time

app = Flask(__name__)
AUDIO_FOLDER = "static/audio"

# Ensure the audio folder exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        lang = request.form['language']
        speed = request.form['speed']

        slow = True if speed == 'slow' else False
        filename = f"speech_{int(time.time())}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)

        # Generate TTS audio
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(filepath)

        return render_template('index.html', audio_file=filepath, filename=filename)

    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(AUDIO_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
