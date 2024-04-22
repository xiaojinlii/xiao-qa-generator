import os
from typing import Any, Type

from tqdm import tqdm

from xiao_qa_generator.formatter.base import BaseFormatter
from xiao_qa_generator.generator.base import BaseGenerator


class BatchGenerator:
    """
    批量生成器
    """
    def __init__(self, generator: BaseGenerator, formatter: Type[BaseFormatter]):
        self.generator = generator
        self.formatter = formatter

    def generate(self, output_path: str, **input_variables: Any):
        result = self.generator.generate(**input_variables)
        self._export_to_file(result["output"], output_path)

    def generate_batch(self, batch_start: int, batch_end: int, output_dir: str, **input_variables: Any):
        for i in tqdm(range(batch_start, batch_end + 1), desc='batch generating'):
            output_path = os.path.join(output_dir, f"batch_{i}.json")
            self.generate(output_path, **input_variables)

    def _export_to_file(self, result, output_path: str):
        self.formatter.export_to_file(
            output_path=output_path,
            inputs=result
        )
