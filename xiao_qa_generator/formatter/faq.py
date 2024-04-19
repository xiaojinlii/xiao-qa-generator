import json
from typing import List, Tuple

from .base import BaseFormatter

QA_SEP = '====='


class FAQFormatter(BaseFormatter):

    @staticmethod
    def export_to_file(output_path: str, inputs: List[Tuple[str, str]], encoding: str = 'utf-8') -> None:
        """
        导出文件
        :param output_path:输出文件路径，文件格式为faq
        :param inputs:问答对
        :param encoding:编码格式
        """
        length = len(inputs)
        with open(output_path, 'w', encoding=encoding) as file:
            count = 1
            for question, answer in inputs:
                qa = "question: " + question + "\nanswer: " + answer
                if count < length:
                    qa += "\n" + QA_SEP + "\n"
                file.write(qa)
                count += 1

    @staticmethod
    def load_file(file_path: str, encoding: str = 'utf-8') -> List[Tuple[str, str]]:
        """
        加载文件
        :param file_path:文件路径，文件格式为faq
        :param encoding:编码格式
        """
        with open(file_path, 'r', encoding=encoding) as file:
            text = file.read()

        results = []
        arr = text.split(QA_SEP)
        for item in arr:
            question, answer = item.strip().split("\n", 1)
            question = question.replace("question: ", "")
            answer = answer.replace("answer: ", "")
            results.append((question, answer))

        return results
