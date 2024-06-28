from flask import Flask, request, jsonify
import os
from pydub import AudioSegment
import speech_recognition as sr
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import openai
from openai import OpenAI
import json
from datetime import datetime
from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from llama_cpp import Llama
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
from sentence_transformers import SentenceTransformer, util
import pickle
import torch
import traceback

# 定義全域變數
RECODE_DIR = 'recode'
WEB_TTS_PUBLIC_VOICE_DIR = '../web-tts/public/voice'
EMBEDDING_FILE_DIR = 'C:/Users/as093/OneDrive/桌面/web/TTS-Systeam/backEnd/embedding_file'
LLM_WEIGHT_DIR = 'C:/Users/as093/OneDrive/桌面/web/TTS-Systeam/backEnd/LLM_weight'
USER_UPLOAD_TXT = 'C:/Users/as093/OneDrive/桌面/web/TTS-Systeam/backEnd/embedding_file/user_upload'

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

def to_audio(text_input: str, user_id: str) -> str:
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"main_video_{user_id}_{timestamp}.wav"
        # download and load all models
        preload_models()

        # generate audio from text
        text_prompt = f"""
            [EN]{text_input}[EN]
        """
        audio_array = generate_audio(text_prompt, language='mix', prompt="yaesakura")
        # voice type seel yaesakura

        # save audio to disk
        write_wav(os.path.join(WEB_TTS_PUBLIC_VOICE_DIR, filename), SAMPLE_RATE, audio_array)

        # play text in notebook
        Audio(audio_array, rate=SAMPLE_RATE)
        print("generate scussece")
        socketio.emit("audio_path", {"message": filename})
        return "generate scussece"
    except Exception as e:
        print("Generate fail")
        print(str(e))
        print(traceback.format_exc())
        return "Generate fail"

def audio_to_text(user_ID: str) -> str:
    original_audio = AudioSegment.from_file(os.path.join(RECODE_DIR, f'user_upload_{user_ID}.wav'))

    # 將音訊轉換為PCM格式的WAV
    pcm_audio = original_audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    pcm_audio.export(os.path.join(RECODE_DIR, f'converted_audio_{user_ID}.wav'), format='wav')
    
    # 使用speech_recognition進行語音識別
    r = sr.Recognizer()
    with sr.AudioFile(os.path.join(RECODE_DIR, f'converted_audio_{user_ID}.wav')) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='zh-TW')  # 使用Google Web Speech API進行語音識別
            print(text)
            socketio.emit("text_response", {"message": {"content": text, "type": "user", "user_id": user_ID}})
            return text
        except sr.UnknownValueError:
            text = "Google Web Speech API 無法識別音頻"
            print("converted :", text)
            return text
        except sr.RequestError as e:
            text = f"無法從Google Web Speech API獲取結果; {e}"
            print(text)
            return text

#no working in this sript
def write_content_not_replace(user_input: str, content_path: str):
    with open(content_path, 'a', encoding='utf-8') as file:
        file.write(user_input + "/n")

def content_embedding(content_path: str, pkl_path: str, is_replace: bool = True):
    contents = []
    with open(content_path, 'r', encoding='utf-8') as file:
        contents = file.readlines()

    contents_embedding = []
    model = SentenceTransformer("all-MiniLM-L6-v2")
    for content in contents:
        contents_embedding.append(model.encode(content))
    with open(pkl_path, 'wb') as pkl_file:
        pickle.dump(contents_embedding, pkl_file)

def cos_similarity(content_path: str, pkl_path: str, user_input: str, top_k: int = 3):
    contents = []
    with open(content_path, "r", encoding='utf-8') as file:
        contents = file.readlines()

    contents_embedding = []
    with open(pkl_path, "rb") as pkl_file:
        contents_embedding = pickle.load(pkl_file)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    input_embedding = model.encode([user_input])
    cos_scores = util.cos_sim(input_embedding, contents_embedding)[0]
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    try:
        relevant_content = [contents[idx].split() for idx in top_indices]
    except :
        relevant_content = [["no information"]]
        
    
    print(f"relevant_content:{relevant_content}")
    tmp = []
    for text in relevant_content:
        tmp.append(text[0])
    relevant_content = tmp
    return relevant_content

#no working in this script
def rebuild_embedding_db(user_input: str):
    try:
        content_path = os.path.join(EMBEDDING_FILE_DIR, 'content.txt')
        pkl_path = os.path.join(EMBEDDING_FILE_DIR, 'embedding.pkl')
        write_content_not_replace(user_input=user_input, content_path=content_path)
        content_embedding(content_path=content_path, pkl_path=pkl_path)
    except Exception as e:
        raise e

def local_llm_generate_text(user_input: str, user_id: str) -> str:
    content_path = os.path.join(USER_UPLOAD_TXT, f'user_upload_{user_id}.txt')
    pkl_path = os.path.join(EMBEDDING_FILE_DIR, 'embedding.pkl')
    relevant_contents = cos_similarity(content_path=content_path, pkl_path=pkl_path, user_input=user_input, top_k=5)
    result = ','.join(relevant_contents)

    LLM = Llama(model_path=os.path.join(LLM_WEIGHT_DIR, "mistral-7b-instruct-v0.1.Q3_K_M.gguf"),
                n_ctx=2048,
                verbose=True)
    prompt = f"""<s>[INST]You are an assistant named Mia. Your role is to provide brief answers to questions using the information you know. Additionally, you will use relevant information about the person asking the question to tailor your responses. Keep your answers concise and speak English.[/INST]
            Information about the person asking: {result}</s>
            [INST]{user_input} [/INST]"""

    output = LLM(prompt, max_tokens=0, temperature=0.4)
    # display the response
    print(output["choices"][0]["text"])
    return output["choices"][0]["text"]

def generate_text(user_input: str, user_history: list) -> str:
    prompt = user_history
    prompt.append({"role": "user", "content": f"{user_input}"})
    print("prompt: ", prompt)
    client = OpenAI(
        api_key='sk-DYpiqVu0F3PbsmOTtlDGT3BlbkFJBk3Z38E5xp2vcprluGg'
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

@app.route('/txt_upload', methods=['POST'])
def user_rag_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    user_id = request.form.get('userID')
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = f"user_upload_{user_id}"
        file_path = os.path.join(EMBEDDING_FILE_DIR, 'user_upload', f"{filename}.txt")
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

    return jsonify({"error": "Invalid file type"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt'}

@socketio.on("user_text_input")
def user_text_input(data):
    print(data)
    userID = data['userID']
    print(data['messages'])
    return_text = local_llm_generate_text(user_input=data['messages'],user_id=userID)
    to_audio(return_text, userID)

    socketio.emit("text_response", {"message": {"content": return_text, "type": "bot", "user_id": userID}})

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
    print(user_ID)

    if file.filename == '':
        print("no_file")
        return jsonify({'message': '沒有選擇檔案'}), 400
    if file:
        filename = f'user_upload_{user_ID}.wav'  # 自定義儲存的檔案名稱
        file.save(os.path.join(RECODE_DIR, filename))  # 儲存檔案
        user_input = audio_to_text(user_ID)
        return_text = local_llm_generate_text(user_input=user_input,user_id=user_ID)
        to_audio(return_text, user_ID)
        socketio.emit("text_response", {"message": {"content": return_text, "type": "bot", "user_id": user_ID}})
        print("file_is_upload")
        return jsonify({'message': '檔案上傳成功'}), 200

if __name__ == '__main__':
    if not os.path.exists(RECODE_DIR):
        os.makedirs(RECODE_DIR)
        print("folder created")
    else:
        print("folder exists")
        
    app.run(debug=True)
