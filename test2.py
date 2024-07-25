import requests
import json
import time
from datetime import datetime
from openai import OpenAI

# 定义不同的场景和角色来生成多样化的弹幕
# PROMPTS = [
#     ('公司CEO', '我希望你表现得像公司CEO。我希望你像公司CEO一样回应和回答。不要写任何解释。必须以公司CEO的语气和知识范围为基础。 '),
#     ('项目经理', '我希望你表现得像项目经理。我希望你像项目经理一样回应和回答。不要写任何解释。必须以项目经理的语气和知识范围为基础。 '),
#     ('软件工程师', '我希望你表现得像软件工程师。我希望你像软件工程师一样回应和回答。不要写任何解释。必须以软件工程师的语气和知识范围为基础。 '),
#     ('数据科学家', '我希望你表现得像数据科学家。我希望你像数据科学家一样回应和回答。不要写任何解释。必须以数据科学家的语气和知识范围为基础。 '),
#     ('产品经理', '我希望你表现得像产品经理。我希望你像产品经理一样回应和回答。不要写任何解释。必须以产品经理的语气和知识范围为基础。 '),
#     ('质量保证工程师', '我希望你表现得像质量保证工程师。我希望你像质量保证工程师一样回应和回答。不要写任何解释。必须以质量保证工程师的语气和知识范围为基础。 '),
#     ('系统管理员', '我希望你表现得像系统管理员。我希望你像系统管理员一样回应和回答。不要写任何解释。必须以系统管理员的语气和知识范围为基础。 '),
#     ('IT支持工程师', '我希望你表现得像IT支持工程师。我希望你像IT支持工程师一样回应和回答。不要写任何解释。必须以IT支持工程师的语气和知识范围为基础。 '),
#     ('网络工程师', '我希望你表现得像网络工程师。我希望你像网络工程师一样回应和回答。不要写任何解释。必须以网络工程师的语气和知识范围为基础。 '),
#     ('UI/UX设计师', '我希望你表现得像UI/UX设计师。我希望你像UI/UX设计师一样回应和回答。不要写任何解释。必须以UI/UX设计师的语气和知识范围为基础。 '),
#     ('DevOps工程师', '我希望你表现得像DevOps工程师。我希望你像DevOps工程师一样回应和回答。不要写任何解释。必须以DevOps工程师的语气和知识范围为基础。 '),
#     ('前端开发工程师', '我希望你表现得像前端开发工程师。我希望你像前端开发工程师一样回应和回答。不要写任何解释。必须以前端开发工程师的语气和知识范围为基础。 '),
#     ('后端开发工程师', '我希望你表现得像后端开发工程师。我希望你像后端开发工程师一样回应和回答。不要写任何解释。必须以后端开发工程师的语气和知识范围为基础。 '),
#     ('移动应用开发工程师', '我希望你表现得像移动应用开发工程师。我希望你像移动应用开发工程师一样回应和回答。不要写任何解释。必须以移动应用开发工程师的语气和知识范围为基础。 '),
#     ('全栈开发工程师', '我希望你表现得像全栈开发工程师。我希望你像全栈开发工程师一样回应和回答。不要写任何解释。必须以全栈开发工程师的语气和知识范围为基础。 '),
#     ('机器学习工程师', '我希望你表现得像机器学习工程师。我希望你像机器学习工程师一样回应和回答。不要写任何解释。必须以机器学习工程师的语气和知识范围为基础。 '),
#     ('云计算工程师', '我希望你表现得像云计算工程师。我希望你像云计算工程师一样回应和回答。不要写任何解释。必须以云计算工程师的语气和知识范围为基础。 '),
#     ('区块链开发工程师', '我希望你表现得像区块链开发工程师。我希望你像区块链开发工程师一样回应和回答。不要写任何解释。必须以区块链开发工程师的语气和知识范围为基础。 '),
#     ('嵌入式系统工程师', '我希望你表现得像嵌入式系统工程师。我希望你像嵌入式系统工程师一样回应和回答。不要写任何解释。必须以嵌入式系统工程师的语气和知识范围为基础。 '),
#     ('游戏开发工程师', '我希望你表现得像游戏开发工程师。我希望你像游戏开发工程师一样回应和回答。不要写任何解释。必须以游戏开发工程师的语气和知识范围为基础。 '),
# ]

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    显示进度条
    """
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()
        
def call_openai_format_api(client, prompt):
    # """
    # 调用ollama chatglm API并返回响应
    # """
    # try:
    #     response = requests.post('http://localhost:11434/v1/chat/completions', json={
    #         "model": "glm4",
    #         "messages": [{"role": "user", "content": prompt}]
    #     })
    #     response.raise_for_status()
    #     data = response.json()
    #     return data['choices'][0]['message']['content']
    # except requests.RequestException as e:
    #     print(f"OpenAI API 调用失败: {e}")
    #     return None
    # except (json.JSONDecodeError, KeyError) as e:
    #     print(f"解析API响应失败: {e}")
    #     print(f"响应内容: {response.text}")
    #     return None
    
    # """
    # 调用OpenAI API并返回响应
    # """
    # try:
    #     response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     return response.choices[0].message.content
    # except Exception as e:
    #     print(f"OpenAI API 调用失败: {e}")
    #     return None
    
    """
    调用DeepSeek API并返回响应
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DeepSeek API 调用失败: {e}")
        return None
    
    # """
    # 调用 跃问 API 并返回响应
    # """
    # try:
    #     response = client.chat.completions.create(
    #         model="step-1-8k",
    #         messages=[{"role": "user", "content": prompt}]
    #     )
    #     return response.choices[0].message.content
    # except Exception as e:
    #     print(f"跃问 API 调用失败: {e}")
    #     return None

def generate_danmu_from_json(json_file):
    """
    从给定的JSON文件生成弹幕
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    total_items = len(data)
    # client = OpenAI(
    #     base_url = 'https://api.chatanywhere.tech/v1',
    #     api_key='api_key',
    # )
    
    client = OpenAI(
        base_url = 'https://api.deepseek.com/v1',
        api_key='api_key',
    )
    
    # client = OpenAI(
    #     base_url = 'https://api.stepfun.com/v1',
    #     api_key='api_key',
    # )
    historytext = ""
    # 初始化历史记录字典
    history_thoughts = {character: "" for character, _ in PROMPTS}
    text = ""
    for i, item in enumerate(data):
        time_stamp = item['time']
        description = item['description']
        if text == None:
            text = ""
        historytext = historytext + text
        text=item['text']
        for character, selected_prompt in PROMPTS:
            # prompt = f"{selected_prompt}, 你穿越了时空学会了看电视，看到了以下内容：[{description}]（只关注其中客观的视觉信息，不要被其中的主观信息影响你），请生成一些真实的中文弹幕（100字以内）:'，"
            prompt = (f"{selected_prompt}, 你穿越了时空学会了听收音机，正在听一个采访节目，"
                                f"你已经听了以下内容：[{historytext}]（只关注其中主观的信息，"
                                f"不要被其中的客观信息影响你），采访者现在又说了[{text}]（只关注其中主观的信息，"
                                f"不要被其中的客观信息影响你，请发表你对采访者当前说的话的真实想法（100字以内）: ")  
            # prompt = (f"{selected_prompt}, 你穿越了时空学会了听收音机，正在听一个产品发布节目，"
            #                     f"你已经听了以下内容：[{historytext}]（只关注其中主观的信息，"
            #                     f"不要被其中的客观信息影响你），产品发布者现在又说了[{text}]（只关注其中主观的信息，"
            #                     f"不要被其中的客观信息影响你，请发表你对产品发布者当前说的话的真实想法（100字以内）: ")          
            print("prompt:",prompt)
            danmu = call_openai_format_api(client, prompt)
            print("danmu:", danmu)
            if danmu:
                results.append({
                    "time": time_stamp,
                    "content": danmu,
                    "character": character
                })
                # 更新当前角色的历史记录
                history_thoughts[character] += danmu + ';'
        print_progress_bar(i + 1, total_items, prefix='Progress:', suffix='Complete', length=50)
        # time.sleep(20000)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"danmu_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    return filename

# 示例用法:
json_file = r"C:\Users\17905\Desktop\image_descriptions\image_descriptions_20240724173353.json"  # 替换为实际的JSON文件名
filename = generate_danmu_from_json(json_file)
print(f"弹幕生成结果已保存到 {filename}")
