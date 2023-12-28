from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import speech_recognition as sr
from flask_socketio import SocketIO
from flask_cors import CORS,cross_origin
import openai
from openai import OpenAI

app = Flask(__name__,
            static_url_path='/python',   
            static_folder='static',      
            template_folder='templates') 
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False




CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

socketio = SocketIO(app, cors_allowed_origins="*")





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


def generate_text(user_input,user_history):
    client = OpenAI(
        api_key='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'
    )
  
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    
    messages=[
        {"role": "system", "content": f"你是一個友善、正向、樂觀、說話簡單簡短自然、積極的人,回答需要依據以下的使用者歷史問題{user_history}並且以1到2句話回答"},
        {"role": "user", "content": f"'{user_input}'"}
    ]
    )

    # 打印出生成的文本内容
    if completion.choices:
        generated_message = completion.choices[0].message
        if generated_message:
            print(generated_message.content)

            return generated_message.content
        else:
            print("No message content generated.")
            return "No message content generated."
    else:
        print("No response generated.")
        return "No response generated."
    
    


@socketio.on("user_text_input")
def user_text_input(data):
    print(data['messages'][-1])
    userID = data['userID']
    return_text =  generate_text(data['messages'][-1],data['messages'][0:-2])
    
    # return_text="text"
    socketio.emit("response",{"message":[return_text,userID]})



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
