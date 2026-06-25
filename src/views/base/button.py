"""
按钮基类
"""
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from views.base.styles import get_style


class TextButton(QPushButton):
    """
    文本类型按钮（类似于HTML的a标签）
    """
    
    def __init__(self, text="", parent=None):
        """
        初始化文本按钮
        
        Args:
            text: 按钮文本
            parent: 父组件
        """
        super().__init__(text, parent)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化属性
        self._init_properties()
    
    def _apply_styles(self):
        """
        应用样式
        """
        # 应用文本按钮样式
        self.setStyleSheet(get_style("text_button"))
        
        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)
    
    def _init_properties(self):
        """
        初始化属性
        """
        # 设置鼠标指针为手形
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 设置焦点策略
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    def set_text(self, text):
        """
        设置按钮文本
        
        Args:
            text: 新的按钮文本
        """
        self.setText(text)
    
    def set_underline(self, underline):
        """
        设置是否显示下划线
        
        Args:
            underline: 是否显示下划线
        """
        font = self.font()
        font.setUnderline(underline)
        self.setFont(font)


class BaseButton(QPushButton):
    """
    传统意义上的按钮
    """
    
    def __init__(self, text="", parent=None):
        """
        初始化传统按钮
        
        Args:
            text: 按钮文本
            parent: 父组件
        """
        super().__init__(text, parent)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化属性
        self._init_properties()
    
    def _apply_styles(self):
        """
        应用样式
        """
        # 应用按钮基础样式
        style = get_style("button")
        
        # 添加悬停和按下状态样式
        style += ""
        """
        QPushButton:hover {
            background-color: #BBDEFB;
            border-color: #2196F3;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        QPushButton:pressed {
            background-color: #2196F3;
            color: #FFFFFF;
            transform: translateY(1px);
        }
        """
        
        self.setStyleSheet(style)
        
        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)
    
    def _init_properties(self):
        """
        初始化属性
        """
        # 设置鼠标指针为手形
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 设置焦点策略
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # 设置默认大小
        self.setMinimumHeight(36)
        self.setMinimumWidth(80)
    
    def set_text(self, text):
        """
        设置按钮文本
        
        Args:
            text: 新的按钮文本
        """
        self.setText(text)
    
    def set_icon(self, icon):
        """
        设置按钮图标
        
        Args:
            icon: 要设置的图标
        """
        self.setIcon(icon)
    
    def set_enabled(self, enabled):
        """
        设置按钮是否可用
        
        Args:
            enabled: 是否可用
        """
        self.setEnabled(enabled)
