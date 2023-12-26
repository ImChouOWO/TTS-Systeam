from pydub import AudioSegment
import speech_recognition as sr

# 設定ffmpeg的路徑（如果它不在您的環境變量中）
# AudioSegment.converter = r"path_to_ffmpeg.exe"

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
    except sr.UnknownValueError:
        print("Google Web Speech API 無法識別音頻")
    except sr.RequestError as e:
        print(f"無法從Google Web Speech API獲取結果; {e}")
