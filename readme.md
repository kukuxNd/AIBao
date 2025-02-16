# 简易的小红书爆款文案生成器

## 使用方法:
- 配置提示词：
```
    1. 在input/dian.txt 文件 每行输入你的点子
    2. 在input/prompt.txt 输入你的提示词和要求
    3. api/ans_deepseek.py 输入你的api key
 ```
 - 运行启动
```
 python AiBao.py
 ``` 

 - AiBao.py 内配置参数：
 ```
WAIT_TIME_PER_THREAD = 1  # 每个线程等待的时间（秒）
THREAD_PER_CHUNCK = 5  # 每组多少条线程
WAIT_TIME_PER_CHUNCK = 5  # 每组线程等待的时间（秒）
FAIL_RETRY_TIMES = 3  # 失败重试次数
```

- 注意：api接口目前各家稳定性不强，请自行测试，如果有更好的api接口，可以自行替换
