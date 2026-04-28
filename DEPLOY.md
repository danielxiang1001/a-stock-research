# 部署说明

## 方案D：GitHub Pages + AKShare 数据自动更新

### 架构
```
AKShare → Python脚本 → GitHub Actions定时更新 → GitHub Pages → 团队访问
```

### 部署步骤

#### 1. 创建 GitHub 仓库

1. 打开 https://github.com/new
2. 仓库名称：`a-stock-research`（或你喜欢）
3. 选择 **Private**（私有）或 **Public**（公开）
4. 点击 Create repository

#### 2. 上传代码

```bash
cd /Users/xiangwenlong/WorkBuddy/20260428131851/a-stock-research
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/a-stock-research.git
git push -u origin main
```

#### 3. 启用 GitHub Pages

1. 进入仓库 → Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: **main** , folder: **/ (root)**
4. 点击 Save

#### 4. 启用 GitHub Actions

工作流文件 `.github/workflows/update-data.yml` 已配置好：
- 每周一到周五（北京时间 9:00, 15:30, 21:00）自动更新数据
- 支持手动触发（在 Actions 页面点击 "Run workflow"）

#### 5. 等待第一次数据更新

- Actions 会自动运行脚本获取数据
- 数据会提交到 `market_data.json`
- 几分钟后网页就能看到实时数据

---

### 团队成员使用

直接访问：`https://你的用户名.github.io/a-stock-research/`

无需安装任何软件，只要能上网就能用。

---

### 本地测试

如果想在本地测试：

```bash
# 安装 AKShare
pip install akshare

# 运行脚本获取数据
python fetch_data_akshare.py

# 用浏览器打开 index.html
open index.html
```

---

### 自定义修改

#### 修改数据更新频率
编辑 `.github/workflows/update-data.yml` 中的 cron 表达式：
```yaml
schedule:
  - cron: '0 1,7,13 * * 1-5'  # UTC时间
```
换算为北京时间：+8小时

#### 修改数据源
编辑 `fetch_data_akshare.py`

#### 修改网页样式
编辑 `index.html`

---

### 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 网页主文件 |
| `market_data.json` | 数据文件（自动生成） |
| `fetch_data_akshare.py` | 数据获取脚本 |
| `.github/workflows/update-data.yml` | GitHub Actions 配置 |
