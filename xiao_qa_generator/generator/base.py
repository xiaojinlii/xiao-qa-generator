import asyncio
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import Dict, Optional, List, Any, Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate


class BaseGenerator(ABC):

    def __init__(
            self,
            chat_model: BaseChatModel,
            template: Optional[str] = None,
            template_path: Optional[str] = None,
            template_name: Optional[str] = None,
            language: Literal["en", "zh_CN"] = "zh_CN"
    ):
        self.chat_model = chat_model
        self._TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", language)

        if template is not None:
            self.template = template
        elif template_path is not None:
            self.template = self._get_template(template_path)
        elif template_name is not None:
            template_path = os.path.join(self._TEMPLATES_DIR, template_name)
            self.template = self._get_template(template_path)
        else:
            raise ValueError("Value error: template, template_path and template_name must not both be None.")

    def generate(self, **input_variables: Any) -> Dict:
        """
        生成数据
        :param input_variables:对应template中的参数
        """
        messages = self._get_messages(**input_variables)
        response = self.chat_model.invoke(messages)
        return self._parse(response)

    async def generate_async(self, **input_variables: Any) -> Dict:
        """
        异步生成数据
        :param input_variables:对应template中的参数
        """
        messages = self._get_messages(**input_variables)
        response = await self.chat_model.ainvoke(messages)
        return await self._parse_async(response)

    @abstractmethod
    def _parse(self, response: BaseMessage) -> Dict:
        """解析数据"""
        raise NotImplementedError

    async def _parse_async(self, response: BaseMessage) -> Dict:
        """异步解析数据"""
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor()
        result = await loop.run_in_executor(executor, self._parse, response)
        return result

    def _get_messages(self, **input_variables: Any) -> List[BaseMessage]:
        chat_template = self._get_chat_prompt_template(self.template)
        messages = chat_template.format_messages(**input_variables)
        return messages

    def _get_chat_prompt_template(self, template: str) -> ChatPromptTemplate:
        """
        根据模板字符串获取ChatPromptTemplate
        :param template: 模板字符串。从上到下依次为system instructions、few-shot input、few-shot output、input template，每段之间使用<|separator|>分隔
        """
        content_list = [content.strip() for content in template.split("<|separator|>")]
        chat_template = ChatPromptTemplate.from_messages(
            [
                ("system", content_list[0]),  # system instructions
                ("human", content_list[1]),  # few-shot input
                ("ai", content_list[2]),  # few-shot output
                ("human", content_list[3]),  # input template
            ]
        )
        return chat_template

    @lru_cache
    def _get_template(self, filepath) -> str:
        with open(filepath, encoding="utf-8") as f:
            template = f.read()
        return template
