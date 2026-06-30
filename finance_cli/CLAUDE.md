# 家庭记账工具 (Finance Tracker)

基于 Python + Streamlit + SQLite3 的 Web 记账应用。

## 技术栈

- **Python** 3.13+
- **Streamlit** 1.51 — Web UI 框架
- **SQLite3** — 内置数据库，无需额外安装
- **pandas** — 数据处理和展示

## 项目结构

```
finance_cli/
├── CLAUDE.md           # 本文件
├── app.py              # 入口：页面配置、侧边栏导航、路由分发
├── db.py               # 数据库层：建表、CRUD、统计查询
├── views/
│   ├── __init__.py     # 包标识
│   ├── add.py          # 录入账单页面
│   ├── view.py         # 查看账单页面（筛选 + 表格）
│   ├── delete.py       # 删除账单页面
│   └── statistics.py   # 分类统计页面（柱状图 + 报表）
├── finance.db          # SQLite 数据库文件（首次运行自动创建）
└── .gitignore
```

> 注意：页面模块放在 `views/` 而非 `pages/`，避免 Streamlit 自动生成默认导航栏。

## 运行方式

```bash
cd finance_cli
streamlit run app.py
```

浏览器访问 http://localhost:8501

## 数据库

**表名**: `entries`

| 列 | 类型 | 说明 |
|---|---|---|
| id | INTEGER PK | 自增主键 |
| amount | REAL | 金额（元） |
| category | TEXT | 分类（餐饮/交通/购物/娱乐/居住/其他） |
| date | TEXT | 日期（YYYY-MM-DD） |
| note | TEXT | 备注 |
| created_at | TEXT | 创建时间 |

## 模块职责

- **db.py** — 所有数据库操作，每个函数接收 `conn` 参数
- **views/*.py** — 每个文件暴露 `render(conn)` 函数，负责 UI 渲染
- **app.py** — 创建数据库连接，侧边栏 `st.sidebar.radio` 导航，调用对应页面

## 依赖安装

```bash
pip install streamlit pandas
```
