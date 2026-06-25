"""
样式定义文件
"""

# 颜色主题定义
COLORS = {
    # 主色调
    "primary": "#E3F2FD",  # 浅蓝色
    "primary_dark": "#2196F3",  # 深蓝色
    "primary_light": "#BBDEFB",  # 更浅的蓝色
    
    # 背景色
    "background": "#FFFFFF",  # 白色
    "background_secondary": "#F5F5F5",  # 浅灰色背景
    "app_background": "#F0F0F0",  # 整个应用的浅灰色背景
    
    # 文本色
    "text": "#333333",  # 深灰色
    "text_secondary": "#666666",  # 中灰色
    "text_light": "#999999",  # 浅灰色
    
    # 边框色
    "border": "#E0E0E0",  # 浅灰色边框
    "border_focus": "#2196F3",  # 聚焦时的边框色
    
    # 状态色
    "success": "#4CAF50",  # 绿色
    "warning": "#FFC107",  # 黄色
    "error": "#F44336",  # 红色
    "info": "#2196F3",  # 蓝色
}

# 字体定义
FONTS = {
    "default": "Arial, sans-serif",
    "heading": "Arial, sans-serif",
    "button": "Arial, sans-serif",
}

# 字体大小定义
FONT_SIZES = {
    "small": "10px",
    "medium": "12px",
    "default": "14px",
    "large": "16px",
    "xlarge": "18px",
    "heading": "20px",
}

# 间距定义
SPACING = {
    "xs": "4px",
    "small": "8px",
    "medium": "12px",
    "default": "16px",
    "large": "20px",
    "xlarge": "24px",
}

# 圆角定义
BORDER_RADIUS = {
    "small": "4px",
    "medium": "8px",
    "default": "12px",
    "large": "16px",
}

# 阴影定义
SHADOWS = {
    "small": "0 2px 4px rgba(0, 0, 0, 0.1)",
    "default": "0 4px 8px rgba(0, 0, 0, 0.1)",
    "large": "0 8px 16px rgba(0, 0, 0, 0.1)",
}

# 通用样式表
COMMON_STYLES = {
    "window": f"background-color: {COLORS['background']};",
              
    "button": f"""font-family: {FONTS['button']};
              font-size: {FONT_SIZES['default']};
              border-radius: {BORDER_RADIUS['medium']};
              padding: {SPACING['small']} {SPACING['medium']};
              border: 1px solid {COLORS['border']};
              background-color: {COLORS['primary']};
              color: {COLORS['text']};
              cursor: pointer;
              transition: all 0.3s ease;""",
              
    "button:hover": f"""background-color: {COLORS['primary_light']};
                    border-color: {COLORS['primary_dark']};
                    box-shadow: {SHADOWS['small']};""",
                    
    "button:pressed": f"""background-color: {COLORS['primary_dark']};
                     color: {COLORS['background']};
                     transform: translateY(1px);""",
                     
    "text_button": f"""font-family: {FONTS['button']};
                   font-size: {FONT_SIZES['default']};
                   border: none;
                   background-color: transparent;
                   color: {COLORS['primary_dark']};
                   cursor: pointer;
                   padding: {SPACING['small']};
                   text-decoration: underline;
                   transition: color 0.3s ease;""",
                   
    "text_button:hover": f"color: {COLORS['primary_light']};",
}


# 获取样式的辅助函数
def get_style(style_name):
    """
    获取指定样式
    
    Args:
        style_name: 样式名称
        
    Returns:
        样式字符串
    """
    return COMMON_STYLES.get(style_name, "")


# 获取颜色的辅助函数
def get_color(color_name):
    """
    获取指定颜色
    
    Args:
        color_name: 颜色名称
        
    Returns:
        颜色值
    """
    return COLORS.get(color_name, COLORS["text"])
