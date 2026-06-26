"""
中央面板，展示论文全文，格式错误的文本红色高亮，可能错误的文本黄色高亮
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout

from views.base.panel import BasePanel
from views.base.styles import COLORS


class CenterPanel(BasePanel):
    """
    中央面板
    """

    def __init__(self, parent=None):
        """
        初始化中央面板

        :param parent: 父组件
        """
        super().__init__(parent)
        
        # 创建白色圆角盒子
        self._create_white_box()
    
    def _create_white_box(self):
        """
        创建白色圆角盒子，所有控件放在盒子内
        """
        # 创建白色盒子widget
        self.white_box = QWidget()
        self.white_box.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['background']};
                border-radius: 8px;
            }}
        """)
        
        # 创建盒子布局，距离边缘4像素
        self.box_layout = QVBoxLayout(self.white_box)
        self.box_layout.setContentsMargins(4, 4, 4, 4)
        self.box_layout.setSpacing(0)
        
        # 将白色盒子添加到主布局
        self.add_widget(self.white_box, 1)
        