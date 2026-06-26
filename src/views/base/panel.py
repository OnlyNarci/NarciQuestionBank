"""
面板基类，用于创建可嵌入的子组件面板
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QFont

from views.base.styles import COLORS


class BasePanel(QWidget):
    """
    面板基类，继承自QWidget，用于创建可嵌入的子组件
    """

    def __init__(self, parent=None):
        """
        初始化面板

        :param parent: 父组件
        """
        super().__init__(parent)

        # 应用样式
        self._apply_styles()

        # 初始化主布局
        self._init_main_layout()

    def _apply_styles(self):
        """
        应用样式
        """
        # 设置面板背景为透明，让父容器的背景色透过来
        self.setStyleSheet("background-color: transparent;")

        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)

    def _init_main_layout(self):
        """
        初始化主布局
        """
        # 创建主垂直布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(0)

    def add_widget(self, widget, stretch=0):
        """
        添加组件到主布局

        :param widget: 要添加的组件
        :param stretch: 拉伸因子
        """
        self.main_layout.addWidget(widget, stretch)

    def insert_widget(self, index, widget, stretch=0):
        """
        在指定位置插入组件

        :param index: 插入位置
        :param widget: 要插入的组件
        :param stretch: 拉伸因子
        """
        self.main_layout.insertWidget(index, widget, stretch)

    def remove_widget(self, widget):
        """
        从主布局中移除组件

        :param widget: 要移除的组件
        """
        self.main_layout.removeWidget(widget)
        widget.deleteLater()

    def clear_layout(self):
        """
        清空主布局
        """
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
