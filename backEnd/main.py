from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import speech_recognition as sr
from flask_socketio import SocketIO
from flask_cors import CORS,cross_origin
import openai
from openai import OpenAI
import json
from datetime import datetime
from utils.generation import SAMPLE_RATE, generate_audio, preload_models

from scipy.io.wavfile import write as write_wav
from IPython.display import Audio



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



def to_audio(text_input:str,user_id:str)->str:


    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"main_video_{user_id}_{timestamp}.wav"
        # download and load all models
        preload_models()

        # generate audio from text
        text_prompt = f"""
            [ZH]{text_input}[ZH]
        """
        audio_array = generate_audio(text_prompt, language='mix',prompt="yaesakura")
        # voice type seel yaesakura

        # save audio to disk
        write_wav(f"../web-tts/public/voice/{filename}", SAMPLE_RATE, audio_array)

        # play text in notebook
        Audio(audio_array, rate=SAMPLE_RATE)
        print("generate scussece")
        socketio.emit("audio_path",
                  {"message":filename })
        return "generate scussece"
    

    except:
        print("generate fail")
        return "generate fail"

def audio_to_text(user_ID:str)->str:
    # 讀取原始音訊檔案
    original_audio = AudioSegment.from_file(f'recode/user_upload_{user_ID}.wav')

    # 將音訊轉換為PCM格式的WAV
    pcm_audio = original_audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    pcm_audio.export(f'recode/converted_audio_{user_ID}.wav', format='wav')
    # 使用speech_recognition進行語音識別
    r = sr.Recognizer()
    with sr.AudioFile(f'recode/converted_audio_{user_ID}.wav') as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='zh-TW')  # 使用Google Web Speech API進行語音識別
            print(text)
            socketio.emit("text_response",
                  {"message":
                   {
                       "content": text,
                       "type": "user",
                       "user_id":user_ID
                   }})
            return text
            
        except sr.UnknownValueError:
            text = "Google Web Speech API 無法識別音頻"
            print("converted :",text)
            return text
        except sr.RequestError as e:
            text = f"無法從Google Web Speech API獲取結果; {e}"
            print(text)
            return text


def generate_text(user_input:str,user_history:list)->str:
    prompt = user_history
    prompt.append({"role": "user", "content": f"{user_input}"})
    print("prompt: ",prompt)
    client = OpenAI(
        api_key='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'
        
    )
  
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    


    messages=prompt,
    
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    
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
    print(data)
    chat_history  = [{"role": "system", "content": "設計一個說話簡潔、正向、積極的語言模型。此模型提供傾聽與情感支持，擅長回應情緒、提供關心、提供建議，同時她也非常喜歡文學作品與旅遊，必須用30字以內且溫和同理心的文字回答，並避免提及對話者情緒。"}]
    for chat in data['history']:
        reshape = ""
        if chat['type'] == "user":
            reshape = {"role": "user",
                        "content": chat['content']
                    }
        

        else:
            reshape = {"role": "assistant",
                        "content": chat['content']
                    }
        chat_history.append(reshape)



    userID = data['userID']
    print(data['messages'])
    # return_text="測試123"
    return_text =  generate_text(data['messages'],chat_history)
    to_audio(return_text,userID)
    
    socketio.emit("text_response",
                  {"message":
                   {
                       "content": return_text,
                       "type": "bot",
                       "user_id":userID
                   }})


@socketio.on("user_voice_input")
def user_voice_input(data):
    print(data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("missing_file")
        return jsonify({'message': '檔案缺失'}), 400
    file = request.files['file']
    user_ID = request.form.get('userID', 'default_user_id')
    user_history = json.loads(request.form['chatHistory'])

    chat_history  = [{"role": "system", "content": "設計一個說話簡潔、正向、積極且喜愛文學的語言模型。此模型提供傾聽與情感支持，擅長回應情緒，必須用30字以內且溫和同理心的文字回答，並避免提及對話者情緒。"}]
    for chat in user_history:
        reshape = ""
        if chat['type'] == "user":
            reshape = {"role": "user",
                        "content": chat['content']
                    }
        

        else:
            reshape = {"role": "assistant",
                        "content": chat['content']
                    }
        chat_history.append(reshape)


    if file.filename == '':
        print("no_file")
        return jsonify({'message': '沒有選擇檔案'}), 400
    if file:
        filename = f'user_upload_{user_ID}.wav' # 自定義儲存的檔案名稱
        file.save(os.path.join('recode', filename)) # 儲存檔案
        user_input = audio_to_text(user_ID)
        return_text = generate_text(user_input,chat_history)
        to_audio(return_text,user_ID)
        socketio.emit("text_response",
                  {"message":
                   {
                       "content": return_text,
                       "type": "bot",
                       "user_id":user_ID
                   }})
        print("file_is_upload")
        return jsonify({'message': '檔案上傳成功'}), 200
    


if __name__ == '__main__':
    save_path = 'recode'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print("folder creat")
    else:
        print("folder exit")
        
    app.run(debug=True)
