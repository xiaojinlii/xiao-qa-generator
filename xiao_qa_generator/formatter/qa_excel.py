from typing import List, Tuple

import pandas as pd

from .base import BaseFormatter


class QAExcelFormatter(BaseFormatter):

    @staticmethod
    def export_to_file(output_path: str, inputs: List[Tuple[str, str]], encoding: str = 'utf-8') -> None:
        """
        导出文件
        :param output_path:输出文件路径，文件格式为xlsx
        :param inputs:问答对
        :param encoding:编码格式
        """
        results = [{"question": question, "answer": answer} for question, answer in inputs]
        df = pd.DataFrame(results)
        df.to_excel(output_path, index=False)

    @staticmethod
    def load_file(file_path: str, encoding: str = 'utf-8', sheet_name: str = "Sheet1") -> List[Tuple[str, str]]:
        """
        加载文件
        :param file_path:文件路径，文件格式为xlsx
        :param encoding:编码格式
        :param sheet_name: sheet
        """
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data_list = df.to_dict(orient='records')
        results = [(qa['question'], qa['answer']) for qa in data_list]
        return results
