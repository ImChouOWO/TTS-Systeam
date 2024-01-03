from utils.generation import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

def to_audio(text_input:str,user_id:str)->str:


    try:
        # download and load all models
        preload_models()

        # generate audio from text
        text_prompt = f"""
            [ZH]{text_input}[ZH]
        """
        audio_array = generate_audio(text_prompt, language='mix',prompt="yaesakura")
        # voice type seel yaesakura

        # save audio to disk
        write_wav(f"backEnd/recode/converted_audio_{user_id}.wav", SAMPLE_RATE, audio_array)

        # play text in notebook
        Audio(audio_array, rate=SAMPLE_RATE)
        return "generate scussece"
    

    except:
        return "generate fail"
    

if __name__ =="__main__":
    to_audio("測試","123")
