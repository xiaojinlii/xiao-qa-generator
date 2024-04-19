from xiao_qa_generator.formatter.sharegpt import ShareGPTFormatter

convs = ShareGPTFormatter.load_file(
    file_path=r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\sharegpt.json"
)

print(convs)
for conv in convs:
    for question, answer in conv:
        print(f"Q: {question}")
        print(f"A: {answer}")
    print("---------")
