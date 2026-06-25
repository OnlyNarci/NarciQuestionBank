"""
结构化的论文数据
"""
from typing import Optional
from pydantic import Field
from dto.base import BaseDTO


class TextFormat(BaseDTO):
    level: int = Field(1, description="大纲级别")
    font: Optional[str] = Field(None, description="字体，例如SimSun")
    font_size: Optional[int] = Field(None, ge=0, description="字号")
    
