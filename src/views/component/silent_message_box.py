"""
无声消息框组件，用于显示没有系统声音的消息提示
"""
from typing import Optional
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt

from views.base.styles import COLORS


class SilentMessageBox(QDialog):
    """
    没有声音的消息框
    """

    Information = 1
    Warning = 2
    Error = 3
    Question = 4

    Yes = QDialog.DialogCode.Accepted
    No = QDialog.DialogCode.Rejected

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        title: str = "提示",
        text: str = "",
        icon_type: int = Information
    ) -> None:
        """
        初始化无声消息框

        :param parent: 父窗口
        :param title: 标题
        :param text: 消息文本
        :param icon_type: 图标类型，可选值：Information、Warning、Error、Question
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(300)

        # 设置窗口标志，禁用系统声音
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowStaysOnTopHint
        )

        # 根据类型设置样式
        if icon_type == self.Warning:
            border_color = "#FFC107"
        elif icon_type == self.Error:
            border_color = "#F44336"
        elif icon_type == self.Question:
            border_color = "#2196F3"
        else:
            border_color = "#2196F3"

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['background']};
                border: 2px solid {border_color};
                border-radius: 8px;
            }}
            QLabel {{
                color: {COLORS['text']};
                font-size: 14px;
                padding: 10px;
            }}
            QPushButton {{
                min-width: 80px;
                padding: 8px 16px;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['primary']};
                color: {COLORS['text']};
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_light']};
            }}
        """)

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(15)
        self._layout.setContentsMargins(20, 20, 20, 20)

        # 消息文本
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(label)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        self._layout.addLayout(button_layout)


class SilentQuestionBox(SilentMessageBox):
    """
    没有声音的确认对话框
    """

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        title: str = "确认",
        text: str = ""
    ) -> None:
        """
        初始化无声确认对话框

        :param parent: 父窗口
        :param title: 标题
        :param text: 消息文本
        """
        super().__init__(parent, title, text, self.Question)

        # 替换按钮为是/否
        # 清除现有按钮布局（最后一个item是按钮布局）
        while self._layout.count() > 1:
            item = self._layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # 删除布局中的所有控件
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        # 添加是/否按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        yes_button = QPushButton("是")
        yes_button.clicked.connect(self.accept)
        button_layout.addWidget(yes_button)

        no_button = QPushButton("否")
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        self._layout.addLayout(button_layout)


def silent_information(
    parent: Optional[QWidget],
    title: str,
    text: str
) -> int:
    """
    显示无声的信息消息框

    :param parent: 父窗口
    :param title: 标题
    :param text: 消息文本
    :return: QDialog.Accepted
    """
    msg_box = SilentMessageBox(parent, title, text, SilentMessageBox.Information)
    return msg_box.exec()


def silent_warning(
    parent: Optional[QWidget],
    title: str,
    text: str
) -> int:
    """
    显示无声的警告消息框

    :param parent: 父窗口
    :param title: 标题
    :param text: 消息文本
    :return: QDialog.Accepted
    """
    msg_box = SilentMessageBox(parent, title, text, SilentMessageBox.Warning)
    return msg_box.exec()


def silent_error(
    parent: Optional[QWidget],
    title: str,
    text: str
) -> int:
    """
    显示无声的错误消息框

    :param parent: 父窗口
    :param title: 标题
    :param text: 消息文本
    :return: QDialog.Accepted
    """
    msg_box = SilentMessageBox(parent, title, text, SilentMessageBox.Error)
    return msg_box.exec()


def silent_question(
    parent: Optional[QWidget],
    title: str,
    text: str
) -> int:
    """
    显示无声的确认消息框

    :param parent: 父窗口
    :param title: 标题
    :param text: 消息文本
    :return: QDialog.Accepted 表示"是"，QDialog.Rejected 表示"否"
    """
    msg_box = SilentQuestionBox(parent, title, text)
    return msg_box.exec()
