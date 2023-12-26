from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import speech_recognition as sr

app = Flask(__name__)


def audio_to_text():
    # 讀取原始音訊檔案
    original_audio = AudioSegment.from_file('backEnd/recode/user_upload.wav')

    # 將音訊轉換為PCM格式的WAV
    pcm_audio = original_audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    pcm_audio.export('backEnd/recode/converted_audio.wav', format='wav')
    # 使用speech_recognition進行語音識別
    r = sr.Recognizer()
    with sr.AudioFile('backEnd/recode/converted_audio.wav') as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='zh-TW')  # 使用Google Web Speech API進行語音識別
            print(text)
            return text
            
        except sr.UnknownValueError:
            text = "Google Web Speech API 無法識別音頻"
            print(text)
            return text
        except sr.RequestError as e:
            text = f"無法從Google Web Speech API獲取結果; {e}"
            print(text)
            return text

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': '檔案缺失'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': '沒有選擇檔案'}), 400
    if file:
        filename = 'user_upload.wav' # 自定義儲存的檔案名稱
        file.save(os.path.join('backEnd/recode', filename)) # 儲存檔案
        audio_to_text()
        return jsonify({'message': '檔案上傳成功'}), 200
    


if __name__ == '__main__':
    app.run(debug=True)
