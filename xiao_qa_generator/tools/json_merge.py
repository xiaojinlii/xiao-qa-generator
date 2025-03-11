import json
import os

import chardet


def merge(json_path_list, output_path):
    """
    合并多个json文件到一个新文件中
    """
    all = []
    for json_path in json_path_list:
        with open(json_path, 'rb') as struct_file:
            encode_detect = chardet.detect(struct_file.read())
        with open(json_path, 'r', encoding=encode_detect["encoding"]) as file:
            items = json.load(file)
            all += items

    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(all, out_f, indent=4, ensure_ascii=False)


def merge_dir(input_dir, output_path):
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
    input_dir = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314_QA'
    output_path = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314_QA.json'
    merge_dir(input_dir, output_path)

    # for i in range(1, 61):
    #     path1 = fr"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\questions_split\1\batch_{i}.json"
    #     path2 = fr"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\questions_split\2\batch_{i}.json"
    #     path3 = fr"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\questions_split\3\batch_{i}.json"
    #     merge([path1, path2, path3], fr"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\questions_split\merge123\batch_{i}.json")

    # merge([
    #     r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\temp\questions_split\children_datas\merge123.json",
    #     r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\temp\questions_split\children_datas\identity.json",
    # ], r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\temp\questions_split\qas.json")
