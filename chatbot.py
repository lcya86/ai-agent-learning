# chatbot.py

import os

from openai import OpenAI

from dotenv import load_dotenv



load_dotenv()



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.siliconflow.cn/v1")



# 存储对话历史

messages = [

    {"role": "system", "content": "你是一个乐于助人的AI助手，回答简洁明了。"}

]



print("🤖 聊天机器人已启动（输入 'quit' 或 'exit' 退出）\n")



while True:

    # 1. 获取用户输入

    user_input = input("你: ").strip()

    

    # 2. 检查退出

    if user_input.lower() in ["quit", "exit", "q"]:

        print("👋 再见！")

        break

    

    # 3. 空输入跳过

    if not user_input:

        continue

    

    # 4. 添加用户消息到历史

    messages.append({"role": "user", "content": user_input})

    

    # 5. 调用API

    try:

        response = client.chat.completions.create(

            model="deepseek-ai/DeepSeek-V3.2",

            messages=messages,

            stream=True  # 流式输出，打字机效果

        )

        

        # 6. 流式打印回复

        print("AI: ", end="", flush=True)

        full_reply = ""

        

        for chunk in response:

            if chunk.choices[0].delta.content:

                content = chunk.choices[0].delta.content

                print(content, end="", flush=True)

                full_reply += content

        

        print()  # 换行

        

        # 7. 添加AI回复到历史（保持上下文）

        messages.append({"role": "assistant", "content": full_reply})

        

    except Exception as e:

        print(f"❌ 出错了: {e}")

