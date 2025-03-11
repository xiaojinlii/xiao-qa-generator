import os

from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownHeaderTextSplitter

from xiao_qa_generator.formatter.qd_excel import QDExcelFormatter


headers_to_split_on = [
    ("#", "head1"),
    ("##", "head2"),
    ("###", "head3"),
    ("####", "head4"),
]


def load_md(file_path):
    loader = TextLoader(file_path, autodetect_encoding=True)
    docs = loader.load()
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    docs = splitter.split_text(docs[0].page_content)
    return docs


def handle_single(file_path, output_path: str):
    docs = load_md(file_path)

    results = []
    for doc in docs:
        header = doc.metadata.get("head4", None) or doc.metadata.get("head3", None) or doc.metadata.get("head2", None) or doc.metadata.get("head1", None) or ""
        results.append((header, doc.page_content))

    QDExcelFormatter.export_to_file(output_path, results)


def recursive_search(src_dir: str, dst_dir: str):
    os.makedirs(dst_dir, exist_ok=True)

    count = 0
    for root, dirs, files in os.walk(src_dir):
        # print(f"root: {root}")
        # print(f"dirs: {dirs}")
        relative_path = os.path.relpath(root, src_dir)
        current_dst_dir = os.path.join(dst_dir, relative_path)
        # print(f"current_dst_dir: {current_dst_dir}")

        if len(files) > 1:
            os.makedirs(current_dst_dir, exist_ok=True)
        else:
            current_dst_dir = dst_dir
        # print(f"current_dst_dir: {current_dst_dir}")

        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing {file_path}")
            filename, file_extension = os.path.splitext(file)
            target_path = os.path.join(current_dst_dir, f"{filename}.xlsx")
            # print(f"target_path: {target_path}")

            if os.path.exists(target_path):
                print(f"file exists, skip. target_path: {target_path}")
                continue
            handle_single(file_path, target_path)
            count += 1


if __name__ == '__main__':
    # directory_path = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240516'
    # dst_dir = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240516_QD'
    # recursive_search(directory_path, dst_dir)

    file_path = r"C:\Users\xiaojingli\Documents\WXWork\1688853809617503\Cache\File\2024-06\重楼.md"
    out_path = r"C:\Users\xiaojingli\Documents\WXWork\1688853809617503\Cache\File\2024-06\重楼.xlsx"
    handle_single(file_path, out_path)

    # QDExcelFormatter.load_file(r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240516_QD\暗器.xlsx')
