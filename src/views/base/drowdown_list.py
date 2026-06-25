"""
下拉列表组件
"""
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from views.base.styles import COLORS


class BaseDropdownList(QComboBox):
    """
    下拉列表基类
    """
    
    def __init__(self, parent=None):
        """
        初始化下拉列表
        
        Args:
            parent: 父组件
        """
        super().__init__(parent)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化属性
        self._init_properties()
    
    def _apply_styles(self):
        """
        应用样式
        """
        # 定义下拉列表样式
        style = f"""
        QComboBox {{
            font-family: Arial, sans-serif;
            font-size: 12px;
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 8px 12px;
            background-color: {COLORS['background']};
            color: {COLORS['text']};
            min-height: 36px;
        }}
        QComboBox:hover {{
            border-color: {COLORS['primary_dark']};
            background-color: {COLORS['primary']};
        }}
        QComboBox:focus {{
            border-color: {COLORS['primary_dark']};
            outline: none;
            box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left-width: 1px;
            border-left-color: {COLORS['border']};
            border-left-style: solid;
            border-top-right-radius: 8px;
            border-bottom-right-radius: 8px;
            background-color: {COLORS['primary_light']};
        }}
        QComboBox::down-arrow {{
            image: url(:/icons/down_arrow.png);
            width: 16px;
            height: 16px;
        }}
        QComboBox QAbstractItemView {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 5px;
            background-color: {COLORS['background']};
            selection-background-color: {COLORS['primary_dark']};
            selection-color: {COLORS['background']};
            font-family: Arial, sans-serif;
            font-size: 12px;
        }}
        """
        
        self.setStyleSheet(style)
        
        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)
    
    def _init_properties(self):
        """
        初始化属性
        """
        # 设置鼠标指针
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 设置焦点策略
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # 设置可编辑状态
        self.setEditable(False)
        
        # 设置下拉列表属性
        self.setMaxVisibleItems(10)
    
    def add_item(self, text, data=None):
        """
        添加选项
        
        Args:
            text: 选项文本
            data: 选项数据
        """
        self.addItem(text, data)
    
    def add_items(self, items):
        """
        添加多个选项
        
        Args:
            items: 选项列表
        """
        self.addItems(items)
    
    def set_current_item(self, index):
        """
        设置当前选中项
        
        Args:
            index: 选中项索引
        """
        self.setCurrentIndex(index)
    
    def get_current_text(self):
        """
        获取当前选中项文本
        
        Returns:
            当前选中项文本
        """
        return self.currentText()
    
    def get_current_data(self):
        """
        获取当前选中项数据
        
        Returns:
            当前选中项数据
        """
        return self.currentData()
    
    def clear_items(self):
        """
        清空所有选项
        """
        self.clear()
