"""
数据表模型，主要是试题数据表和试卷数据表
"""
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LLMModel(Base):
    """
    大模型连接配置
    """
    __tablename__ = 'llm_setting'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    api_key = Column(String)
    base_url = Column(String)
    temperature = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class PaperFormatConfigModel(Base):
    """
    论文格式校验规则配置
    """
    __tablename__ = 'paper_format_config'
    id = Column(Integer, primary_key=True)
    
