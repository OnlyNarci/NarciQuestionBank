"""
DTO基础类，继承自pydantic的BaseModel
"""
from pydantic import BaseModel
from typing import Any, Dict


class BaseDTO(BaseModel):
    """
    基础DTO类，提供通用的方法
    """
    
    class Config:
        """
        配置类
        """
        from_attributes = True  # 支持从ORM模型创建
        extra = "forbid"  # 禁止额外字段
        frozen = False  # 允许修改
    
    def __repr__(self) -> str:
        """
        友好的字符串表示
        """
        fields = {k: v for k, v in self.model_dump().items() if v is not None}
        fields_str = ", ".join(f"{k}={v}" for k, v in fields.items())
        return f"{self.__class__.__name__}({fields_str})"
    
    def __str__(self) -> str:
        """
        字符串表示
        """
        return self.__repr__()
    
    def to_dict(self, **kwargs) -> Dict[str, Any]:
        """
        转换为字典
        :param kwargs: 传递给model_dump的参数
        :return: 字典
        """
        return self.model_dump(**kwargs)
    
    @classmethod
    def from_orm(cls, obj: Any) -> "BaseDTO":
        """
        从ORM模型创建DTO
        :param obj: ORM模型实例
        :return: DTO实例
        """
        return cls.model_validate(obj)
    
    def update(self, **kwargs) -> "BaseDTO":
        """
        更新字段
        :param kwargs: 要更新的字段
        :return: 更新后的DTO实例
        """
        return self.model_copy(update=kwargs)
