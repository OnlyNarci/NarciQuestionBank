from typing import TypeVar, List, Optional
from pydantic import Field

from dto.base import BaseDTO


class AgentResponse(BaseDTO):
    """
    用于规范化大模型响应的数据结构
    """
    message: str = Field(default="", description="一句话指出错误原因")


T_AgentResponse = TypeVar('T_AgentResponse', bound=AgentResponse)


class CorrectFormatResponse(AgentResponse):
    """
    纠正错误标题格式、参考文献格式的响应结构结构
    """
    error_words: str = Field(description="格式错误的文本")
    correct_words: str = Field(description="正确格式的同义文本")


class CorrectTypos(AgentResponse):
    """
    纠正单个错别字的响应结构
    """
    typo_index: int = Field(ge=0, description="错别字在文本中的索引")
    typos: str = Field(min_length=1, max_length=1, description="错别字，只能是单字")
    correct_way: str = Field(min_length=1, max_length=1, description="正确的字，只能是单字")


class CorrectTyposResponse(AgentResponse):
    """
    针对一段文本纠正错别字的响应
    """
    correct_typos: Optional[List[CorrectTypos]] = Field(default=None, description="一段文本中所有的错别字，无则为空")


class AgentRequest(BaseDTO):
    """
    用于向agent发起请求的数据结构
    """
    prompt: str = Field(default="", description="针对本次请求的单独提示词")
    

T_AgentRequest = TypeVar('T_AgentRequest', bound=AgentRequest)
    