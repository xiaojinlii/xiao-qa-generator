import json
import os

import chardet


def merge(input_dir, output_path):
    """
    将指定目录下的所有json文件合并成
    """
    all = []
    for filename in os.listdir(input_dir):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'rb') as struct_file:
            encode_detect = chardet.detect(struct_file.read())

        with open(file_path, 'r', encoding=encode_detect["encoding"]) as file:
            items = json.load(file)
            all += items

    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(all, out_f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    input_dir = r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge"
    output_path = r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\merge_qas.json"
    merge(input_dir, output_path)
