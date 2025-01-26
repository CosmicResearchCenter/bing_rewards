以下是 **Bing Rewards 自动化工具** 的详细使用说明，包括功能描述、参数说明、示例命令以及注意事项。

---

## **工具简介**
该工具基于 Python 和 Playwright 实现，用于自动化完成 Bing Rewards 的以下任务：
1. **保存登录状态**：通过手动登录 Bing 账户，保存登录状态到本地文件。
2. **执行搜索任务**：自动执行 Bing 搜索，完成每日搜索积分任务。
3. **领取积分**：自动领取 Bing Rewards 的每日积分奖励。

支持无头模式（后台运行）和界面模式（显示浏览器），适合日常自动化任务。

---

## **环境准备**
在运行工具之前，请确保满足以下条件：

### 1. 安装 Python
- 确保已安装 Python 3.7 或更高版本。
- 下载地址：[Python 官网](https://www.python.org/downloads/)

### 2. 安装依赖
在项目目录下运行以下命令安装依赖：
```bash
pip install playwright playwright-stealth
```

### 3. 初始化 Playwright
安装 Playwright 的浏览器内核：
```bash
playwright install
```

---

## **工具使用**

### **1. 命令行参数**
以下是工具支持的命令行参数：

| 参数名               | 描述                                                                 | 默认值           |
|----------------------|----------------------------------------------------------------------|------------------|
| `--login`            | 保存登录状态（手动登录 Bing 账户并保存 cookies）。                   | 无               |
| `--search`           | 执行搜索任务（自动完成 Bing 搜索）。                                 | 无               |
| `--collect`          | 领取积分任务（自动领取 Bing Rewards 积分）。                         | 无               |
| `--auth_file`        | 认证信息文件路径（保存登录状态的 JSON 文件）。                       | `auth.json`      |
| `--search_data_file` | 搜索数据文件路径（包含搜索关键词和句子的 JSON 文件）。               | `search_data.json` |
| `--delay`            | 操作之间的延时（秒），用于控制任务执行速度。                         | `5`              |
| `--headless`         | 是否启用无头模式（后台运行，不显示浏览器界面）。                     | 无（默认显示界面） |

---

### **2. 使用步骤**

#### **步骤 1：保存登录状态**
在首次使用工具时，需要手动登录 Bing 账户并保存登录状态。

运行以下命令：
```bash
python run.py --login --auth_file auth.json
```

- 工具会启动浏览器并打开 Bing 登录页面。
- 手动完成登录后，按回车键保存登录状态到 `auth.json` 文件。

#### **步骤 2：执行搜索任务**
完成登录后，可以运行搜索任务以获取 Bing Rewards 积分。

运行以下命令：
```bash
python run.py --search --auth_file auth.json --search_data_file search_data.json --headless
```

- 工具会自动执行 40 次 Bing 搜索（默认值）。
- 搜索内容从 `search_data.json` 文件中随机选取。

#### **步骤 3：领取积分**
运行以下命令自动领取 Bing Rewards 积分：
```bash
python run.py --collect --auth_file auth.json --headless
```

- 工具会自动打开 Bing Rewards 页面并领取每日积分。

#### **步骤 4：同时执行搜索和领取任务**
可以同时执行搜索和领取任务：
```bash
python run.py --search --collect --auth_file auth.json --search_data_file search_data.json --headless
```

---

### **3. 配置文件说明**

#### **`auth.json`**
- 用于保存登录状态（cookies）。
- 通过 `--login` 参数生成。
- 文件内容示例：
  ```json
  {
    "cookies": [
      {
        "name": "cookie_name",
        "value": "cookie_value",
        "domain": ".bing.com",
        "path": "/",
        "expires": 1234567890,
        "httpOnly": true,
        "secure": true
      }
    ]
  }
  ```

#### **`search_data.json`**
- 包含搜索关键词和句子的 JSON 文件。
- 文件内容示例：
  ```json
  {
    "search_terms": ["Python", "Playwright", "Bing Rewards"],
    "search_sentences": [
      "What is Python programming?",
      "How to use Playwright for automation?",
      "Bing Rewards daily tasks"
    ]
  }
  ```

---

### **4. 示例命令**

#### **保存登录状态**
```bash
python run.py --login --auth_file auth.json
```

#### **执行搜索任务（无头模式）**
```bash
python run.py --search --auth_file auth.json --search_data_file search_data.json --headless
```

#### **领取积分（无头模式）**
```bash
python run.py --collect --auth_file auth.json --headless
```

#### **同时执行搜索和领取任务（无头模式）**
```bash
python run.py --search --collect --auth_file auth.json --search_data_file search_data.json --headless
```

#### **显示浏览器界面（禁用无头模式）**
```bash
python run.py --search --auth_file auth.json --search_data_file search_data.json
```

---

## **注意事项**
1. **登录状态有效期**：
   - 登录状态（cookies）可能会过期，建议定期重新保存登录状态。

2. **搜索数据文件**：
   - 确保 `search_data.json` 文件中包含足够的关键词和句子，以避免重复搜索。

3. **无头模式**：
   - 在服务器或无界面环境中运行时，请启用无头模式（`--headless`）。
   - 在本地调试时，可以禁用无头模式以查看浏览器界面。

4. **延时设置**：
   - 默认延时为 5 秒，可以根据需要调整 `--delay` 参数的值。

5. **错误处理**：
   - 如果任务失败，工具会记录错误日志并继续执行后续任务。

---

## **常见问题**

### **1. 登录失败**
- 确保网络连接正常。
- 检查是否使用了正确的 Bing 账户。

### **2. 搜索任务未获取积分**
- 确保搜索内容不重复。
- 检查 Bing Rewards 的每日积分上限是否已满。

### **3. 无头模式下无法运行**
- 确保已安装 Playwright 的浏览器内核：
  ```bash
  playwright install
  ```

---

通过以上说明，您可以轻松使用该工具自动化完成 Bing Rewards 的日常任务。如果有其他问题，欢迎随时反馈！