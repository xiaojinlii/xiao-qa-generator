import os

import pandas as pd

DEFAULT_SYMBOL = "-"


def handle_single(file_path, output_path: str):
    df = pd.read_excel(file_path)

    all_keys = []
    data_list = df.to_dict(orient='records')
    for data in data_list:
        temp_keys = [key for key in data.keys() if data[key] != DEFAULT_SYMBOL]
        all_keys += temp_keys

    unique_keys = [*{*all_keys}]
    unique_keys.remove("document")
    # print(unique_keys)
    unique_keys = sorted(unique_keys)
    # print(unique_keys)

    new_data_list = []
    for data in data_list:
        new_data = {}
        new_data["document"] = data["document"]
        for i in range(len(unique_keys)):
            new_data[f"question{i + 1}"] = data[unique_keys[i]]
        new_data_list.append(new_data)

    new_df = pd.DataFrame(new_data_list)
    new_df.to_excel(output_path, index=False)


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
    file_path = r"C:\Users\xiaojingli\Documents\WXWork\1688853809617503\Cache\File\2024-06\重楼.xlsx"
    output_path = r"C:\Users\xiaojingli\Documents\WXWork\1688853809617503\Cache\File\2024-06\重楼new.xlsx"
    handle_single(file_path, output_path)

    # src_dir = r"E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库多问一答"
    # target_dir = r"E:\WorkSpace\LLMWorkSpace\knowledge_base\tlbb\content\问答库多问一答_new"
    # recursive_search(src_dir, target_dir)
