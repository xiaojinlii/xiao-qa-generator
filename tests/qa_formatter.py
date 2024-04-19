from xiao_qa_generator.formatter.alpaca import AlpacaFormatter
from xiao_qa_generator.formatter.faq import FAQFormatter
from xiao_qa_generator.formatter.qa_json import QAJsonFormatter
from xiao_qa_generator.formatter.qa_jsonl import QAJsonlFormatter

# qas = QAJsonFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.json",
# )
# qas = QAJsonlFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.jsonl",
# )
# qas = AlpacaFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\alpaca.json",
# )
qas = FAQFormatter.load_file(
    file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.faq",
)

print(qas)
for question, answer in qas:
    print(f"Q: {question}")
    print(f"A: {answer}")
    print("---------")


# QAJsonFormatter.export_to_file(
#     output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.json",
#     qas=qas
# )
# QAJsonlFormatter.export_to_file(
#     output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.jsonl",
#     qas=qas
# )
# AlpacaFormatter.export_to_file(
#     output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\alpaca.json",
#     qas=qas
# )
# FAQFormatter.export_to_file(
#     output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.faq",
#     qas=qas
# )
