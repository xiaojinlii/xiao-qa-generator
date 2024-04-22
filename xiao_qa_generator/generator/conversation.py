import os
from typing import Dict, Tuple, List, Optional, Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

from .qa import QAGenerator


class ConversationGenerator(QAGenerator):

    def __init__(
            self,
            chat_model: BaseChatModel,
            temperature: float = 0.7,
            template: Optional[str] = None,
            template_path: Optional[str] = None,
            template_name: Optional[str] = None,
            language: Literal["en", "zh_CN"] = "zh_CN"
    ):
        if template is None and template_path is None and template_name is None:
            template_name = "prompt_qa_conversation.txt"

        super().__init__(
            chat_model,
            temperature=temperature,
            template=template,
            template_path=template_path,
            template_name=template_name,
            language=language
        )

    def _parse(self, response: BaseMessage) -> Dict:
        content = response.content
        token_usage = response.response_metadata["token_usage"]

        questions, answers = self._parse_qa(content)
        assert len(questions) == len(answers), "Parsing error: Unequal question answer count"

        questions, token_usage2 = self._modify_conversation_questions(questions)
        token_usage = self._merge_token_usage(token_usage, token_usage2)

        return {
            "output": list(zip(questions, answers)),
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
            "output": list(zip(questions, answers)),
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
