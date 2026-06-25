"""
LLM配置对话框，用于添加和编辑LLM配置
"""
from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QDoubleSpinBox, QWidget, QApplication
)
from PySide6.QtCore import Qt
from langchain_openai import ChatOpenAI

from dto.setting_dto import LlmSettings
from views.base.styles import COLORS
from views.base.button import BaseButton
from views.component.silent_message_box import silent_information, silent_warning
from utils.log_manager import get_logger


logger = get_logger(__name__)


class LLMConfigDialog(QDialog):
    """
    LLM配置对话框，用于添加和编辑LLM配置
    """
    
    def __init__(self, parent: Optional[QWidget] = None, llm_settings: Optional[LlmSettings] = None):
        """
        初始化对话框
        
        :param parent: 父组件
        :param llm_settings: 编辑模式时传入的现有配置，为None表示新建模式
        """
        super().__init__(parent)
        
        self.llm_settings: Optional[LlmSettings] = llm_settings
        self.is_edit_mode: bool = llm_settings is not None
        
        # 设置对话框属性
        self.setWindowTitle("编辑模型配置" if self.is_edit_mode else "添加模型配置")
        self.resize(450, 300)
        self.setMinimumSize(400, 250)
        self.setModal(True)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化UI
        self._init_ui()
        
        # 如果是编辑模式，填充现有数据
        if self.is_edit_mode:
            self._fill_existing_data()
    
    def _apply_styles(self) -> None:
        """
        应用样式
        """
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['background']};
            }}
            QLabel {{
                color: {COLORS['text']};
                font-size: 14px;
                font-weight: bold;
            }}
            QLineEdit {{
                padding: 8px;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['background']};
                color: {COLORS['text']};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['primary_dark']};
            }}
            QDoubleSpinBox {{
                padding: 8px;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['background']};
                color: {COLORS['text']};
                font-size: 13px;
            }}
            QDoubleSpinBox:focus {{
                border-color: {COLORS['primary_dark']};
            }}
        """)
    
    def _init_ui(self) -> None:
        """
        初始化UI组件
        """
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 模型名称输入
        model_name_widget = self._create_input_field(
            "模型名称：", 
            "模型名称",
            "请输入模型名称，例如：deepseek-chat"
        )
        layout.addWidget(model_name_widget)
        self.model_name_input = model_name_widget.findChild(QLineEdit)
        
        # API密钥输入
        api_key_widget = self._create_input_field(
            "API密钥：",
            "API密钥",
            "请输入API密钥"
        )
        layout.addWidget(api_key_widget)
        self.api_key_input = api_key_widget.findChild(QLineEdit)
        
        # 模型地址输入
        base_url_widget = self._create_input_field(
            "模型地址：",
            "模型地址",
            "请输入模型地址，例如：https://api.deepseek.com/v1"
        )
        layout.addWidget(base_url_widget)
        self.base_url_input = base_url_widget.findChild(QLineEdit)
        
        # 温度参数输入
        temperature_widget = self._create_temperature_field()
        layout.addWidget(temperature_widget)
        self.temperature_input = temperature_widget.findChild(QDoubleSpinBox)
        
        # 按钮区域
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(10)
        
        # 左侧：测试连接按钮
        test_button = BaseButton("测试连接")
        test_button.setMinimumWidth(100)
        test_button.clicked.connect(self._on_test_connection)
        button_layout.addWidget(test_button)
        
        # 右侧：保存和取消按钮
        button_layout.addStretch()
        
        save_button = BaseButton("保存")
        save_button.setMinimumWidth(80)
        save_button.clicked.connect(self._on_save)
        
        cancel_button = BaseButton("取消")
        cancel_button.setMinimumWidth(80)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addWidget(button_widget)
    
    def _on_test_connection(self) -> None:
        """
        测试连接按钮点击事件
        """
        if self.test_connection():
            silent_information(self, "成功", "连接测试成功！")
        else:
            silent_warning(self, "失败", "模型名称、API密钥或模型地址可能无效，请检查")
    
    @staticmethod
    def _create_input_field(label_text: str, placeholder: str, tooltip: str) -> QWidget:
        """
        创建输入字段组件
        
        :param label_text: 标签文本
        :param placeholder: 占位符文本
        :param tooltip: 提示文本
        :return: 包含标签和输入框的组件
        """
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 5px;
            }}
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        
        label = QLabel(label_text)
        label.setFixedWidth(80)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setToolTip(tooltip)
        
        layout.addWidget(label)
        layout.addWidget(line_edit)
        
        return widget
    
    @staticmethod
    def _create_temperature_field() -> QWidget:
        """
        创建温度参数输入字段
        
        :return: 包含标签和输入框的组件
        """
        widget = QWidget()
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 5px;
            }}
        """)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        
        label = QLabel("温度参数：")
        label.setFixedWidth(80)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spin_box = QDoubleSpinBox()
        spin_box.setRange(0.0, 1.0)
        spin_box.setSingleStep(0.1)
        spin_box.setDecimals(1)
        spin_box.setValue(0.7)
        spin_box.setToolTip("设置温度参数，范围：0-1")
        
        layout.addWidget(label)
        layout.addWidget(spin_box)
        
        return widget
    
    def _fill_existing_data(self) -> None:
        """
        填充现有数据（编辑模式）
        """
        if self.llm_settings:
            self.model_name_input.setText(self.llm_settings.model_name)
            self.api_key_input.setText(self.llm_settings.api_key)
            self.base_url_input.setText(self.llm_settings.base_url)
            self.temperature_input.setValue(self.llm_settings.temperature)
    
    def _validate_input(self) -> bool:
        """
        验证输入是否有效
        
        :return: True表示有效，False表示无效
        """
        model_name = self.model_name_input.text().strip()
        api_key = self.api_key_input.text().strip()
        base_url = self.base_url_input.text().strip()
        
        # 基本验证：检查是否为空
        if not model_name or not api_key or not base_url:
            return False
        
        return True
    
    def test_connection(self) -> bool:
        """
        测试连接
        
        :return: True表示连接成功，False表示连接失败
        """
        model_name = self.model_name_input.text().strip()
        api_key = self.api_key_input.text().strip()
        base_url = self.base_url_input.text().strip()
        
        # 基本验证
        if not model_name or not api_key or not base_url:
            return False
        
        # 验证模型配置是否可用
        try:
            # 设置等待光标
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            
            # 创建临时连接测试
            test_llm = ChatOpenAI(
                model=model_name,
                base_url=base_url,
                api_key=api_key,
                temperature=0.1,
                timeout=5,
                max_retries=1
            )
            # 发送一个简单的测试消息
            test_llm.invoke("test, reponse as fast as possible")

            # 恢复光标
            QApplication.restoreOverrideCursor()
            logger.info(f"LLM连接测试成功: {model_name}")
            return True
        except Exception as e:
            # 恢复光标
            QApplication.restoreOverrideCursor()
            logger.warning(f'LLM连接测试失败: {model_name}, error: {e}')
            return False
    
    def _on_save(self) -> None:
        """
        保存按钮点击事件
        """
        if not self._validate_input():
            silent_warning(
                self,
                "警告",
                "请填写所有必填字段"
            )
            return

        model_name = self.model_name_input.text().strip()
        # 创建或更新配置
        if self.is_edit_mode:
            self.llm_settings.model_name = model_name
            self.llm_settings.api_key = self.api_key_input.text().strip()
            self.llm_settings.base_url = self.base_url_input.text().strip()
            self.llm_settings.temperature = self.temperature_input.value()
            logger.info(f"保存LLM配置更新: {model_name}, id={self.llm_settings.id}")
        else:
            self.llm_settings = LlmSettings(
                model_name=model_name,
                api_key=self.api_key_input.text().strip(),
                base_url=self.base_url_input.text().strip(),
                temperature=self.temperature_input.value()
            )
            logger.info(f"新建LLM配置: {model_name}")

        self.accept()
    
    def get_llm_settings(self) -> LlmSettings:
        """
        获取配置数据
        
        :return: LLM配置对象
        """
        return self.llm_settings
    