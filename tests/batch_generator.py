from langchain_community.chat_models import ChatTongyi
from langchain_openai import ChatOpenAI

from xiao_qa_generator.formatter.qa_json import QAJsonFormatter
from xiao_qa_generator.generator.batch import BatchGenerator
from xiao_qa_generator.generator.qa import QAGenerator

if __name__ == '__main__':
    chat_model = ChatTongyi(dashscope_api_key="sk-xxx")
    chat_model.model_name = "qwen-plus"

    template_name = "prompt_qa_short_answer.txt"
    generator = QAGenerator(chat_model, template_name=template_name, temperature=1)

    text = """帮会练功活动每天晚上7点准时在帮会城市开始，一直到晚上9点15分之前都能参加哦。少侠等级达到18级后，就能邀约上一位同帮的好兄弟，组成2人小队一同练功啦。
    首先要以两人组队的形式到帮会城市练功师严心（105，114）处报名，报完名之后即可进行练功，练功过程大概会持续3到5分钟。
    少侠在找到同帮派的少侠练功时，最好选择那些和你的等级相差大的少侠进行组队，因为等级相差越大，就能获得更多的经验加成，两个人等级相差5级就能获得最大收益啦！"""

    # Prompt模板参数
    input_variables = {
        "text": text,
        "num_questions": 5
    }

    batch = BatchGenerator(generator, QAJsonFormatter)
    output_dir = r"E:\WorkSpace\GithubWorkSpace\xiao-qa-generator\xiao_qa_generator\output\batch_test"
    batch.generate_batch(1, 3, output_dir, **input_variables)
