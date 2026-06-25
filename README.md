# 论文格式校验工具

## 项目介绍

一款简单的论文格式校验工具，校验字体、段落、样式、错别字等

## 技术栈

- **前端**：PySide6
- **数据库**：SQLite
- **ORM**：SQLAlchemy
- **大模型框架**：LangChain
- **数据处理**：Pandas
- **PDF处理**：PyPDF2/pdfplumber
- **Word处理**：python-docx
- **打包工具**：PyInstaller

## 项目结构

```
├── src/
│   ├── db/                  # 数据库相关
│   ├── service/             # 业务逻辑层
│   ├── utils/               # 工具类
│   ├── view_models/         # 视图模型层
│   ├── views/               # 视图层
│   └── main.py              # 主程序入口
├── test/                    # 单元测试
├── config.yml               # 配置文件
├── pyproject.toml           # 依赖管理
└── README.md                # 项目说明
```

## 安装说明

### 1. 环境要求
- Python 3.10+
- 操作系统：Windows/macOS/Linux

### 2. 依赖安装

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -e .
```

### 3. 运行程序

```bash
# 运行主程序
python src/main.py
```

### 4. 打包部署

```bash
# 使用PyInstaller打包
pyinstaller --name PaperFormater --onefile src/main.py
```


## 注意事项

1. **大模型使用**：使用大模型功能需要配置相应的API密钥
2. **文件格式**：导入的PDF和Word文件应保持清晰的格式
3. **数据库备份**：定期备份数据库文件以防止数据丢失
4. **性能优化**：处理论文可能需要较长时间，请耐心等待

## 联系方式

如有问题或建议，欢迎联系我们：

- 邮箱：binfen0403@163.com
-  GitHub：https://github.com/OnlyNarci/PaperFormater
---

**版本**：1.0.0
**更新日期**：2026-06-16