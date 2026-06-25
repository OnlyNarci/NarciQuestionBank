"""
中央面板，展示论文全文，格式错误的文本红色高亮，可能错误的文本黄色高亮
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout

from views.base.window import BaseWindow
from views.base.styles import COLORS


class CenterPanel(BaseWindow):
    """
    中央面板
    """
    
    def __init__(self):
        """
        初始化中央面板
        """
        super().__init__(title="论文内容", width=800, height=800, min_width=400, min_height=600)
        
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
        