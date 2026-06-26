"""
主程序入口
"""
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSplitter

from db.session import DbSession
from utils.log_manager import get_logger
from core.settings import get_settings, update_window_settings
from dto.setting_dto import WindowSettings

# 导入视图组件
from views.left_panel import LeftPanel
from views.right_panel import RightPanel
from views.center_panel import CenterPanel
from views.base.styles import COLORS


# 获取logger
logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

        # 从配置加载窗口设置
        settings = get_settings()
        window_settings = settings.interface.window

        # 设置窗口属性
        self.setWindowTitle("论文格式校验")
        self.setMinimumSize(800, 600)
        total_width = window_settings.left_width + window_settings.center_width + window_settings.right_width
        self.resize(total_width, window_settings.height)

        # 设置应用背景色为浅灰色
        self.setStyleSheet(f"background-color: {COLORS['app_background']};")

        # 创建主容器
        main_widget = QWidget()
        main_widget.setStyleSheet(f"background-color: {COLORS['app_background']};")
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 使用QSplitter创建可调整的三联布局
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border']};
                width: 4px;
            }}
            QSplitter::handle:hover {{
                background-color: {COLORS['primary']};
            }}
        """)

        # 创建左侧面板
        self.left_panel = LeftPanel()
        self.left_panel.setMinimumWidth(200)
        self.left_panel.setMaximumWidth(600)
        self.splitter.addWidget(self.left_panel)

        # 创建中央面板
        self.center_panel = CenterPanel()
        self.splitter.addWidget(self.center_panel)

        # 创建右侧面板
        self.right_panel = RightPanel()
        self.right_panel.setMinimumWidth(200)
        self.right_panel.setMaximumWidth(600)
        self.splitter.addWidget(self.right_panel)

        # 设置初始面板宽度比例
        self.splitter.setSizes([
            window_settings.left_width,
            window_settings.center_width,
            window_settings.right_width
        ])

        main_layout.addWidget(self.splitter, 1)

        # 设置主窗口中央部件
        self.setCentralWidget(main_widget)

    def closeEvent(self, event):
        """
        关闭事件处理，保存窗口设置
        """
        # 获取当前窗口尺寸
        width = self.width()
        height = self.height()

        # 从splitter获取面板宽度
        sizes = self.splitter.sizes()
        if len(sizes) == 3:
            left_width = sizes[0]
            center_width = sizes[1]
            right_width = sizes[2]
        else:
            left_width = self.left_panel.width()
            right_width = self.right_panel.width()
            center_width = width - left_width - right_width

        # 创建窗口设置对象
        window_settings = WindowSettings(
            height=height,
            center_width=center_width,
            left_width=left_width,
            right_width=right_width
        )

        # 保存窗口设置
        update_window_settings(window_settings)
        logger.info(f"窗口设置已保存: height={height}, left_width={left_width}, center_width={center_width}, right_width={right_width}")

        event.accept()


def main():
    """
    主函数
    """
    logger.info("开始启动论文格式校验软件")

    # 初始化数据库
    logger.info("正在初始化数据库...")
    DbSession().init_db()

    # 创建应用程序
    logger.info("正在创建应用程序...")
    app = QApplication(sys.argv)

    # 设置应用程序样式
    app.setStyle("Fusion")

    # 创建主窗口
    logger.info("正在创建主窗口...")
    window = MainWindow()
    window.show()
    logger.info("主窗口创建完成，应用程序启动")

    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
