"""
滑块组件
"""
from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


from views.base.styles import COLORS


class BaseSlider(QSlider):
    """
    滑块基类
    """
    
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        """
        初始化滑块
        
        Args:
            orientation: 滑块方向
            parent: 父组件
        """
        super().__init__(orientation, parent)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化属性
        self._init_properties()
    
    def _apply_styles(self):
        """
        应用样式
        """
        # 定义滑块样式
        if self.orientation() == Qt.Orientation.Horizontal:
            handle_size = "16px"
            groove_height = "6px"
        else:
            handle_size = "16px"
            groove_height = "6px"
        
        style = f"""
        QSlider {{
            min-height: 36px;
        }}
        QSlider::groove:horizontal {{
            border: none;
            height: {groove_height};
            background: {COLORS['border']};
            border-radius: 3px;
        }}
        QSlider::groove:vertical {{
            border: none;
            width: {groove_height};
            background: {COLORS['border']};
            border-radius: 3px;
        }}
        QSlider::sub-page:horizontal {{
            background: {COLORS['primary_dark']};
            border-radius: 3px;
        }}
        QSlider::sub-page:vertical {{
            background: {COLORS['primary_dark']};
            border-radius: 3px;
        }}
        QSlider::add-page:horizontal {{
            background: {COLORS['border']};
            border-radius: 3px;
        }}
        QSlider::add-page:vertical {{
            background: {COLORS['border']};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: {COLORS['background']};
            border: 2px solid {COLORS['primary_dark']};
            width: {handle_size};
            height: {handle_size};
            border-radius: 8px;
            margin: -5px 0;
            cursor: pointer;
        }}
        QSlider::handle:vertical {{
            background: {COLORS['background']};
            border: 2px solid {COLORS['primary_dark']};
            width: {handle_size};
            height: {handle_size};
            border-radius: 8px;
            margin: 0 -5px;
            cursor: pointer;
        }}
        QSlider::handle:horizontal:hover {{
            background: {COLORS['primary']};
            border-color: {COLORS['primary_dark']};
        }}
        QSlider::handle:vertical:hover {{
            background: {COLORS['primary']};
            border-color: {COLORS['primary_dark']};
        }}
        QSlider::handle:horizontal:pressed {{
            background: {COLORS['primary_dark']};
            border-color: {COLORS['primary_dark']};
        }}
        QSlider::handle:vertical:pressed {{
            background: {COLORS['primary_dark']};
            border-color: {COLORS['primary_dark']};
        }}
        """
        
        self.setStyleSheet(style)
    
    def _init_properties(self):
        """
        初始化属性
        """
        # 设置鼠标指针
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # 设置焦点策略
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # 设置默认范围
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(50)
        
        # 设置步长
        self.setSingleStep(1)
        self.setPageStep(10)
    
    def set_range(self, minimum, maximum):
        """
        设置滑块范围
        
        Args:
            minimum: 最小值
            maximum: 最大值
        """
        self.setMinimum(minimum)
        self.setMaximum(maximum)
    
    def set_value(self, value):
        """
        设置滑块值
        
        Args:
            value: 滑块值
        """
        self.setValue(value)
    
    def get_value(self):
        """
        获取滑块值
        
        Returns:
            滑块当前值
        """
        return self.value()
    
    def set_step(self, step):
        """
        设置步长
        
        Args:
            step: 步长值
        """
        self.setSingleStep(step)
