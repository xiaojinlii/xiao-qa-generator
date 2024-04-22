from xiao_qa_generator.formatter.alpaca import AlpacaFormatter
from xiao_qa_generator.formatter.qa_json import QAJsonFormatter

if __name__ == "__main__":
    input_path = r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.json"
    output_path = r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas_alpaca.json"

    results = QAJsonFormatter.load_file(file_path=input_path)
    AlpacaFormatter.export_to_file(output_path=output_path, inputs=results)
