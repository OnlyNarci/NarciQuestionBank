"""
窗口基类
"""
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from PySide6.QtGui import QFont

from views.base.styles import COLORS


class BaseWindow(QMainWindow):
    """
    窗口基类
    """
    
    def __init__(self, title="应用程序", width=1200, height=800, min_width=800, min_height=600):
        """
        初始化窗口
        
        Args:
            title: 窗口标题
            width: 窗口宽度
            height: 窗口高度
            min_width: 窗口最小宽度
            min_height: 窗口最小高度
        """
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle(title)
        self.resize(width, height)
        self.setMinimumSize(min_width, min_height)
        
        # 应用样式
        self._apply_styles()
        
        # 初始化主布局
        self._init_main_layout()
        
        # 初始化窗口状态
        self._init_window_state()
        
        # 初始化键盘快捷键
        self._init_shortcuts()
    
    def _apply_styles(self):
        """
        应用样式
        """
        # 设置窗口背景色为浅灰色
        self.setStyleSheet(f"background-color: {COLORS['app_background']};")
        
        # 设置字体
        font = QFont("Arial", 12)
        self.setFont(font)
    
    def _init_main_layout(self):
        """
        初始化主布局
        """
        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 设置中央部件背景为透明，让窗口背景色透过来
        self.central_widget.setStyleSheet("background-color: transparent;")
        
        # 创建主垂直布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(0)
    
    def _init_window_state(self):
        """
        初始化窗口状态
        """
        # 窗口状态标志
        self.is_maximized = False
        self.is_fullscreen = False
    
    def _init_shortcuts(self):
        """
        初始化键盘快捷键
        """
        # 这里可以添加全局快捷键
        # 例如：Ctrl+Q 退出，Ctrl+M 最小化等
        pass
    
    def center(self):
        """
        窗口居中显示
        """
        # 获取屏幕几何信息
        screen = QApplication.primaryScreen().geometry()
        
        # 计算窗口居中位置
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        
        # 设置窗口位置
        self.move(x, y)
    
    def set_title(self, title):
        """
        设置窗口标题
        
        Args:
            title: 新的窗口标题
        """
        self.setWindowTitle(title)
    
    def set_size(self, width, height):
        """
        设置窗口大小
        
        Args:
            width: 窗口宽度
            height: 窗口高度
        """
        self.resize(width, height)
    
    def maximize(self):
        """
        最大化窗口
        """
        self.showMaximized()
        self.is_maximized = True
    
    def minimize(self):
        """
        最小化窗口
        """
        self.showMinimized()
    
    def restore(self):
        """
        还原窗口
        """
        self.showNormal()
        self.is_maximized = False
    
    def toggle_fullscreen(self):
        """
        切换全屏模式
        """
        if self.is_fullscreen:
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True
    
    def add_widget(self, widget, stretch=0):
        """
        添加组件到主布局
        
        Args:
            widget: 要添加的组件
            stretch: 拉伸因子
        """
        self.main_layout.addWidget(widget, stretch)
    
    def insert_widget(self, index, widget, stretch=0):
        """
        在指定位置插入组件
        
        Args:
            index: 插入位置
            widget: 要插入的组件
            stretch: 拉伸因子
        """
        self.main_layout.insertWidget(index, widget, stretch)
    
    def remove_widget(self, widget):
        """
        从主布局中移除组件
        
        Args:
            widget: 要移除的组件
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
    
    def closeEvent(self, event):
        """
        关闭事件处理
        
        Args:
            event: 关闭事件
        """
        # 这里可以添加关闭前的清理操作
        event.accept()
