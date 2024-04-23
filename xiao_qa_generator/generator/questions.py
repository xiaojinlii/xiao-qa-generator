from typing import Dict, List

from langchain_core.messages import BaseMessage

from .base import BaseGenerator


class QuestionsGenerator(BaseGenerator):

    def _parse(self, response: BaseMessage) -> Dict:
        content = response.content
        token_usage = response.response_metadata["token_usage"]

        questions = self._parse_content(content)
        return {
            "output": list(zip(questions, questions)),
            "token_usage": token_usage,
        }

    def _parse_content(self, response_text: str) -> List[str]:
        q_prefix = "[Q]: "
        questions = []
        for line in response_text.split("\n"):
            if line.startswith(q_prefix):
                questions.append(line[len(q_prefix):])
            else:
                raise ValueError("Parsing error: line must be a question")
        return questions
