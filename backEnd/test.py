import openai
import os

from openai import OpenAI
client = OpenAI(
    
)
user_message_chinese = '你好啊'
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  
  messages=[
    {"role": "system", "content": "你是一個友善、正向、樂觀、積極的人"},
    {"role": "user", "content": f"'{user_message_chinese}'"}
  ]
)

# 打印出生成的文本内容
if completion.choices:
    generated_message = completion.choices[0].message
    if generated_message:
        print(generated_message.content)
    else:
        print("No message content generated.")
else:
    print("No response generated.")