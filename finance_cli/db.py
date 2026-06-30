"""
====================================================
    数据库模块 — 所有数据库操作集中在这里
    包括：建表、增删查、统计、辅助查询
====================================================
"""

import sqlite3
import pandas as pd

# ==================================================
# 常量定义
# ==================================================

# 数据库文件名
DB_FILE = "finance.db"

# 预设的 6 个消费分类
CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "居住", "其他"]


# ==================================================
# 数据库初始化
# ==================================================

def init_db():
    """
    初始化数据库连接并创建表（如果表不存在）。
    首次运行时自动创建 finance.db 文件和 entries 表。
    返回: sqlite3.Connection 对象（已设置 row_factory）
    """
    conn = sqlite3.connect(DB_FILE)
    # 设置 row_factory，让查询结果支持按列名访问
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 创建账单表（IF NOT EXISTS 确保不会重复创建）
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            amount     REAL    NOT NULL,
            category   TEXT    NOT NULL,
            date       TEXT    NOT NULL,
            note       TEXT    DEFAULT '',
            created_at TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)

    # 创建索引，加速按日期和分类的查询
    c.execute("CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_entries_category ON entries(category)")

    conn.commit()
    return conn


# ==================================================
# 增 — 添加账单
# ==================================================

def add_entry(conn, amount, category, date_str, note):
    """
    向数据库插入一条新账单记录。
    参数:
        conn:     数据库连接
        amount:   金额（float）
        category: 分类名称（str）
        date_str: 日期字符串，格式 "YYYY-MM-DD"
        note:     备注（str）
    返回: 新插入记录的 id（int）
    """
    c = conn.cursor()
    c.execute(
        "INSERT INTO entries (amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date_str, note)
    )
    conn.commit()
    return c.lastrowid


# ==================================================
# 查 — 查询账单列表
# ==================================================

def get_entries(conn, month=None, category=None):
    """
    查询账单记录，支持按月份和分类筛选。
    参数:
        conn:     数据库连接
        month:    可选，月份字符串 "YYYY-MM"，如 "2026-06"
        category: 可选，分类名称
    返回: pandas DataFrame（按日期降序排列）
    """
    query = "SELECT id, amount, category, date, note, created_at FROM entries WHERE 1=1"
    params = []

    if month:
        # strftime('%Y-%m', date) 提取日期中的年月部分进行匹配
        query += " AND strftime('%Y-%m', date) = ?"
        params.append(month)

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY date DESC, id DESC"

    df = pd.read_sql_query(query, conn, params=params)
    return df


# ==================================================
# 删 — 按 ID 删除账单
# ==================================================

def delete_entry(conn, entry_id):
    """
    根据 ID 删除一条账单记录。
    参数:
        conn:     数据库连接
        entry_id: 要删除的记录 ID（int）
    返回: True 表示删除成功，False 表示未找到该记录
    """
    c = conn.cursor()
    c.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    return c.rowcount > 0


# ==================================================
# 统计 — 分类汇总
# ==================================================

def get_category_stats(conn, month=None):
    """
    按分类统计总金额和记录条数。
    参数:
        conn:  数据库连接
        month: 可选，月份字符串 "YYYY-MM"，只统计该月数据
    返回: pandas DataFrame（包含 category, total_amount, count 三列）
    """
    query = """
        SELECT
            category,
            SUM(amount) AS total_amount,
            COUNT(*)    AS count
        FROM entries
    """
    params = []

    if month:
        query += " WHERE strftime('%Y-%m', date) = ?"
        params.append(month)

    query += " GROUP BY category ORDER BY total_amount DESC"

    df = pd.read_sql_query(query, conn, params=params)
    return df


# ==================================================
# 辅助 — 获取已有数据的年月列表
# ==================================================

def get_available_months(conn):
    """
    查询数据库中所有不同的年月值，用于筛选下拉菜单。
    返回: 字符串列表，如 ["2026-06", "2026-05", ...]
    """
    df = pd.read_sql_query(
        "SELECT DISTINCT strftime('%Y-%m', date) AS ym FROM entries ORDER BY ym DESC",
        conn
    )
    return df["ym"].tolist()
