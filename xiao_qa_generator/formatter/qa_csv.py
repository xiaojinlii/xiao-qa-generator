from typing import List, Tuple

import pandas as pd

from .base import BaseFormatter


class QACSVFormatter(BaseFormatter):

    @staticmethod
    def export_to_file(output_path: str, inputs: List[Tuple[str, str]], encoding: str = 'ansi') -> None:
        """
        导出文件
        :param output_path:输出文件路径，文件格式为csv
        :param inputs:问答对
        :param encoding:编码格式
        """
        results = [{"question": question, "answer": answer} for question, answer in inputs]
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False, encoding=encoding)

    @staticmethod
    def load_file(file_path: str, encoding: str = 'ansi') -> List[Tuple[str, str]]:
        """
        加载文件
        :param file_path:文件路径，文件格式为json
        :param encoding:编码格式
        """
        df = pd.read_csv(file_path, encoding=encoding)
        data_list = df.to_dict(orient='records')
        results = [(qa['question'], qa['answer']) for qa in data_list]
        return results
