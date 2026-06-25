"""
主程序入口
"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

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

        # 创建中央内容区域
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {COLORS['app_background']};")
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 创建左侧面板
        self.left_panel = LeftPanel()
        self.left_panel.setFixedWidth(window_settings.left_width)
        content_layout.addWidget(self.left_panel)

        # 创建中央面板
        self.center_panel = CenterPanel()
        content_layout.addWidget(self.center_panel, 1)  # 占据剩余空间

        # 创建右侧面板
        self.right_panel = RightPanel()
        self.right_panel.setFixedWidth(window_settings.right_width)
        content_layout.addWidget(self.right_panel)

        main_layout.addWidget(content_widget, 1)  # 占据剩余空间

        # 设置主窗口中央部件
        self.setCentralWidget(main_widget)

    def closeEvent(self, event):
        """
        关闭事件处理，保存窗口设置
        """
        # 获取当前窗口尺寸
        width = self.width()
        height = self.height()

        # 计算中央面板宽度（总宽度减去左右面板）
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
