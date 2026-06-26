"""
左侧面板，导航窗格，提供llm连接配置和论文格式校验规则配置
"""
from typing import List, Optional, Callable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QStyledItemDelegate, QStyleOptionViewItem, QDialog, QStyle, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QRect, QModelIndex, QAbstractItemModel
from PySide6.QtGui import QIcon, QPainter, QPixmap, QColor, QPainterPath, QPen, QBrush, QMouseEvent

from views.base.panel import BasePanel
from views.base.styles import COLORS
from views.component.llm_config_dialog import LLMConfigDialog
from views.component.silent_message_box import silent_information, silent_warning, silent_question
from services.agent import LlmService
from dto.setting_dto import LlmSettings
from core.settings import update_current_llm_settings
from utils.log_manager import get_logger


logger = get_logger(__name__)


class LlmComboDelegate(QStyledItemDelegate):
    """
    自定义下拉列表项代理，显示编辑和删除图标按钮
    """
    
    def __init__(
        self, 
        parent: Optional[QWidget] = None, 
        edit_callback: Optional[Callable[[int], None]] = None, 
        delete_callback: Optional[Callable[[int], None]] = None
    ):
        """
        初始化代理
        
        :param parent: 父组件
        :param edit_callback: 编辑回调函数，接收 llm_id: int 参数
        :param delete_callback: 删除回调函数，接收 llm_id: int 参数
        """
        super().__init__(parent)
        self.edit_callback: Optional[Callable[[int], None]] = edit_callback
        self.delete_callback: Optional[Callable[[int], None]] = delete_callback
        self._edit_icon: Optional[QIcon] = None
        self._delete_icon: Optional[QIcon] = None
    
    def _create_icons(self) -> None:
        """
        创建编辑和删除图标
        """
        # 创建编辑图标（黑色铅笔）
        edit_pixmap = QPixmap(20, 20)
        edit_pixmap.fill(Qt.GlobalColor.transparent)
        edit_painter = QPainter(edit_pixmap)
        edit_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制黑色铅笔图标
        edit_painter.setPen(QPen(QColor("#000000"), 1.5))
        # 画笔身
        edit_painter.drawLine(5, 15, 12, 8)
        # 画笔尖
        edit_painter.drawLine(12, 8, 16, 4)
        # 画橡皮擦部分
        edit_painter.drawLine(5, 15, 8, 12)
        edit_painter.drawLine(5, 15, 8, 15)
        edit_painter.end()
        self._edit_icon = QIcon(edit_pixmap)
        
        # 创建删除图标（黑色垃圾桶）
        delete_pixmap = QPixmap(20, 20)
        delete_pixmap.fill(Qt.GlobalColor.transparent)
        delete_painter = QPainter(delete_pixmap)
        delete_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制黑色垃圾桶图标
        delete_painter.setPen(QPen(QColor("#000000"), 1.5))
        # 画桶身
        delete_painter.drawRect(5, 7, 10, 10)
        # 画盖子
        delete_painter.drawLine(4, 7, 16, 7)
        delete_painter.drawLine(6, 5, 14, 5)
        delete_painter.drawLine(6, 5, 6, 7)
        delete_painter.drawLine(14, 5, 14, 7)
        # 画竖线（桶的纹理）
        delete_painter.drawLine(8, 9, 8, 15)
        delete_painter.drawLine(12, 9, 12, 15)
        delete_painter.end()
        self._delete_icon = QIcon(delete_pixmap)
    
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex
    ) -> None:
        """
        绘制下拉列表项，包含编辑和删除按钮
        
        :param painter: 绘图工具
        :param option: 样式选项
        :param index: 模型索引
        """
        # 初始化图标
        if self._edit_icon is None:
            self._create_icons()
        
        # 获取数据
        text = index.data(Qt.ItemDataRole.DisplayRole)
        llm_id = index.data(Qt.ItemDataRole.UserRole)
        
        # 如果是无效项，直接绘制文本
        if llm_id is None:
            super().paint(painter, option, index)
            return
        
        # 按钮尺寸和间距
        button_size = 22
        button_spacing = 4
        right_margin = 8
        
        # 按钮起始位置
        buttons_start_x = option.rect.right() - button_size * 2 - button_spacing - right_margin
        
        # 编辑按钮区域
        edit_button_rect = QRect(
            buttons_start_x,
            option.rect.top(),
            button_size,
            option.rect.height()
        )
        
        # 删除按钮区域
        delete_button_rect = QRect(
            buttons_start_x + button_size + button_spacing,
            option.rect.top(),
            button_size,
            option.rect.height()
        )
        
        # 绘制背景（白底）
        if option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, QColor("#E3F2FD"))  # 选中时浅蓝色背景
        else:
            painter.fillRect(option.rect, QColor("#FFFFFF"))   # 白底
        
        # 绘制文本区域（黑字）
        text_rect = QRect(
            option.rect.left() + 8,
            option.rect.top(),
            buttons_start_x - 8 - button_spacing,
            option.rect.height()
        )
        painter.setPen(QColor("#000000"))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
        
        # 鼠标悬停效果
        if option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(edit_button_rect, QColor("#E0E0E0"))
            painter.fillRect(delete_button_rect, QColor("#FFCDD2"))
        
        # 绘制编辑图标
        self._edit_icon.paint(painter, edit_button_rect, Qt.AlignmentFlag.AlignCenter)
        
        # 绘制删除图标
        self._delete_icon.paint(painter, delete_button_rect, Qt.AlignmentFlag.AlignCenter)
    
    def editorEvent(
        self,
        event,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex
    ) -> bool:
        """
        处理编辑事件（按钮点击）
        
        :param event: 事件对象
        :param model: 数据模型
        :param option: 样式选项
        :param index: 模型索引
        :return: 是否处理了事件
        """
        if not index.isValid():
            return False
        
        llm_id = index.data(Qt.ItemDataRole.UserRole)
        if llm_id is None:
            return False
        
        # 获取按钮区域
        button_size = 22
        button_spacing = 4
        right_margin = 8
        
        rect_right = option.rect.right()
        
        # 编辑按钮区域
        edit_rect = QRect(
            rect_right - button_size * 2 - button_spacing - right_margin,
            option.rect.top(),
            button_size,
            option.rect.height()
        )
        
        # 删除按钮区域
        delete_rect = QRect(
            rect_right - button_size - right_margin,
            option.rect.top(),
            button_size,
            option.rect.height()
        )
        
        # 判断点击位置
        if event.type() == event.Type.MouseButtonPress:
            if isinstance(event, QMouseEvent):
                pos = event.position().toPoint()
                if edit_rect.contains(pos) and self.edit_callback:
                    self.edit_callback(llm_id)
                    return True
                elif delete_rect.contains(pos) and self.delete_callback:
                    self.delete_callback(llm_id)
                    return True
        
        return False
    
    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex
    ) -> QSize:
        """
        返回项的尺寸
        
        :param option: 样式选项
        :param index: 模型索引
        :return: 项的尺寸
        """
        return QSize(option.rect.width(), 36)


class LlmCombo(QComboBox):
    """
    自定义LLM下拉列表，包含编辑和删除图标按钮
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        初始化下拉列表
        
        :param parent: 父组件
        """
        super().__init__(parent)
        
        # 设置可编辑
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setStyleSheet(f"""
            QLineEdit {{
                font-family: Arial, sans-serif;
                font-size: 12px;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px;
                background-color: #FFFFFF;
                color: #000000;
                min-height: 32px;
            }}
            QLineEdit:focus {{
                border-color: {COLORS['primary_dark']};
            }}
        """)
        
        # 设置下拉框样式（隐藏默认箭头）
        self.setStyleSheet(f"""
            QComboBox {{
                border: none;
                padding: 0;
                min-height: 32px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 32px;
                border: none;
                background-color: {COLORS['primary_light']};
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 0;
                background-color: #FFFFFF;
                selection-background-color: {COLORS['primary']};
            }}
            QComboBox QAbstractItemView::item {{
                color: #000000;
                padding: 6px;
                min-height: 30px;
            }}
            QComboBox QAbstractItemView::item:selected {{
                color: #000000;
                background-color: #E3F2FD;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: #F5F5F5;
            }}
        """)
        
        # 设置代理（不传回调，由外部通过 set_callbacks 设置）
        self._delegate = LlmComboDelegate(self)
        self.setItemDelegate(self._delegate)
        
        # 存储所有配置
        self._llm_settings_list = []
        self._edit_callback = None
        self._delete_callback = None
    
    def set_callbacks(
        self, 
        edit_callback: Callable[[int], None], 
        delete_callback: Callable[[int], None]
    ) -> None:
        """
        设置编辑和删除回调函数
        
        :param edit_callback: 编辑回调函数，接收 llm_id: int 参数
        :param delete_callback: 删除回调函数，接收 llm_id: int 参数
        """
        self._edit_callback = edit_callback
        self._delete_callback = delete_callback
        self._delegate.edit_callback = edit_callback
        self._delegate.delete_callback = delete_callback
    
    def paintEvent(self, event) -> None:
        """
        重写paintEvent绘制白色下拉箭头
        """
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 下拉按钮区域
        drop_width = 32
        drop_x = self.rect().right() - drop_width
        drop_y = self.rect().top()
        drop_height = self.rect().height()
        
        # 计算箭头位置（居中）
        arrow_x = drop_x + drop_width // 2
        arrow_y = drop_y + drop_height // 2
        
        # 绘制白色倒三角箭头（使用QPainterPath）
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        
        # 箭头参数
        arrow_width = 8
        arrow_height = 6
        
        path = QPainterPath()
        path.moveTo(arrow_x - arrow_width, arrow_y - arrow_height // 2)
        path.lineTo(arrow_x + arrow_width, arrow_y - arrow_height // 2)
        path.lineTo(arrow_x, arrow_y + arrow_height // 2)
        path.closeSubpath()
        
        painter.drawPath(path)
    
    def set_llm_settings(self, llm_settings_list: List[LlmSettings]) -> None:
        """
        设置LLM配置列表
        
        :param llm_settings_list: LLM配置列表
        """
        self._llm_settings_list = llm_settings_list
        self.clear()
        
        # 添加所有配置
        for llm_settings in llm_settings_list:
            self.addItem(llm_settings.model_name, llm_settings.id)
    
    def get_settings_by_id(self, llm_id: int) -> Optional[LlmSettings]:
        """
        根据ID获取配置
        
        :param llm_id: 配置ID
        :return: 对应的配置对象，如果不存在返回None
        """
        for settings in self._llm_settings_list:
            if settings.id == llm_id:
                return settings
        return None


class LeftPanel(BasePanel):
    """
    左侧面板，提供LLM连接配置管理功能
    """

    def __init__(self, parent=None) -> None:
        """
        初始化左侧面板

        :param parent: 父组件
        """
        super().__init__(parent)
        
        # 当前选中的LLM配置ID
        self.current_llm_id: Optional[int] = None
        
        # 创建白色圆角盒子
        self._create_white_box()
        
        # 初始化UI
        self._init_llm_ui()
        
        # 加载LLM配置
        self._load_llm_settings()
    
    def _create_white_box(self) -> None:
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
        
        # 将白色盒子添加到主布局（主布局已有4px边距）
        self.add_widget(self.white_box, 1)
    
    def _init_llm_ui(self) -> None:
        """
        初始化LLM配置UI
        """
        # 创建LLM配置区域容器
        llm_widget = QWidget()
        llm_layout = QVBoxLayout(llm_widget)
        llm_layout.setContentsMargins(10, 10, 10, 10)
        llm_layout.setSpacing(10)
        
        # 标题标签
        title_label = QLabel("大模型连接：")
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text']};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        llm_layout.addWidget(title_label)
        
        # 下拉框和添加按钮的布局
        combo_layout = QHBoxLayout()
        combo_layout.setSpacing(5)
        combo_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        # LLM配置下拉框
        self.llm_combo = LlmCombo()
        self.llm_combo.set_callbacks(
            edit_callback=lambda llm_id: self._on_edit_llm_by_id(llm_id),
            delete_callback=lambda llm_id: self._on_delete_llm(llm_id)
        )
        combo_layout.addWidget(self.llm_combo, 1)
        
        # 添加按钮
        self.add_button = QPushButton("+")
        self.add_button.setMinimumSize(32, 32)
        self.add_button.setMaximumWidth(48)
        self.add_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.add_button.setStyleSheet(f"""
            QPushButton {{
                font-size: 18px;
                font-weight: bold;
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['primary']};
                color: {COLORS['text']};
                padding: 0;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_light']};
                border-color: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['primary_dark']};
                color: #FFFFFF;
            }}
        """)
        self.add_button.clicked.connect(self._on_add_llm)
        combo_layout.addWidget(self.add_button)
        
        # 下拉框选择事件
        self.llm_combo.currentIndexChanged.connect(self._on_llm_selected)
        
        llm_layout.addLayout(combo_layout)
        
        # LLM配置列表区域
        self.llm_list_widget = QWidget()
        self.llm_list_layout = QVBoxLayout(self.llm_list_widget)
        self.llm_list_layout.setContentsMargins(0, 0, 0, 0)
        self.llm_list_layout.setSpacing(3)
        self.llm_list_widget.setVisible(False)  # 默认隐藏
        llm_layout.addWidget(self.llm_list_widget)
        
        # 添加到白色盒子布局
        self.box_layout.addWidget(llm_widget)
        
        # 添加弹性空间
        self.box_layout.addWidget(QWidget(), 1)
    
    @staticmethod
    def _create_edit_icon() -> QIcon:
        """
        创建编辑图标
        
        :return: 编辑图标
        """
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QColor(COLORS['primary_dark']))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # 绘制铅笔图标
        painter.drawRect(4, 4, 6, 12)
        painter.drawLine(10, 4, 16, 10)
        painter.drawLine(10, 16, 16, 10)
        
        painter.end()
        return QIcon(pixmap)
    
    @staticmethod
    def _create_delete_icon() -> QIcon:
        """
        创建删除图标
        
        :return: 删除图标
        """
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QColor(COLORS['error']))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # 绘制回收站图标
        painter.drawRect(4, 6, 12, 10)
        painter.drawLine(4, 8, 16, 8)
        painter.drawLine(4, 6, 8, 6)
        painter.drawLine(12, 6, 16, 6)
        painter.drawLine(8, 4, 8, 6)
        painter.drawLine(12, 4, 12, 6)
        
        painter.end()
        return QIcon(pixmap)
    
    def _load_llm_settings(self) -> None:
        """
        加载LLM配置列表
        """
        try:
            llm_settings_list = LlmService.get_llm_settings()
            self._update_llm_list(llm_settings_list)
            self.llm_combo.set_llm_settings(llm_settings_list)
        except Exception as e:
            logger.error(f"加载LLM配置失败: {e}")
            silent_warning(self, "错误", f"加载LLM配置失败：{str(e)}")
    
    def _update_llm_list(self, llm_settings_list: List[LlmSettings]) -> None:
        """
        更新LLM配置列表
        
        :param llm_settings_list: LLM配置列表
        """
        # 清空现有列表
        while self.llm_list_layout.count() > 0:
            item = self.llm_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加配置项
        for llm_settings in llm_settings_list:
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 3, 5, 3)
            item_layout.setSpacing(5)
            
            # 配置名称标签
            name_label = QLabel(llm_settings.model_name)
            name_label.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text']};
                    font-size: 12px;
                }}
            """)
            item_layout.addWidget(name_label, 1)
            
            # 编辑按钮
            edit_button = QPushButton()
            edit_button.setIcon(self._create_edit_icon())
            edit_button.setFixedSize(24, 24)
            edit_button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    border-radius: 4px;
                    background-color: transparent;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['primary']};
                }}
            """)
            edit_button.clicked.connect(lambda checked, s=llm_settings: self._on_edit_llm(s))
            item_layout.addWidget(edit_button)
            
            # 删除按钮
            delete_button = QPushButton()
            delete_button.setIcon(self._create_delete_icon())
            delete_button.setFixedSize(24, 24)
            delete_button.setStyleSheet(f"""
                QPushButton {{
                    border: none;
                    border-radius: 4px;
                    background-color: transparent;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['error']};
                }}
            """)
            delete_button.clicked.connect(lambda checked, llm_id=llm_settings.id: self._on_delete_llm(llm_id))
            item_layout.addWidget(delete_button)
            
            # 添加到列表
            self.llm_list_layout.addWidget(item_widget)
    
    def _on_llm_selected(self, index: int) -> None:
        """
        下拉框选择事件
        
        :param index: 选中的索引
        """
        if index >= 0:
            llm_id = self.llm_combo.itemData(index)
            if llm_id is not None:
                llm_settings = self.llm_combo.get_settings_by_id(llm_id)
                if llm_settings:
                    update_current_llm_settings(llm_settings)
                    logger.info(f"已选择LLM配置: {llm_settings.model_name}, id={llm_id}")
    
    def _on_edit_llm_by_id(self, llm_id: int) -> None:
        """
        根据ID编辑LLM配置

        :param llm_id: 要编辑的配置ID
        """
        llm_settings = self.llm_combo.get_settings_by_id(llm_id)
        if llm_settings:
            logger.info(f"触发LLM配置编辑: {llm_settings.model_name}, id={llm_id}")
            self._on_edit_llm(llm_settings)
    
    def _on_add_llm(self) -> None:
        """
        添加LLM配置
        """
        dialog = LLMConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            llm_settings = dialog.get_llm_settings()
            try:
                model_id = LlmService.create_llm_setting(llm_settings)
                llm_settings.id = model_id
                logger.info(f"成功创建LLM配置: {llm_settings.model_name}, id={model_id}")
                
                self._load_llm_settings()
                
                silent_information(self, "成功", "LLM配置创建成功！")
            except Exception as e:
                logger.error(f"创建LLM配置失败: {e}")
                silent_warning(self, "错误", f"创建LLM配置失败：{str(e)}")
    
    def _on_edit_llm(self, llm_settings: LlmSettings) -> None:
        """
        编辑LLM配置
        
        :param llm_settings: 要编辑的配置
        """
        dialog = LLMConfigDialog(self, llm_settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_settings = dialog.get_llm_settings()
            try:
                model_id = LlmService.update_Llm_setting(updated_settings)
                updated_settings.id = model_id
                logger.info(f"成功更新LLM配置: {updated_settings.model_name}, id={model_id}")
                
                self._load_llm_settings()
                
                silent_information(self, "成功", "LLM配置更新成功！")
            except Exception as e:
                logger.error(f"更新LLM配置失败: {e}")
                silent_warning(self, "错误", f"更新LLM配置失败：{str(e)}")
    
    def _on_delete_llm(self, llm_id: int) -> None:
        """
        删除LLM配置
        
        :param llm_id: 要删除的配置ID
        """
        reply = silent_question(
            self,
            "确认删除",
            "确定要删除此LLM配置吗？"
        )
        
        if reply == QDialog.DialogCode.Accepted:
            try:
                LlmService.delete_Llm_setting(llm_id)
                logger.info(f"成功删除LLM配置: {llm_id}")
                
                self._load_llm_settings()
                
                silent_information(self, "成功", "LLM配置删除成功！")
            except Exception as e:
                logger.error(f"删除LLM配置失败: {e}")
                silent_warning(self, "错误", f"删除LLM配置失败：{str(e)}")
                