from langchain_community.chat_models import ChatTongyi
from xiao_qa_generator.generator.conversation import ConversationGenerator


async def main():
    qwen_model = ChatTongyi(model_name="qwen-turbo", dashscope_api_key="sk-xxx")
    conv_generator = ConversationGenerator(qwen_model)

    text = """帮会练功活动每天晚上7点准时在帮会城市开始，一直到晚上9点15分之前都能参加哦。少侠等级达到18级后，就能邀约上一位同帮的好兄弟，组成2人小队一同练功啦。
    首先要以两人组队的形式到帮会城市练功师严心（105，114）处报名，报完名之后即可进行练功，练功过程大概会持续3到5分钟。
    少侠在找到同帮派的少侠练功时，最好选择那些和你的等级相差大的少侠进行组队，因为等级相差越大，就能获得更多的经验加成，两个人等级相差5级就能获得最大收益啦！"""
    result = await conv_generator.generate_async(text=text, num_questions=5)
    print(f"token_usage: {result['token_usage']}")
    print("---------")
    for question, answer in result["question_answers"]:
        print(f"Q: {question}")
        print(f"A: {answer}")
        print("---------")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
