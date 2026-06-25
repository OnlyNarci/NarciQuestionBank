from pydantic import Field
from typing import Literal
from pathlib import Path
from dto.base import BaseDTO


class OpenAISettings(BaseDTO):
    """OpenAI模型配置"""
    api_key: str = Field(default="your_api_key_here", description="API密钥")
    model_name: str = Field(default="gpt-3.5-turbo", description="模型名称")
    temperature: float = Field(default=0.7, ge=0, le=1, description="温度参数")


class LlmSettings(BaseDTO):
    """DeepSeek模型配置"""
    id: int = Field(default=0, description="模型在数据表中的唯一索引")
    model_name: str = Field(default="deepseek-chat", description="模型名称")
    api_key: str = Field(default="your_api_key_here", description="API密钥")
    base_url: str = Field(default="https://api.deepseek.com/v1", decription="模型地址")
    temperature: float = Field(default=0.7, ge=0, le=1, description="温度参数")


class WindowSettings(BaseDTO):
    """窗口配置"""
    height: int = Field(default=800, ge=0, description="窗口高度")
    center_width: int = Field(default=1200, ge=0, description="中央窗口宽度")
    left_width: int = Field(default=400, ge=0, description="左侧窗口宽度")
    right_width: int = Field(default=400, ge=0, description="右侧窗口宽度")


class InterfaceSettings(BaseDTO):
    """界面配置"""
    theme: Literal["light", "dark"] = Field(default="light", description="主题")
    window: WindowSettings = Field(default_factory=WindowSettings, description="窗口配置")


class PathsSettings(BaseDTO):
    """路径配置"""
    data_dir: Path = Field(default=Path("data"), description="数据目录")
    db_path: Path = Field(default=Path("data/db/agent_format.db"), description="数据库文件路径")
    temp_dir: Path = Field(default=Path("temp"), description="临时文件目录")
    log_dir: Path = Field(default=Path("logs"), description="日志目录")
    static_dir: Path = Field(default=Path('static'), description="静态资源目录")
    prompt_dir: Path = Field(default=Path("static/prompt"), description="提示词目录")
    

class AppSetting(BaseDTO):
    """配置数据类"""
    llm: LlmSettings = Field(default_factory=LlmSettings, description="大模型配置")
    interface: InterfaceSettings = Field(default_factory=InterfaceSettings, description="界面配置")
    paths: PathsSettings = Field(default_factory=PathsSettings, description="路径配置")
