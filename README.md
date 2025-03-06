# FileCreator

---

## 📌 项目结构生成器 (Flexible Project Structure Generator)

这是一个用 **Python** 编写的灵活的项目结构生成器，可以根据不同格式的输入来创建项目目录结构。

---

## ✨ 功能特点

✅ **支持多种输入格式**：
  - 📂 目录树文本格式
  - 📄 JSON 格式
  - 📜 YAML 格式
✅ **自动创建目录和文件**
✅ **详细的转换过程日志**
✅ **错误处理和提示**

---

## 🔧 安装依赖

本程序依赖 **`PyYAML`** 库。程序会自动检测并安装依赖，或者你可以手动安装：

```bash
pip install pyyaml
```

---

## 🚀 使用示例

### 📂 目录树格式输入

```plaintext
project/
├── src/
│   ├── main.py
│   └── utils.py
└── docs/
    └── README.md
```

### 📄 JSON 格式输入

```json
{
  "project": {
    "src": {
      "main.py": "",
      "utils.py": ""
    },
    "docs": {
      "README.md": ""
    }
  }
}
```

### 📜 YAML 格式输入

```yaml
project:
  src:
    main.py: ""
    utils.py: ""
  docs:
    README.md: ""
```

---

## 🏃 运行程序

```bash
python flexible-project-structure-generator.py
```

---

## 🎯 示例输入

```plaintext
project/
├── src/    # 源代码目录
│   ├── main.py  # 主程序
│   └── utils.py  # 工具函数
└── docs/    # 文档目录
    └── README.md  # 说明文档
```

输入 **'done'** 结束。

---

## 📍 指定保存路径

```plaintext
D:\my_project
```

程序将在指定路径创建相应的目录结构。

---

## 📖 目录内容

📌 本 README 包含了：

1️⃣ **项目简介和主要功能**
2️⃣ **安装说明**
3️⃣ **详细的使用方法和示例**
4️⃣ **支持的输入格式**
5️⃣ **注意事项和错误处理**
6️⃣ **贡献指南和许可证信息**

📢 你可以根据需要调整或补充这个 README 的内容。

---

