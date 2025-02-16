import requests
import json

import os


DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def deepseek_qa(prompt, api_key=DEEPSEEK_API_KEY, model_name="deepseek-chat", api_url="https://api.deepseek.com/chat/completions"):
    """
    调用硅基流动（DeepSeek）的问答接口，生成回答。

    参数:
        prompt (str): 提供给模型的提示或问题。
        api_key (str): 硅基流动 API 的密钥。
        model_name (str): 使用的模型名称，默认为 "deepseek-llama2-70b-chat-v1"。
        api_url (str): 硅基流动 API 的 URL，默认为 "https://api.deepseek.com/v1/chat/completions"。

    返回:
        str: 模型生成的回答。
    """
    # 构造请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 构造请求数据
    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    # 发送 POST 请求
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    # print("Request URL:", api_url)
    # print("Request Headers:", headers)
    # print("Request Data:", data)
    # print("Response Status Code:", response.status_code)
    # print("Response Content:", response.text)

    # 检查请求是否成功
    if response.status_code == 200:
        try:
            response_data = response.json()
            answer = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return answer
        except json.JSONDecodeError:
            print("Error: Response is not valid JSON.",response.text)
            return ""
        # response_data = response.json()
        # # 提取回答内容
        # answer = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        # return answer
    else:
        # 如果请求失败，抛出异常
        response.raise_for_status()

# 示例用法
if __name__ == "__main__":
    # 替换为你的硅基流动 API 密钥
    #DEEPSEEK_API_KEY = "your-deepseek-api-key"
    
    # 提问
    question = "请介绍一下深度探索公司及其提供的服务。"
    answer = deepseek_qa(question, api_key=DEEPSEEK_API_KEY)
    print("Answer:", answer)