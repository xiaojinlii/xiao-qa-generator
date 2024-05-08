from xiao_qa_generator.formatter.alpaca import AlpacaFormatter
from xiao_qa_generator.formatter.qa_json import QAJsonFormatter

instruction = "将以下问题拆分为多个子问题，每个子问题之间用<|sep|>分隔。如果子问题中包含代词（如它、他、他们等），拆分后的子问题需将代词替换为对应的实体。"


results = QAJsonFormatter.load_file(
    file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\temp\questions_split\qas_symbols.json",
)


for question, answer in results:
    print(f"Q: {question}")
    print(f"A: {answer}")


AlpacaFormatter.export_instruction_to_file(
    instruction=instruction,
    output_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\datasets\questions_split\alpaca_questions_split_1k_symbols.json",
    inputs=results
)
