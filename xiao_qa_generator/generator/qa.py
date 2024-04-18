from typing import Dict, Tuple, List

from langchain_core.messages import BaseMessage

from .base import BaseGenerator


class QAGenerator(BaseGenerator):

    def _parse(self, response: BaseMessage) -> Dict:
        content = response.content
        token_usage = response.response_metadata["token_usage"]

        questions, answers = self._parse_qa(content)
        assert len(questions) == len(answers), "Parsing error: Unequal question answer count"
        return {
            "question_answers": list(zip(questions, answers)),
            "token_usage": token_usage,
        }

    def _parse_qa(self, response_text: str) -> Tuple[List[str], List[str]]:
        q_prefix, a_prefix = "[Q]: ", "[A]: "
        last_updated = None
        questions, answers = [], []
        for line in response_text.split("\n"):
            if line.startswith(q_prefix):
                questions.append(line[len(q_prefix):])
                last_updated = "Q"
            elif line.startswith(a_prefix):
                answers.append(line[len(a_prefix):])
                last_updated = "A"
            else:  # Q or A spread across multiple lines
                assert last_updated is not None, "Parsing error: First line must be a question"
                if last_updated == "Q":
                    questions[-1] += "\n" + line
                else:
                    answers[-1] += "\n" + line
        return questions, answers


async def main():
    from langchain_community.chat_models import ChatTongyi
    qwen_model = ChatTongyi(model_name="qwen-turbo", dashscope_api_key="sk-xxx")

    template_name = "prompt_qa_short_answer.txt"
    # template_name = "prompt_qa_long_answer.txt"
    # template_name = "prompt_qa_summary.txt"
    # template_name = "prompt_qa_boolean.txt"
    qa_generator = QAGenerator(qwen_model, template_name=template_name)

    text = """帮会练功活动每天晚上7点准时在帮会城市开始，一直到晚上9点15分之前都能参加哦。少侠等级达到18级后，就能邀约上一位同帮的好兄弟，组成2人小队一同练功啦。
    首先要以两人组队的形式到帮会城市练功师严心（105，114）处报名，报完名之后即可进行练功，练功过程大概会持续3到5分钟。
    少侠在找到同帮派的少侠练功时，最好选择那些和你的等级相差大的少侠进行组队，因为等级相差越大，就能获得更多的经验加成，两个人等级相差5级就能获得最大收益啦！"""
    result = await qa_generator.generate_async(text=text, num_questions=5)
    # result = await qa_generator.generate_async(text=text, num_words=50)  # use prompt_qa_summary.txt
    print(f"token_usage: {result['token_usage']}")
    print("---------")
    for question, answer in result["question_answers"]:
        print(f"Q: {question}")
        print(f"A: {answer}")
        print("---------")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
