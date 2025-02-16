import threading
import requests
# 创建线程列表
import api.ans_deepseek as deepseek
import time
threads = []
prompt = ""
WAIT_TIME_PER_THREAD = 1  # 每个线程等待的时间（秒）
THREAD_PER_CHUNCK = 5  # 每组多少条线程
WAIT_TIME_PER_CHUNCK = 5  # 每组线程等待的时间（秒）
FAIL_RETRY_TIMES = 3  # 失败重试次数

with open('input/prompt.txt', 'r', encoding="utf-8") as pfile:
    prompt = pfile.read()
    print(prompt)

def process_document(doc_txt):
    print(f"Processing document {doc_txt} in thread {threading.current_thread().name}")
    doc_res = deepseek.deepseek_qa(f"{prompt} \n 点子标题如下：{doc_txt}")
    retry_connt = FAIL_RETRY_TIMES
    while doc_res == "":
        if retry_connt == 0:
            break
        print(f"生成失败 重新生成:{retry_connt}")
        retry_connt -= 1
        doc_res = doc_res = deepseek.deepseek_qa(f"{prompt} \n 点子标题如下：{doc_txt}")

    if doc_res != "":    
        with open(f'output/result{threading.current_thread().name[:9]}.txt', 'w', encoding="utf-8") as rfile:
            rfile.write(doc_res)
    else:
        print("生成失败")        
    print(f"Finished processing document {doc_txt} in thread {threading.current_thread().name}")    

with open('input/dian.txt', 'r', encoding="utf-8") as file:
    count  = 0
    for line in file:
        count += 1
        print(line.strip())
        doc_txt = line.strip()
        thread = threading.Thread(target=process_document, args=(doc_txt,))  # 注意这里的逗号
        threads.append(thread)
        thread.start()
        time.sleep(WAIT_TIME_PER_THREAD)
        if count >= THREAD_PER_CHUNCK:
            count = 0
            time.sleep(WAIT_TIME_PER_CHUNCK)
            for thread in threads:
                thread.join()



for thread in threads:
    thread.join()
print("All threads have finished.")

# for doc_txt in threads:
#     result = consult_llm_api(prompt, doc_txt)
#     print(result)