以下是 **详细的使用说明**，涵盖了脚本的功能、参数说明、使用步骤以及注意事项。您可以根据需要参考这些内容来运行脚本。

---

## 脚本功能

该脚本用于自动化 Bing Rewards 的相关操作，包括：

1. **保存登录状态**：
   - 打开浏览器，提示用户手动登录 Bing 账号，并将登录状态保存到文件中。

2. **执行搜索任务**：
   - 自动执行 Bing 搜索任务，以获取积分。

3. **领取积分**：
   - 自动领取 Bing Rewards 积分。

---

## 脚本文件

1. **`bing_rewards.py`**：
   - 包含 `BingReWards` 类和 `save_login_state` 函数，用于实现核心功能。

2. **`run.py`**：
   - 主脚本，通过命令行参数调用 `bing_rewards.py` 中的功能。

---

## 环境准备

### 1. 安装依赖
确保已安装以下 Python 库：
- `playwright`
- `playwright-stealth`

安装命令：
```bash
pip install playwright playwright-stealth
```

### 2. 安装浏览器
运行以下命令安装 Playwright 所需的浏览器：
```bash
playwright install
```

### 3. 准备搜索数据文件
创建一个名为 `search_data.json` 的文件，用于做搜索的内容：
```json
{
  "search_terms": ["Python", "Playwright", "Bing Rewards", "自动化脚本"],
  "search_sentences": [
    "如何使用 Playwright 进行自动化测试",
    "Bing Rewards 积分获取技巧",
    "Python 自动化脚本编写指南"
  ]
}
```

---

## 使用步骤

### 1. 保存登录状态
首次运行脚本时，需要保存登录状态。

#### 命令：
```bash
python run.py --login --auth_file auth.json
```

#### 说明：
- `--login`：表示执行保存登录状态的操作。
- `--auth_file auth.json`：指定保存登录状态的文件名为 `auth.json`（默认值为 `auth.json`）。

#### 操作流程：
1. 脚本会打开浏览器并导航到 Bing 登录页面。
2. 用户手动登录 Bing 账号。
3. 登录完成后，按回车键继续。
4. 登录状态将保存到 `auth.json` 文件中。

---

### 2. 执行搜索任务
使用保存的登录状态执行 Bing 搜索任务。

#### 命令：
```bash
python run.py --search --auth_file auth.json --search_data_file search_data.json --delay 5
```

#### 说明：
- `--search`：表示执行搜索任务。
- `--auth_file auth.json`：指定使用的登录状态文件（默认为 `auth.json`）。
- `--search_data_file search_data.json`：指定搜索数据文件（默认为 `search_data.json`）。
- `--delay 5`：设置每次操作之间的延时（秒），默认为 5 秒。

#### 操作流程：
1. 脚本会打开浏览器并加载登录状态。
2. 自动执行 40 次 Bing 搜索任务。
3. 每次搜索后，脚本会随机滚动页面并等待一段时间。
4. 任务完成后，浏览器会自动关闭。

---

### 3. 领取积分
使用保存的登录状态领取 Bing Rewards 积分。

#### 命令：
```bash
python run.py --collect --auth_file auth.json --delay 5
```

#### 说明：
- `--collect`：表示执行领取积分操作。
- `--auth_file auth.json`：指定使用的登录状态文件（默认为 `auth.json`）。
- `--delay 5`：设置每次操作之间的延时（秒），默认为 5 秒。

#### 操作流程：
1. 脚本会打开浏览器并加载登录状态。
2. 自动导航到 Bing Rewards 页面并领取积分。
3. 任务完成后，浏览器会自动关闭。

---

### 4. 同时执行搜索和领取积分
可以同时执行搜索任务和领取积分操作。

#### 命令：
```bash
python run.py --search --collect --auth_file auth.json --search_data_file search_data.json --delay 5
```

#### 说明：
- `--search` 和 `--collect`：同时执行搜索任务和领取积分操作。
- 其他参数与单独执行时相同。

---

## 参数说明

| 参数               | 说明                                                                 |
|--------------------|----------------------------------------------------------------------|
| `--login`          | 保存登录状态到文件。                                                |
| `--search`         | 执行 Bing 搜索任务。                                                |
| `--collect`        | 收集 Bing Rewards 积分。                                            |
| `--auth_file`      | 认证信息文件路径，默认为 `auth.json`。                              |
| `--search_data_file` | 搜索数据文件路径，默认为 `search_data.json`。                       |
| `--delay`          | 操作之间的延时（秒），默认为 5 秒。                                 |

---

## 注意事项

1. **首次运行**：
   - 必须先使用 `--login` 参数保存登录状态。

2. **搜索数据文件**：
   - 确保 `search_data.json` 文件包含 `search_terms` 和 `search_sentences` 字段。

3. **延时设置**：
   - 根据实际情况调整 `--delay` 参数，避免操作过于频繁导致检测。

4. **多账号支持**：
   - 可以通过指定不同的 `--auth_file` 文件名来管理多个账号的登录状态。

5. **浏览器窗口**：
   - 脚本运行时，浏览器窗口会显示操作过程。如果需要后台运行，可以将 `headless=False` 改为 `headless=True`。

---

## 示例命令

### 1. 保存登录状态
```bash
python run.py --login --auth_file auth.json
```

### 2. 执行搜索任务
```bash
python run.py --search --auth_file auth.json --search_data_file search_data.json --delay 5
```

### 3. 领取积分
```bash
python run.py --collect --auth_file auth.json --delay 5
```

### 4. 同时执行搜索和领取积分
```bash
python run.py --search --collect --auth_file auth.json --search_data_file search_data.json --delay 5
```

---

通过以上说明，您可以轻松使用脚本来实现 Bing Rewards 的自动化操作。如果还有其他问题，请随时告诉我！