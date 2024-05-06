"""
问题：对于子问题之间不使用问号或句号的问题，不会分割
- Q: 你好，你是谁
- Q: 李白是谁，乔峰是谁

处理：
将question中的？随机替换完其他符号
"""

import random

from xiao_qa_generator.formatter.alpaca import AlpacaFormatter

results = AlpacaFormatter.load_file(
    file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\datasets\questions_split\alpaca_questions_split_900.json",
)

symbols = [
    "，", "。", "；", "、", "|", "-", "=", "!", "@", "#", "$", "%", "*", "&", ",", ".", ";", " ", ""
]

new_results = []
for question, answer in results:
    print(f"Q: {question}")
    print(f"A: {answer}")
    split_count = answer.count("<|sep|>")
    print(split_count)

    while split_count >= 1:
        if random.random() < 0.5:  # 概率替换为符号
            s = random.choice(symbols)
            question = question.replace("？", s, 1)
            print(f"Q2: {question}")
        split_count -= 1

    print("---------")
    new_results.append((question, answer))

# for question, answer in new_results:
#     print(f"Q: {question}")
#     print(f"A: {answer}")
#     print("---------")

AlpacaFormatter.export_to_file(
    output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\datasets\questions_split\alpaca_questions_split_900_symbols.json",
    inputs=new_results
)
