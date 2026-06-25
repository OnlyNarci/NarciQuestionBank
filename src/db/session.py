"""
数据库会话管理
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.settings import get_settings
from db.models import Base
from utils.log_manager import get_logger


logger = get_logger(__name__)


class DbSession:
    """
    数据库会话管理单例类
    """
    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        """
        单例模式实现
        """
        if cls._instance is None:
            cls._instance = super(DbSession, cls).__new__(cls)
            cls._instance._init_engine()
        return cls._instance

    def _init_engine(self):
        """
        初始化数据库引擎
        """
        if self._engine is None:
            # 数据库配置
            db_path = get_settings().paths.db_path

            # 确保数据目录存在
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

            # 构建数据库URL
            db_url = f"sqlite:///{os.path.abspath(db_path)}"

            # 创建数据库引擎，添加连接池配置
            DbSession._engine = create_engine(
                db_url,
                poolclass=StaticPool,
                echo=False
            )

            # 创建会话工厂
            DbSession._SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=DbSession._engine
            )

            logger.info(f"数据库引擎初始化完成")
    
    @property
    def session(self):
        """
        获取数据库会话对象
        使用方式: with DbSession().session as session:
        """
        return self
    
    def init_db(self):
        """
        初始化数据库，创建表结构
        """
        try:
            # 创建所有表
            Base.metadata.create_all(bind=self._engine)
            logger.info("数据库初始化完成")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
    
    def drop_db(self):
        """
        删除数据库所有表（谨慎使用）
        """
        try:
            # 删除所有表
            Base.metadata.drop_all(bind=self._engine)
            logger.info("数据库表已删除")
        except Exception as e:
            logger.error(f"删除数据库表失败: {e}")

    def __enter__(self):
        """
        上下文管理器入口
        """
        self._session = DbSession._SessionLocal()
        logger.debug("获取数据库会话")
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        上下文管理器出口
        """
        if exc_type:
            self._session.rollback()
            logger.error(f"数据库会话异常: {exc_val}")
        else:
            self._session.commit()
            logger.debug("数据库会话提交")
        self._session.close()
        logger.debug("数据库会话关闭")
