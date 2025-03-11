import os

from langchain_community.chat_models import ChatTongyi
from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownHeaderTextSplitter
from tqdm import tqdm

from xiao_qa_generator.formatter.qa_json import QAJsonFormatter
from xiao_qa_generator.generator.base import BaseGenerator
from xiao_qa_generator.generator.qa import QAGenerator

headers_to_split_on = [
    ("#", "head1"),
    ("##", "head2"),
    ("###", "head3"),
    ("####", "head4"),
]

model = ChatTongyi(model_name="qwen-max", dashscope_api_key="sk-xxx")

def load_md(file_path):
    loader = TextLoader(file_path, autodetect_encoding=True)
    docs = loader.load()
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    docs = splitter.split_text(docs[0].page_content)

    all_docs = []
    for doc in docs:
        all_docs.append(doc.page_content)
    return all_docs


def handle_single(file_path, output_path: str):
    docs = load_md(file_path)

    results = []
    for doc in tqdm(docs):
        # print("----------")
        # print(f"input: {doc}")

        # template_name = "prompt_qa_short_answer.txt"
        template_name = "prompt_zts\prompt_zts_summary.txt"
        generator = BaseGenerator(model, template_name=template_name)
        output = generator.generate(text=doc)
        # print(f"output: {output}")
        results.append((doc, output["output"]))

    QAJsonFormatter.export_to_file(output_path, results)


def recursive_search(src_dir: str, dst_dir: str):
    os.makedirs(dst_dir, exist_ok=True)

    count = 0
    for root, dirs, files in os.walk(src_dir):
        # print(f"root: {root}")
        # print(f"dirs: {dirs}")
        # relative_path = os.path.relpath(root, src_dir)
        # current_dst_dir = os.path.join(dst_dir, relative_path)
        # print(f"current_dst_dir: {current_dst_dir}")
        for file in files:
            relative_path = os.path.relpath(root, src_dir)
            # print(f"relative_path: {relative_path}")
            # target_dir = os.path.join(dst_dir, relative_path)
            # os.makedirs(target_dir, exist_ok=True)
            # print(f"file: {file}")
            file_path = os.path.join(root, file)
            print(f"Processing {file_path}")
            filename, file_extension = os.path.splitext(file)
            target_path = os.path.join(dst_dir, f"{filename}.json")
            # print(f"target_path: {target_path}")

            if os.path.exists(target_path):
                print(f"file exists, skip. target_path: {target_path}")
                continue
            handle_single(file_path, target_path)
            count += 1


if __name__ == '__main__':
    directory_path = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314'
    dst_dir = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314_QA'
    recursive_search(directory_path, dst_dir)

    # file_path = r"E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314\宝石\宝石.md"
    # handle_single(file_path)
