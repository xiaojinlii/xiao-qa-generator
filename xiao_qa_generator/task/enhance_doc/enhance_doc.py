import os

from langchain_community.chat_models import ChatTongyi
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

from xiao_qa_generator.generator.qa import QAGenerator

headers_to_split_on = [
    ("#", "head1"),
    ("##", "head2"),
    ("###", "head3"),
    ("####", "head4"),
]

qwen_model = ChatTongyi(model_name="qwen-plus", dashscope_api_key="sk-40259aa4a43848eb90cf24daee8225e4")


def load_md(file_path):
    loader = TextLoader(file_path, autodetect_encoding=True)
    docs = loader.load()
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    docs = splitter.split_text(docs[0].page_content)

    all_docs = []
    for doc in docs:
        # print(doc)
        content = ""
        for i in range(1, 5):
            head = doc.metadata.get(f"head{i}", None)
            if head:
                content += f"{'#'*i} {head}\n"
        content += doc.page_content
        # print(content)
        all_docs.append(content)
    return all_docs


def handle_single(file_path):
    docs = load_md(file_path)

    for doc in docs:
        print("----------")
        print(doc)

        template_name = "prompt_qa_short_answer.txt"
        # template_name = "prompt_qa_long_answer.txt"
        qa_generator = QAGenerator(qwen_model, template_name=template_name)
        result = qa_generator.generate(text=doc, num_questions=5)
        for question, answer in result["output"]:
            print(f"Q: {question}")
            print(f"A: {answer}")
            print("---------")


def recursive_search(src_dir: str, dst_dir: str):
    for root, dirs, files in os.walk(src_dir):
        print(f"root: {root}")
        print(f"dirs: {dirs}")
        # relative_path = os.path.relpath(root, src_dir)
        # current_dst_dir = os.path.join(dst_dir, relative_path)
        # print(f"current_dst_dir: {current_dst_dir}")
        for file in files:
            relative_path = os.path.relpath(root, src_dir)
            print(f"relative_path: {relative_path}")
            # print(f"file: {file}")


if __name__ == '__main__':
    # directory_path = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314'
    # dst_dir = r'E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240314_qq'
    # recursive_search(directory_path, dst_dir)

    file_path = r"E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库20240516\帮会\帮会.md"
    handle_single(file_path)


