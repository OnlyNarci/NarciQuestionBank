"""
日志管理工具
"""
import os
import logging
from datetime import datetime
from typing import Optional

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

# 日志文件名
INFO_LOG_FILE = os.path.join(LOG_DIR, "info_log.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error_log.log")


class LogManager:
    """
    日志管理器
    """

    _loggers = {}

    @classmethod
    def create_logger(cls, name: str) -> logging.Logger:
        """
        创建日志记录器
        
        :param name: 模块名称，通常为__name__
        :return: 日志记录器对象
        """
        # 如果已经创建过该名称的logger，直接返回
        if name in cls._loggers:
            return cls._loggers[name]

        # 创建logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # 解析路径，从src开始
        path = cls._parse_path(name)

        # 创建自定义格式化器
        class CustomFormatter(logging.Formatter):
            def format(self, record):
                record.path = path
                return super().format(record)

        # 创建格式化器
        formatter = CustomFormatter(
            '[%(levelname)s] %(asctime)s %(path)s %(message)s',
            datefmt='%Y%m%d %H:%M:%S'
        )

        # 创建信息日志处理器
        info_handler = logging.FileHandler(INFO_LOG_FILE, encoding='utf-8')
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        # 创建错误日志处理器
        error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # 添加处理器到logger
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

        # 存储logger
        cls._loggers[name] = logger

        return logger

    @staticmethod
    def _parse_path(name: str) -> str:
        """
        解析路径，从src开始
        
        :param name: 模块名称
        :return: 解析后的路径
        """
        # 从name中提取路径，从src开始
        parts = name.split('.')
        if parts and parts[0] == 'src':
            # 如果以src开头，直接返回
            return '.'.join(parts[1:]) if len(parts) > 1 else ''
        else:
            # 否则直接返回name
            return name


# 便捷函数
def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器
    
    :param name: 模块名称，通常为__name__
    :return: 日志记录器对象
    """
    return LogManager.create_logger(name)
