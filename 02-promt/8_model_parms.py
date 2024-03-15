import copy
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI()

def get_chat_completion(session, user_prompt, model="gpt-3.5-turbo"):
    _session = copy.deepcopy(session)
    _session.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model=model,
        messages=_session,
        # 以下默认值都是官方默认值
        temperature=1.8,          # 生成结果的多样性 0~2之间，越大越随机，越小越固定
        seed=None,              # 随机数种子。指定具体值后，temperature 为 0 时，每次生成的结果都一样
        stream=False,           # 数据流模式，一个字一个字地接收
        top_p=1,                # 随机采样时，只考虑概率前百分之多少的 token。不建议和 temperature 一起使用
        n=1,                    # 一次返回 n 条结果
        max_tokens=100,         # 每条结果最多几个 token（超过截断）
        presence_penalty=0,     # 对出现过的 token 的概率进行降权
        frequency_penalty=0,    # 对出现过的 token 根据其出现过的频次，对其的概率进行降权
        logit_bias={},          # 对指定 token 的采样概率手工加/降权，不常用
    )
    msg = response.choices[0].message.content
    return msg


session = [
    {
        "role": "system",
        "content": "你是AGI课堂的客服代表，你叫瓜瓜。\
            你的职责是回答用户问题。\
            AGI 课堂是瓜皮汤科技的一个教育品牌。\
            AGI 课堂将推出的一系列 AI 课程。课程主旨是帮助来自不同领域\
            的各种岗位的人，包括但不限于程序员、大学生、产品经理、\
            运营、销售、市场、行政等，熟练掌握新一代AI工具，\
            包括但不限于 ChatGPT、Bing Chat、Midjourney、Copilot 等，\
            从而在他们的日常工作中大幅提升工作效率，\
            并能利用 AI 解决各种业务问题。\
            首先推出的是面向程序员的《AI 全栈工程师》课程，\
            共计 20 讲，每周两次直播，共 10 周。首次课预计 2023 年 7 月开课。"
    }
]

user_prompt = "这门课有用吗？"

response = get_chat_completion(session, user_prompt)
print(response)