import json
from typing import List, Tuple

from .base import BaseFormatter


class AlpacaFormatter(BaseFormatter):

    @staticmethod
    def export_to_file(output_path: str, inputs: List[Tuple[str, str]], encoding: str = 'utf-8') -> None:
        """
        导出文件
        :param output_path:输出文件路径，文件格式为json
        :param inputs:问答对
        :param encoding:编码格式
        """
        results = [{"instruction": question, "input": "", "output": answer} for question, answer in inputs]

        with open(output_path, 'w', encoding=encoding) as file:
            json.dump(results, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_file(file_path: str, encoding: str = 'utf-8') -> List[Tuple[str, str]]:
        """
        加载文件
        :param file_path:文件路径，文件格式为json
        :param encoding:编码格式
        """
        with open(file_path, 'r', encoding=encoding) as file:
            qas = json.load(file)

        results = [(qa['instruction'], qa['output']) for qa in qas]
        return results
