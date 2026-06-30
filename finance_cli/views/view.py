"""
====================================================
    查看账单页面 — 按月份和分类筛选，表格展示
====================================================
"""

import streamlit as st
from db import get_entries, get_available_months, CATEGORIES


def render(conn):
    """
    渲染查看账单页面。
    conn: 数据库连接对象
    """
    st.header("📋 账单列表")

    # --- 获取可用月份列表 ---
    available_months = get_available_months(conn)

    # --- 筛选区域：两列并排 ---
    col1, col2 = st.columns(2)

    with col1:
        # 月份筛选下拉框（"全部" + 已有月份）
        month_options = ["全部"] + available_months
        selected_month = st.selectbox(
            label="📅 选择月份",
            options=month_options,
            help="按月份筛选账单"
        )

    with col2:
        # 分类筛选下拉框
        category_options = ["全部"] + CATEGORIES
        selected_category = st.selectbox(
            label="📂 选择分类",
            options=category_options,
            help="按分类筛选账单"
        )

    # --- 查询数据 ---
    # 只有选了具体月份/分类才传参数，"全部"则不筛选
    month = None if selected_month == "全部" else selected_month
    category = None if selected_category == "全部" else selected_category

    df = get_entries(conn, month=month, category=category)

    # --- 展示数据 ---
    if df.empty:
        st.info("📭 暂无符合条件的账单记录，去录入一笔吧！")
    else:
        # 格式化金额列，添加 ¥ 符号
        display_df = df.copy()
        display_df["amount"] = display_df["amount"].map("¥{:.2f}".format)

        # 重新排序列并重命名，让表格更易读
        display_df = display_df[["id", "amount", "category", "date", "note", "created_at"]]
        display_df.columns = ["编号", "金额", "分类", "日期", "备注", "创建时间"]

        st.dataframe(
            display_df,
            use_container_width=True,
            height=400,
            hide_index=True  # 隐藏 DataFrame 默认的行索引
        )

        st.caption(f"共 {len(df)} 条记录")
