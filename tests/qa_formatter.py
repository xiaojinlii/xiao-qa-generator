from xiao_qa_generator.formatter.alpaca import AlpacaFormatter
from xiao_qa_generator.formatter.faq import FAQFormatter
from xiao_qa_generator.formatter.qa_csv import QACSVFormatter
from xiao_qa_generator.formatter.qa_excel import QAExcelFormatter
from xiao_qa_generator.formatter.qa_json import QAJsonFormatter
from xiao_qa_generator.formatter.qa_jsonl import QAJsonlFormatter

# qas = QAJsonFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.json",
# )
# qas = QAJsonlFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\qa.jsonl",
# )
# qas = AlpacaFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\alpaca.json",
# )
# qas = FAQFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.json",
# )
# qas = QAExcelFormatter.load_file(
#     file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.xlsx",
# )
qas = QACSVFormatter.load_file(
    file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.csv",
    encoding="ansi"
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
# QAExcelFormatter.export_to_file(
#     output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.xlsx",
#     inputs=qas
# )
# QACSVFormatter.export_to_file(
#     output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.csv",
#     inputs=qas,
#     encoding="ansi"
# )
