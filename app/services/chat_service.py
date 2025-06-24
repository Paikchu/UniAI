from app.providers.deepseek import get_deepseek_response
from app.models.response import ChatResponse, ChatResponseData, ModelInfo, Usage, ErrorResponse
from app.core.config import settings
from app.core.exceptions import ModelNotSupportedException, ProviderException
from app.utils.time_utils import get_current_timestamp

class ChatService:
    @staticmethod
    def process_chat_request(request):
        """Core business logic for processing chat requests"""
        system_prompt = None
        if request.parameters.prompt_id:
            system_prompt = settings.get_prompt(request.parameters.prompt_id)

        if request.model == "deepseek-chat":
            try:
                response_obj = get_deepseek_response(
                    request.parameters.prompt, 
                    system_prompt=system_prompt,
                    temperature=request.parameters.temperature,
                    max_tokens=request.parameters.max_tokens
                )
                
                usage = response_obj.response_metadata.get('token_usage', {})
                
                response_data = ChatResponseData(
                    result=response_obj.content,
                    model_info=ModelInfo(
                        name=request.model,
                        provider="deepseek",
                        version=response_obj.response_metadata.get('model_name', 'unknown')
                    ),
                    usage=Usage(
                        prompt_tokens=usage.get('prompt_tokens', 0),
                        completion_tokens=usage.get('completion_tokens', 0),
                        total_tokens=usage.get('total_tokens', 0)
                    )
                )

                return ChatResponse(
                    data=response_data,
                    request_id=request.request_id,
                    timestamp=get_current_timestamp()
                )
            except Exception as e:
                raise ProviderException("deepseek", str(e))
        
        raise ModelNotSupportedException(request.model)