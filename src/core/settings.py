"""
用于管理软件配置
"""
import yaml
from typing import Dict, Optional, Any
from pathlib import Path

from dto.setting_dto import (
    AppSetting,
    InterfaceSettings,
    WindowSettings,
    PathsSettings,
    LlmSettings
)


_settings: Optional[AppSetting] = None


def get_root_dir() -> Path:
    """获取项目根目录"""
    # 方法1: 从当前文件路径向上查找
    current_path = Path(__file__).resolve()
    for parent in [current_path, *current_path.parents]:
        # 检查是否存在config.yml文件
        if (parent / 'config.yml').exists():
            return parent
    
    # 方法2: 检查当前工作目录
    cwd = Path.cwd()
    if (cwd / 'config.yml').exists():
        return cwd
    
    # 方法3: 默认使用原始计算方法作为后备
    return Path(__file__).parent.parent.parent


def load_config_from_yaml(yaml_path: Optional[str] = None) -> Dict[str, Any]:
    """
    获取配置信息
    :return: 配置信息
    """
    if yaml_path is None:
        yaml_path = get_root_dir() / 'config.yml'
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config or {}


def get_settings() -> AppSetting:
    """
    获取配置信息对象
    :return: 配置信息对象
    """
    global _settings
    if _settings is None:
        root = get_root_dir()
        config = load_config_from_yaml()
        
        # 构建界面配置
        interface_config = config.get('interface', {})
        interface_settings = InterfaceSettings(
            theme=interface_config.get('theme', 'light'),
            window=WindowSettings(**interface_config.get('window', {})),
        )
        
        # 构建路径配置
        paths_config = config.get('paths', {})
        paths_settings = PathsSettings(
            data_dir=root / paths_config.get('data_dir', 'data'),
            db_path=root / paths_config.get('db_dir', 'data/db/paper_format.db'),
            temp_dir=root / paths_config.get('temp_dir', 'temp'),
            log_dir=root / paths_config.get('log_dir', 'logs'),
            prompt_dir=root / paths_config.get('prompt_dir', 'static/prompt')
        )
        
        # 创建并缓存AppSetting对象
        _settings = AppSetting(
            interface=interface_settings,
            paths=paths_settings,
        )
        
    return _settings


def clear_settings() -> None:
    """
    清空配置信息对象
    """
    global _settings
    _settings = None


def save_config_to_yaml(config: Dict[str, Any], yaml_path: Optional[str] = None) -> None:
    """
    将配置信息写入YAML文件
    :param config: 配置信息字典
    :param yaml_path: YAML文件路径，None则使用默认路径
    """
    if yaml_path is None:
        yaml_path = get_root_dir() / 'config.yml'
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)


def _settings_to_dict(settings: AppSetting) -> Dict[str, Any]:
    """
    将AppSetting对象转换为字典
    :param settings: AppSetting对象
    :return: 配置信息字典
    """
    root = get_root_dir()
    
    def relative_path(path: Path) -> str:
        """将绝对路径转换为相对路径"""
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)
    
    return {
        'interface': {
            'theme': settings.interface.theme,
            'window': {
                'height': settings.interface.window.height,
                'center_width': settings.interface.window.center_width,
                'left_width': settings.interface.window.left_width,
                'right_width': settings.interface.window.right_width,
            },
        },
        'paths': {
            'data_dir': relative_path(settings.paths.data_dir),
            'db_path': relative_path(settings.paths.db_path),
            'temp_dir': relative_path(settings.paths.temp_dir),
            'log_dir': relative_path(settings.paths.log_dir),
            'prompt_dir': relative_path(settings.paths.prompt_dir)
        }
    }


def update_llm_settings(llm_setting: LlmSettings) -> None:
    """
    更新当前启用的大模型配置
    :param llm_setting: 大模型配置
    """
    global _settings
    _settings.llm = llm_setting


def update_interface_theme(theme: str) -> None:
    """
    更新界面主题
    :param theme: 主题 (light, dark)
    """
    global _settings
    settings = get_settings()
    settings.interface.theme = theme
    _settings = settings
    
    # 保存到YAML文件
    config_dict = _settings_to_dict(settings)
    save_config_to_yaml(config_dict)


def update_window_settings(window_setting: WindowSettings) -> None:
    """
    更新窗口设置
    :param window_setting: 窗口设置
    """
    global _settings
    settings = get_settings()
    settings.interface.window = window_setting
    _settings = settings
    
    # 保存到YAML文件
    config_dict = _settings_to_dict(settings)
    save_config_to_yaml(config_dict)


def update_current_llm_settings(llm_setting: LlmSettings) -> None:
    """
    更新当前启用的大模型配置
    """
    global _settings
    _settings.llm = llm_setting
    