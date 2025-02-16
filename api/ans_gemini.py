import requests
import json
import os  # 建议使用环境变量安全地管理 API 密钥

API_KEY = os.environ.get("GEMINI_API_KEY")  #  假设你设置了名为 GEMINI_API_KEY 的环境变量

def generate_text_gemini(prompt_text):
    """
    调用 Gemini 2.0 API 生成文本。

    Args:
        prompt_text (str): 用户输入的提示文本。
        api_key (str): 你的 Gemini API 密钥。

    Returns:
        str: Gemini 模型生成的文本回复，如果出错则返回 None。
    """
    api_key = API_KEY
    if not api_key:
        print("请先设置 GEMINI_API_KEY 环境变量!")
        exit()
    # 1. API Endpoint (根据官方文档确认，这里是示例，可能需要更新)
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"  #  gemini-pro 是文本模型

    # 2. 请求头 (Headers) -  通常需要 API 密钥
    headers = {
        "Content-Type": "application/json",
    }

    # 3. 请求体 (Request Body) -  根据 Gemini API 的请求格式构建 JSON 数据
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}  #  将用户提示文本放入 "text" 字段
                ]
            }
        ],
        "generationConfig": {  #  可选的生成配置参数，可以根据需求调整
            "maxOutputTokens": 200,  #  限制最大输出 token 数量
            "temperature": 0.8,      #  调整生成文本的随机性 (0.0 - 1.0)
            "topP": 0.9,             #  Top-p 采样参数
            "topK": 40              #  Top-k 采样参数
        },
        # "safetySettings": [...]  #  可选的安全设置，可以根据需求配置
    }

    #  添加 API 密钥作为 URL 参数 (另一种常见的认证方式)
    params = {"key": api_key}

    try:
        # 4. 发送 POST 请求到 API Endpoint
        response = requests.post(api_url, headers=headers, params=params, json=payload)
        response.raise_for_status()  #  检查请求是否成功 (状态码 2xx)

        # 5. 解析 JSON 响应
        response_json = response.json()
        # print(json.dumps(response_json, indent=2, ensure_ascii=False)) #  打印完整 JSON 响应，方便调试

        # 6. 提取生成的文本 (根据 Gemini API 的响应结构，可能需要调整)
        if "candidates" in response_json and response_json["candidates"]:
            candidate = response_json["candidates"][0]  #  通常取第一个候选答案
            if "content" in candidate and "parts" in candidate["content"]:
                parts = candidate["content"]["parts"]
                generated_text = "".join([part["text"] for part in parts if "text" in part]) #  拼接所有文本部分
                return generated_text
            else:
                print("响应 JSON 结构异常，无法找到 'content' 或 'parts' 字段。")
                return None
        else:
            print("响应 JSON 结构异常，无法找到 'candidates' 字段或 candidates 为空。")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API 请求出错: {e}")
        if response is not None:
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}") # 打印详细错误信息
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        print(f"原始响应内容: {response.text if response else 'No response received'}")
        return None
    except Exception as e:
        print(f"其他错误: {e}")
        return None


# ----  调用示例  ----
if __name__ == "__main__":

    user_prompt = "请用简洁的语言解释一下量子计算的基本原理。"
    generated_response = generate_text_gemini(user_prompt)

    if generated_response:
        print("用户提问:", user_prompt)
        print("Gemini 回答:")
        print(generated_response)
    else:
        print("Gemini API 调用失败，请检查错误信息。")