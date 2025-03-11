from typing import List, Tuple, Dict

import pandas as pd

from .base import BaseFormatter


class QDExcelFormatter(BaseFormatter):
    # 无效数据的占位符
    DEFAULT_SYMBOL = "-"

    @staticmethod
    def export_to_file(output_path: str, inputs: List[Tuple[str, str]], encoding: str = 'utf-8') -> None:
        """
        导出文件
        :param output_path:输出文件路径，文件格式为xlsx
        :param inputs:问答对
        :param encoding:编码格式
        """
        results = [
            {
                "document": answer,
                "question": question,
                "question1": QDExcelFormatter.DEFAULT_SYMBOL,
                "question2": QDExcelFormatter.DEFAULT_SYMBOL,
                "question3": QDExcelFormatter.DEFAULT_SYMBOL,
                "question4": QDExcelFormatter.DEFAULT_SYMBOL,
                "question5": QDExcelFormatter.DEFAULT_SYMBOL,
                "question6": QDExcelFormatter.DEFAULT_SYMBOL,
                "question7": QDExcelFormatter.DEFAULT_SYMBOL,
                "question8": QDExcelFormatter.DEFAULT_SYMBOL,
                "question9": QDExcelFormatter.DEFAULT_SYMBOL,
            }
            for question, answer in inputs
        ]
        df = pd.DataFrame(results)
        df.to_excel(output_path, index=False)

    @staticmethod
    def load_file(file_path: str, encoding: str = 'utf-8', sheet_name: str = "Sheet1") -> List[Dict]:
        """
        加载文件
        :param file_path:文件路径，文件格式为xlsx
        :param encoding:编码格式
        :param sheet_name: sheet
        """
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data_list = df.to_dict(orient='records')
        return data_list
