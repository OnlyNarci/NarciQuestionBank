from typing import Type, Optional, Literal, List
from langchain_core.language_models.base import LanguageModelInput, AIMessage
from langchain_openai import ChatOpenAI

from core.settings import get_settings
from db.models import LLMModel
from db.session import DbSession
from dto.setting_dto import LlmSettings
from dto.agent_dto import AgentResponse
from services.base_service import BaseService
from utils.log_manager import get_logger


logger = get_logger(__name__)


class AgentService(BaseService):
    def __init__(self):
        super().__init__()
        self.agent: Optional[LlmSettings] = None
        self.init_agent()
        self.response_format: Optional[Type[AgentResponse]] = None
    
    def init_agent(self) -> None:
        """
        初始化llm连接
        """
        llm_settings = get_settings().llm
        self.agent = ChatOpenAI(
            model=llm_settings.model_name,
            base_url=llm_settings.base_url,
            api_key=llm_settings.api_key,
            temperature=llm_settings.temperature,
        )

    def set_response_format(
        self,
        response_format: Type[AgentResponse],
        method: Literal["function_calling", "json_mode", "json_schema"] = "json_schema",
        strict: bool = True,
    ) -> None:
        """
        设定agent的响应类型
        :param response_format: 期待的返回格式，类本身而非实例
        :param method: 响应类型
        :param strict: 是否强制校验
        """
        self.response_format = response_format
        self.agent.with_structured_output(response_format, method=method, strict=strict)
    
    def get_response_format(self) -> Type[AgentResponse]:
        """
        获取当前的响应类型
        """
        return self.response_format
    
    def invoke(self, message: LanguageModelInput) -> AIMessage:
        """
        向agent发送单条信息
        """
        return self.agent.invoke(message)


class LlmService(BaseService):
    def __init__(self):
        super().__init__()
    
    @classmethod
    def get_llm_settings(cls) -> List[LlmSettings]:
        """
        获取所有可用的LLM连接配置
        :return: 所有可用的LLM连接配置
        """
        logger.info('获取可用LLM连接配置')
        with DbSession().session as session:
            llm_settings = session.query(LLMModel).all()
            return [
                LlmSettings.from_orm(llm_setting_model)
                for llm_setting_model in llm_settings
            ]
    
    @classmethod
    def create_llm_setting(cls, llm_settings: LlmSettings) -> int:
        """
        新建LLM连接配置
        
        :return: 新创建的模型ID
        """
        logger.info(f'新建LLM连接配置: {llm_settings}')
        with DbSession().session as session:
            try:
                llm_model = LLMModel(
                    model_name=llm_settings.model_name,
                    base_url=llm_settings.base_url,
                    api_key=llm_settings.api_key,
                    temperature=llm_settings.temperature,
                )
                session.add(llm_model)
                session.commit()
                # 刷新以获取id
                session.refresh(llm_model)
                return llm_model.id
            except Exception as e:
                logger.error(f'新建LLM连接配置失败: {e}')
                session.rollback()
                raise e
    
    @classmethod
    def update_Llm_setting(cls, llm_setting: LlmSettings) -> int:
        """
        更新指定id的LLM连接配置
        
        :return: 更新后的模型ID
        """
        logger.info(f'更新LLM连接配置: {llm_setting}')
        with DbSession().session as session:
            llm_model = session.query(LLMModel).filter(LLMModel.id == llm_setting.id).first()
            if llm_model:
                llm_model.model_name = llm_setting.model_name
                llm_model.base_url = llm_setting.base_url
                llm_model.api_key = llm_setting.api_key
                llm_model.temperature = llm_setting.temperature
                session.commit()
                return llm_model.id
            else:
                logger.error(f'没有相应id的LLM连接配置，改为新建')
                return cls.create_llm_setting(llm_setting)
    
    @classmethod
    def delete_Llm_setting(cls, llm_id: int) -> None:
        """
        删除指定id的LLM连接配置
        """
        with DbSession().session as session:
            llm_model = session.query(LLMModel).filter(LLMModel.id == llm_id).first()
            if llm_model:
                logger.info(f'删除LLM连接配置: {llm_model}')
                session.delete(llm_model)
                session.commit()
    