"""
====================================================
    分类统计页面 — 柱状图 + 分类汇总表
====================================================
"""

import streamlit as st
from db import get_category_stats, get_available_months


def render(conn):
    """
    渲染分类统计页面。
    conn: 数据库连接对象
    """
    st.header("📊 分类统计")

    # --- 月份筛选 ---
    available_months = get_available_months(conn)
    month_options = ["全部"] + available_months

    selected_month = st.selectbox(
        label="📅 选择月份",
        options=month_options,
        key="stats_month",  # 独立的 key，避免与其他页面冲突
        help="选择要统计的月份，选「全部」则统计所有数据"
    )

    # --- 查询统计数据 ---
    month = None if selected_month == "全部" else selected_month
    stats_df = get_category_stats(conn, month=month)

    if stats_df.empty:
        st.info("📭 暂无统计数据，先去录入账单吧！")
        return

    # --- 展示区域：左右两列 ---
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("📈 分类支出柱状图")

        # st.bar_chart 需要以分类为索引的 Series/DataFrame
        chart_data = stats_df.set_index("category")["total_amount"]
        st.bar_chart(chart_data)

    with col2:
        st.subheader("📋 分类支出详情")

        # 格式化金额
        display_df = stats_df.copy()
        display_df["total_amount"] = display_df["total_amount"].map("¥{:.2f}".format)
        display_df.columns = ["分类", "总金额", "笔数"]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    # --- 底部汇总 ---
    total_amount = stats_df["total_amount"].sum()
    total_count = int(stats_df["count"].sum())
    st.metric(label="💰 总支出", value=f"¥{total_amount:.2f}")
    st.caption(f"共 {total_count} 笔记录")
