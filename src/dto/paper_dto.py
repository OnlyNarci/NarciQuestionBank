"""
结构化的论文数据
"""
from typing import Optional, List, Any
from enum import StrEnum, Enum
from pydantic import Field
from dto.base import BaseDTO


class LineSpacingRule(StrEnum):
    """
    行距规则
    """
    MULTIPLE = 'multiple'       # 多倍行距
    EXACTLY = 'exactly'         # 固定值
    AT_LEAST = 'at_least'       # 最小值
    SINGLE = 'single'           # 单倍行距
    DOUBLE = 'double'           # 双倍行距


class ParagraphSpacingRule(StrEnum):
    """
    段落间距规则
    """
    PT = 'pt'
    LINES = 'lines'


class AlignmentRule(StrEnum):
    """
    对齐规则
    """
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'
    JUSTIFY = 'justify'     # 两端对齐


class FontSize(float, Enum):
    """
    中文字号和pt的对应关系
    """
    ZERO_SIZE = 42      # 初号
    SMALL_ZERO = 36     # 小初
    ONE_SIZE = 26       # 一号
    SMALL_ONE = 24      # 小一
    TWO_SIZE = 22       # 二号
    SMALL_TWO = 18      # 小二
    THREE_SIZE = 16     # 三号
    SMALL_THREE = 15    # 小三
    FOUR_SIZE = 14      # 四号
    SMALL_FOUR = 12     # 小四
    FIVE_SIZE = 10.5    # 五号
    SMALL_FIVE = 9      # 小五
    SIX_SIZE = 7.5      # 六号
    SMALL_SIX = 6.5     # 小六
    SEVEN_SIZE = 5.5    # 七号
    SMALL_SEVEN = 5     # 小七


class ReferenceType(StrEnum):
    """
    参考文献文献类型标识（遵循 GB/T 7714-2015 信息与文献参考文献著录规则）
    """
    # 核心常用文献类型
    JOURNAL_ARTICLE = "J"           # 期刊文章
    MONOGRAPH = "M"                 # 专著（图书）
    DISSERTATION = "D"              # 学位论文
    CONFERENCE_PROCEEDINGS = "C"    # 会议论文集
    NEWSPAPER_ARTICLE = "N"         # 报纸文章
    STANDARD = "S"                  # 行业/国家标准
    PATENT = "P"                    # 专利文献
    REPORT = "R"                    # 科技报告

    # 电子资源基础类型
    DATABASE = "DB"                 # 数据库
    COMPUTER_PROGRAM = "CP"         # 计算机程序
    ELECTRONIC_BULLETIN = "EB"      # 电子公告

    # 电子资源复合类型（日常最常用）
    EB_ONLINE = "EB/OL"             # 在线电子公告（网页、在线专栏、博客等）
    DB_ONLINE = "DB/OL"             # 在线数据库
    CP_DISK = "CP/DK"               # 光盘版计算机程序

    OTHER = "Z"                     # 其他未说明的文献类型
    

class Font(BaseDTO):
    """
    字体属性
    """
    en_family: str = Field(default="Times New Roman", description="字体")
    zh_family: str = Field(default="宋体", description="中文字体")
    size_pt: float = Field(default=12, ge=0, description="字号, 单位pt, 不存中文字号, 在写入标准化数据之前应根据FontSize换算")
    bold: bool = Field(default=False, description="是否加粗")
    italic: bool = Field(default=False, description="是否斜体")
    underline: bool = Field(default=False, description="是否下划线")
    color: str = Field(default="#000000", description="字体颜色，16进制RGB")
    background_color: Optional[str] = Field(default=None, description="字体背景色，16进制RGB")


class LineSpacing(BaseDTO):
    """
    行间距
    """
    line_spacing_rule: LineSpacingRule = Field(default=LineSpacingRule.EXACTLY, description="行距规则, 选multiple时只认line_spacing_multi, 选exactly/at_least时只认line_spacing_pt, 选single/double时都不用")
    line_spacing_multi: float = Field(default=1, ge=0, description='多倍行距的倍数')
    line_spacing_pt: float = Field(default=20, ge=0, description="行间距, 单位pt")


class ParagraphSpacing(BaseDTO):
    """
    段落间距
    """
    paragraph_spacing_rule: ParagraphSpacingRule = Field(default=ParagraphSpacingRule.LINES, description="段落间距规则, pt只认结尾元素, lines只认lines结尾元素")
    space_before_pt: float = Field(default=0, ge=0, description="段前固定值, 单位pt")
    space_before_lines: float = Field(default=0, ge=0, description="段前行")
    space_after_pt: float = Field(default=0, ge=0, description="段后固定值, 单位pt")
    space_after_lines: float = Field(default=0, ge=0, description="段后行")
    

class Paragraph(BaseDTO):
    line_spacing: LineSpacing = Field(default_factory=LineSpacing, description="行间距")
    paragraph_spacing: ParagraphSpacing = Field(default_factory=ParagraphSpacing, description="段间距")
    alignment: AlignmentRule = Field(default=AlignmentRule.LEFT, description='对齐模式')
    first_line_indent_ch: float = Field(default=2.0, description="首行缩进字符数（中文默认2字符）")

    
class Text(BaseDTO):
    level: int = Field(default=1, ge=1, le=9, description="大纲等级")
    font: Font = Field(default_factory=Font, description="字体样式")
    paragraph: Paragraph = Field(default_factory=Paragraph, description="段落样式")
    content: List[str] = Field(default_factory=list, description="文本内容, 按照标点、制表符、换行等划分")


class Image(BaseDTO):
    """
    图片
    """
    alt: str = Field(default="", description="图片说明")
    path: str = Field(default="", description="图片路径/URL")
    caption: Text = Field(default_factory=Text, description="图题")
    

class Table(BaseDTO):
    """
    表格
    """
    headers: List[List[str]] = Field(default_factory=list, description="表头（二维列表）")
    rows: List[List[str]] = Field(default_factory=list, description="表内容（二维列表）")
    caption: Text = Field(default_factory=Text, description="表题")


class ReferenceItem(BaseDTO):
    """
    结构化参考文献条目
    """
    ref_type: ReferenceType = Field(
        default=ReferenceType.JOURNAL_ARTICLE,
        description="文献类型，遵循GB/T 7714标准标识"
    )
    index: int = Field(description="文献序号，如 [1] 中的 1")
    authors: List[str] = Field(default_factory=list, description="作者列表")
    title: str = Field(description="文献标题")

    # 不同文献类型对应的源出版物字段
    journal: Optional[str] = Field(default=None, description="期刊名称（J 类专用）")
    book_title: Optional[str] = Field(default=None, description="专著/会议集名称（M/C 类专用）")
    school: Optional[str] = Field(default=None, description="学位授予单位（D 类专用）")
    conference_name: Optional[str] = Field(default=None, description="会议全称（C 类专用）")

    # 通用出版信息
    year: int = Field(description="出版/发表年份")
    volume: Optional[str] = Field(default=None, description="卷号")
    issue: Optional[str] = Field(default=None, description="期号")
    pages: Optional[str] = Field(default=None, description="页码范围")
    doi: Optional[str] = Field(default=None, description="DOI 编号")

    # 电子文献专用
    url: Optional[str] = Field(default=None, description="在线资源链接")
    access_date: Optional[str] = Field(default=None, description="引用访问日期（电子文献必填）")
    

class Section(BaseDTO):
    """
    正文章节（含标题+子内容）
    """
    title: Text = Field(default_factory=Text, description="章节标题")
    content: List[Text | "Section" | Image | Table] = Field(default_factory=list, description="章节内容：文本/子章节（体现层级）")
    
    
class Document(BaseDTO):
    title: Text = Field(default_factory=Text, description="主标题")
    abstract: Text = Field(default_factory=Text, description="摘要")
    body: Optional[List[Section]] = Field(default=None, description="正文, 运行时构建, 需体现标题层级关系")
    references: Text = Field(default_factory=Text, description="参考文献, content每个元素为一条")
    