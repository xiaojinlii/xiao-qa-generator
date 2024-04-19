import json
from typing import List, Tuple

from .base import BaseFormatter


class ShareGPTFormatter(BaseFormatter):

    @staticmethod
    def export_to_file(output_path: str, inputs: List[List[Tuple[str, str]]], encoding: str = 'utf-8') -> None:
        """
        导出文件
        :param output_path:输出文件路径，文件格式为json
        :param inputs:对话列表
        :param encoding:编码格式
        """
        conversations = []
        for conv in inputs:
            chat_history = []
            for question, answer in conv:
                chat_history.append({"from": "human", "value": question})
                chat_history.append({"from": "gpt", "value": answer})
            conversations.append(chat_history)
        results = [{"conversations": history} for history in conversations]

        with open(output_path, 'w', encoding=encoding) as file:
            json.dump(results, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_file(file_path: str, encoding: str = 'utf-8') -> List[List[Tuple[str, str]]]:
        """
        加载文件
        :param file_path:文件路径，文件格式为json
        :param encoding:编码格式
        """
        with open(file_path, 'r', encoding=encoding) as file:
            data_dict = json.load(file)

        results = []
        for data in data_dict:
            chat_history = []
            conv_list = data["conversations"]
            half_length = int(len(conv_list) / 2)
            for i in range(half_length):
                conv_human = conv_list[i*2]
                conv_gpt = conv_list[i*2+1]
                # print(i, i*2, i*2+1, conv_human, conv_gpt)
                assert conv_human["from"] == "human"
                assert conv_gpt["from"] == "gpt"
                chat_history.append((conv_human["value"], conv_gpt["value"]))
            results.append(chat_history)

        return results
