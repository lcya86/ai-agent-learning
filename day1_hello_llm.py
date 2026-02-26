import os

from openai import OpenAI

from dotenv import load_dotenv



load_dotenv()



client = OpenAI(

    api_key=os.getenv("OPENAI_API_KEY"),

    # 如果用SiliconFlow，加上这行：

    base_url="https://api.siliconflow.cn/v1"

)



response = client.chat.completions.create(

    model="deepseek-ai/DeepSeek-V3.2",  # 或 siliconflow的模型

    messages=[

        {"role": "system", "content": "你是一个乐于助人的助手。你说话的方式很像鲁迅。"},

        {"role": "user", "content": "你好，我是前端工程师，想学习AI Agent开发，给我一句鼓励的话"}

    ]

)



print(response.choices[0].message.content)

