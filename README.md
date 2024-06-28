## 簡介/Introduction

透過Local LLM、RAG、TTS、STT等技術所完成的專案 
> This project was made by Local LLM、RAG、TTS and STT

>[!NOTE]
>此項專案利用Meta 提出的llama_cpp套件引用 Hugging face 中的 pre-trained model(Mistral 7B)
>
>[pre-trained model](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)
>### Pytorch
>建議安裝CUDA版本
>
> recommend running this project using the CUDA version of PyTorch.

>[!important]
>llama_cpp 使用教學
>
>llama_cpp tutorial
>
>[Run Llama 2 Locally with python](https://swharden.com/blog/2023-07-29-ai-chat-locally-with-python/)

>*權重/weight*
>
>[mistral-7b-instruct-v0.1.Q3_K_M.gguf](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q3_K_M.gguf)
>
>將下載的權重放置於
>Place your weight under the LLM_weight
>```bash
>TTS-System
>    └──backEnd
>          └──LLM_weight
>                └── .gguf file
>```
>

**預覽/preview**
>[!NOTE]
> ### 基礎使用
> 使用者可以透過文字輸入或語音輸入與系統互動，系統會以語音加文字的方式進行回饋
>
>Users can interact with the system by speaking or typing, and will receive feedback through voice and text.
>### RAG
>使用者可以透過上傳TXT檔的方式使系統回答得更加準確
>Users can get hight qulity response by upload txt file.
>
>### Embedding
>
>Sentence Transformers：[sentence_transformers](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
>
>這項專案使用 sentence_transformers 作為詞向量轉換的套件
>
>This project leverages the Sentence Transformers to embed the text.







![preview](https://github.com/ImChouOWO/TTS-Systeam/blob/main/img/img%201.png)



## 引用專案/inference

> [!NOTE]
> [**VALL-E-X**](https://github.com/Plachtaa/VALL-E-X)


##如何執行/How to run this project

💡 **為了確保語音合成相關功能可以使用，請先Clone [VALL-E-X](https://github.com/Plachtaa/VALL-E-X) 中的專案自行測試**
> Clone  [VALL-E-X](https://github.com/Plachtaa/VALL-E-X)  and make sure you can run this project!!!

💡 **需確保能夠正常啟用React.JS相關專案**
> make sure React.JS can be use!!!

💡 **需安裝FFMPEG相關檔案**
> need to download FFMPEG

### 進入專案/Enter the project
```bash
cd TTS-Systeam
```
### 創建虛擬環境
```bash
python -m venv env
```
> [!NOTE]
> 激活虛擬環境

> Unix/macOS
```bash
source env/bin/activate
```
> Windows
```bash
.\env\Scripts\activate 
```
### 安裝依賴包

```bash
pip install -r requirements.txt
```
### 啟動後端伺服器/activate backend server
> 這部份需要兩個 Terminal，分別用於前端與後端
> 
> This part need tow Terminal,one for backend, the other for front

```bash
cd backEnd
```

```bash
python main.py
```

### 啟動前端UI/activate front UI

```bash
cd web-tts
```

```bash
npm start
```
