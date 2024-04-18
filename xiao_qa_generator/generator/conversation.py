import os
from typing import Dict, Tuple, List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

from .qa import QAGenerator


class ConversationGenerator(QAGenerator):

    def __init__(self, chat_model: BaseChatModel):
        super().__init__(chat_model, template_name="prompt_qa_conversation.txt")

    def _parse(self, response: BaseMessage) -> Dict:
        content = response.content
        token_usage = response.response_metadata["token_usage"]

        questions, answers = self._parse_qa(content)
        assert len(questions) == len(answers), "Parsing error: Unequal question answer count"

        questions, token_usage2 = self._modify_conversation_questions(questions)
        token_usage = self._merge_token_usage(token_usage, token_usage2)

        return {
            "question_answers": list(zip(questions, answers)),
            "token_usage": token_usage,
        }

    async def _parse_async(self, response: BaseMessage) -> Dict:
        content = response.content
        token_usage = response.response_metadata["token_usage"]

        questions, answers = self._parse_qa(content)
        assert len(questions) == len(answers), "Parsing error: Unequal question answer count"

        questions, token_usage2 = await self._modify_conversation_questions_async(questions)
        token_usage = self._merge_token_usage(token_usage, token_usage2)

        return {
            "question_answers": list(zip(questions, answers)),
            "token_usage": token_usage,
        }

    def _modify_conversation_questions(self, questions: List[str]) -> Tuple[List[str], Dict]:
        messages = self._get_messages_for_modify_conversation(questions)
        response = self.chat_model.invoke(messages)
        return self._parse_conversation_questions(questions, response)

    async def _modify_conversation_questions_async(self, questions: List[str]) -> Tuple[List[str], Dict]:
        messages = self._get_messages_for_modify_conversation(questions)
        response = await self.chat_model.ainvoke(messages)
        return self._parse_conversation_questions(questions, response)

    def _parse_conversation_questions(self, questions: List[str], response: BaseMessage):
        content = response.content
        token_usage = response.response_metadata["token_usage"]

        modified_questions, _ = self._parse_qa(content)
        # Keep proper nouns in first question of conversation
        modified_questions[0] = questions[0]
        assert len(modified_questions) == len(questions), "Parsing error: Unequal question count after modification"
        return modified_questions, token_usage

    def _get_messages_for_modify_conversation(self, questions: List[str]) -> List:
        modify_template_path = os.path.join(self._TEMPLATES_DIR, "prompt_qa_conversation_modify.txt")
        modify_template = self._get_template(modify_template_path)
        chat_template = self._get_chat_prompt_template(modify_template)
        questions_str = "\n".join([f"[Q]: {q}" for q in questions])
        messages = chat_template.format_messages(questions=questions_str)
        return messages
    def _merge_token_usage(self, token_usage: Dict, token_usage2: Dict) -> Dict:
        return {name: count + token_usage[name] for name, count in token_usage2.items()}


async def main():
    from langchain_community.chat_models import ChatTongyi
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
