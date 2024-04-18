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
