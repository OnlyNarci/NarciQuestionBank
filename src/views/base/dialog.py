"""
对话框组件
"""
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from views.base.styles import get_style
from views.base.button import BaseButton


class BaseDialog(QDialog):
    """
    对话框基类
    """
    
    def __init__(self, title="对话框", width=400, height=300, parent=None):
        """
        初始化对话框
        
        Args:
            title: 对话框标题
            width: 对话框宽度
            height: 对话框高度
            parent: 父组件
        """
        super().__init__(parent)
        
        # 设置对话框属性
        self.setWindowTitle(title)
        self.resize(width, height)
        self.setMinimumSize(300, 200)
        
        # 设置窗口模态
        self.setModal(True)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化布局
        self._init_layout()
        
        # 初始化按钮
        self._init_buttons()
    
    def _apply_styles(self):
        """
        应用样式
        """
        # 设置对话框样式
        self.setStyleSheet(get_style("window"))
        
        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)
    
    def _init_layout(self):
        """
        初始化布局
        """
        # 创建主垂直布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # 创建内容区域
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(10)
        
        # 创建按钮区域
        self.button_widget = QWidget()
        self.button_layout = QHBoxLayout(self.button_widget)
        self.button_layout.setSpacing(10)
        self.button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 添加到主布局
        self.main_layout.addWidget(self.content_widget, 1)
        self.main_layout.addWidget(self.button_widget)
    
    def _init_buttons(self):
        """
        初始化按钮
        """
        # 创建确定按钮
        self.ok_button = BaseButton("确定")
        self.ok_button.setMinimumWidth(80)
        self.ok_button.clicked.connect(self.accept)
        
        # 创建取消按钮
        self.cancel_button = BaseButton("取消")
        self.cancel_button.setMinimumWidth(80)
        self.cancel_button.clicked.connect(self.reject)
        
        # 添加到按钮布局
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
    
    def add_content(self, widget):
        """
        添加内容组件
        
        Args:
            widget: 要添加的组件
        """
        self.content_layout.addWidget(widget)
    
    def add_label(self, text):
        """
        添加标签
        
        Args:
            text: 标签文本
        """
        label = QLabel(text)
        label.setWordWrap(True)
        self.content_layout.addWidget(label)
    
    def set_title(self, title):
        """
        设置对话框标题
        
        Args:
            title: 新的对话框标题
        """
        self.setWindowTitle(title)
    
    def set_ok_text(self, text):
        """
        设置确定按钮文本
        
        Args:
            text: 新的确定按钮文本
        """
        self.ok_button.set_text(text)
    
    def set_cancel_text(self, text):
        """
        设置取消按钮文本
        
        Args:
            text: 新的取消按钮文本
        """
        self.cancel_button.set_text(text)
    
    def center(self):
        """
        对话框居中显示
        """
        # 获取父窗口几何信息
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
        else:
            # 如果没有父窗口，居中显示在屏幕上
            screen = self.screen().geometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
        
        # 设置对话框位置
        self.move(x, y)
    
    def exec(self):
        """
        执行对话框
        
        Returns:
            对话框执行结果
        """
        # 居中显示
        self.center()
        
        # 执行对话框
        result = super().exec()
        return result
