import os
from typing import Optional, Dict, Any, Type

from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_deepseek.chat_models import ChatDeepSeek
from pydantic import BaseModel

from core.exceptions import ProviderException


class DeepSeekResponse:
    """Mock response object to match langchain interface"""

    def __init__(self, content: str, response_metadata: dict = None):
        self.content = content
        self.response_metadata = response_metadata or {}


class DeepSeekProvider:
    """DeepSeek provider using langchain prompt templates"""

    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ProviderException("deepseek", "DeepSeek API key not found")

    def _create_chat_model(self, temperature: float = 0.7, max_tokens: int = 100) -> ChatDeepSeek:
        """Create and configure ChatDeepSeek model"""
        return ChatDeepSeek(
            api_key=self.api_key,
            model="deepseek-chat",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def _create_prompt_template(self, system_prompt: Optional[str] = None) -> ChatPromptTemplate:
        """Create chat prompt template using langchain prompt builders"""
        messages = []

        if system_prompt:
            system_template = SystemMessagePromptTemplate.from_template(system_prompt)
            messages.append(system_template)

        human_template = HumanMessagePromptTemplate.from_template("{user_input}")
        messages.append(human_template)

        return ChatPromptTemplate.from_messages(messages)

    def get_response(
            self,
            prompt: str,
            system_prompt: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 100,
            **kwargs
    ) -> DeepSeekResponse:
        """Get response from DeepSeek using langchain prompt templates"""
        try:
            # Create chat model
            chat_model = self._create_chat_model(temperature, max_tokens)

            # Create prompt template
            prompt_template = self._create_prompt_template(system_prompt)

            # Create output parser
            output_parser = StrOutputParser()

            # Create chain using langchain LCEL (LangChain Expression Language)
            chain = prompt_template | chat_model | output_parser

            # Execute chain with input
            content = chain.invoke({"user_input": prompt})

            # Create response metadata
            response_metadata = {
                "token_usage": {
                    "prompt_tokens": 0,  # DeepSeek may not expose this directly
                    "completion_tokens": 0,
                    "total_tokens": 0
                },
                "model_name": "deepseek-chat",
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            return DeepSeekResponse(content=content, response_metadata=response_metadata)

        except Exception as e:
            raise ProviderException("deepseek", f"Error calling DeepSeek API: {str(e)}")

    def get_response_with_custom_template(
            self,
            template: str,
            input_variables: Dict[str, Any],
            temperature: float = 0.7,
            max_tokens: int = 100
    ) -> DeepSeekResponse:
        """Get response using a custom prompt template"""
        try:
            # Create chat model
            chat_model = self._create_chat_model(temperature, max_tokens)

            # Create custom prompt template
            prompt_template = ChatPromptTemplate.from_template(template)

            # Create output parser
            output_parser = StrOutputParser()

            # Create chain
            chain = prompt_template | chat_model | output_parser

            # Execute chain with input variables
            content = chain.invoke(input_variables)

            # Create response metadata
            response_metadata = {
                "token_usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                },
                "model_name": "deepseek-chat",
                "temperature": temperature,
                "max_tokens": max_tokens,
                "template": template
            }

            return DeepSeekResponse(content=content, response_metadata=response_metadata)

        except Exception as e:
            raise ProviderException("deepseek", f"Error calling DeepSeek API: {str(e)}")

    def get_structured_response(
            self,
            template: str,
            input_variables: Dict[str, Any],
            response_schema: Type[BaseModel],
            temperature: float = 0.7,
            max_tokens: int = None
    ) -> BaseModel:
        """Get structured response using LangChain's with_structured_output"""
        try:
            # Create chat model
            chat_model = self._create_chat_model(temperature, max_tokens)

            # Use LangChain's structured output functionality
            model_with_structure = chat_model.with_structured_output(response_schema)

            # Create custom prompt template
            prompt_template = ChatPromptTemplate.from_template(template)

            # Create chain with structured output
            chain = prompt_template | model_with_structure

            # Execute chain with input variables and get structured response
            structured_result = chain.invoke(input_variables)

            return structured_result

        except Exception as e:
            raise ProviderException("deepseek", f"Error calling DeepSeek API with structured output: {str(e)}")


# Backward compatibility function
def get_deepseek_response(
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 100
) -> DeepSeekResponse:
    """Backward compatibility function for existing code"""
    provider = DeepSeekProvider()
    return provider.get_response(prompt, system_prompt, temperature, max_tokens)
