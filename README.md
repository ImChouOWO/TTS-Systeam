## 簡介/Introduction

透過Local LLM、RAG、TTS、STT等技術所完成的專案  
> This project was made by Local LLM、RAG、TTS and STT

**預覽**



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
