from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseFormatter(ABC):
    @staticmethod
    @abstractmethod
    def export_to_file(output_path: str, inputs: List[Tuple[str, str]], encoding: str = 'utf-8'):
        """
        导出文件
        :param output_path:输出文件路径
        :param inputs:输入数据
        :param encoding:编码格式
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def load_file(file_path: str, encoding: str = 'utf-8') -> List[Tuple[str, str]]:
        """
        加载文件
        :param file_path:文件路径，文件格式为faq
        :param encoding:编码格式
        """
        raise NotImplementedError
