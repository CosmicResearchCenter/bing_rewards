# Bing Rewards 自动化工具

基于 Python 和 Playwright 的 Bing Rewards 自动化工具，帮助用户自动完成必应搜索和积分任务。

## 功能特点

- 支持多账号管理
- 自动执行必应搜索
- 自动领取每日奖励积分
- 支持无头模式运行
- 自动获取热搜词进行搜索
- 智能任务调度与重试机制

## 环境要求

- Python 3.7+
- Playwright
- 系统要求：Windows/Linux/MacOS

## 安装步骤

1. 克隆代码仓库：
```bash
git clone https://github.com/CosmicResearchCenter/bing_rewards.git
cd bing_rewards
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 安装 Playwright：
```bash
playwright install
```

## 使用说明

### 1. 准备工作

1. 在项目根目录下创建 `accounts` 文件夹
2. 使用登录工具保存账号认证信息：
```bash
python src/utils/login.py
```

### 2. 运行程序

启动自动化任务：
```bash
python main.py
```

## 目录结构

```
bing_rewards/
├── main.py            # 主程序入口
├── accounts/          # 账号认证文件目录
├── src/
│   ├── core/         # 核心功能模块
│   │   └── bing_rewards.py
│   └── utils/        # 工具模块
│       ├── login.py  # 登录工具
│       └── tophot.py # 热搜获取工具
└── requirements.txt   # 项目依赖
```

## 配置说明

账号文件 (保存在 accounts 目录下)：
- 文件格式：JSON
- 包含浏览器 cookies 和认证信息
- 每个账号对应一个独立的 JSON 文件

## 注意事项

1. 请合理设置搜索间隔，避免触发必应的安全机制
2. 建议使用代理或VPN，避免IP被限制
3. 定期检查账号登录状态，必要时重新登录
4. 建议配置日志监控，及时发现和处理异常

## 常见问题

Q: 为什么会出现登录失效？
> A: cookies 存在有效期，建议每周重新登录一次

Q: 搜索次数过多会有风险吗？
> A: 程序已内置随机延时和智能调度，风险较低

Q: 支持手机必应吗？
> A: 目前仅支持 PC 端必应搜索

## 更新日志

### v1.0.0 (2024-02-23)
- 支持多账号管理
- 实现自动搜索功能
- 添加自动领取积分功能
- 集成热搜词获取
