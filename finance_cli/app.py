"""
====================================================
    家庭记账工具 — 主入口
    技术栈: Python + Streamlit + SQLite3

    运行方式:
        streamlit run app.py

    浏览器访问 http://localhost:8501
====================================================
"""

import streamlit as st
from db import init_db, CATEGORIES
from views.add import render as render_add
from views.view import render as render_view
from views.delete import render as render_delete
from views.statistics import render as render_statistics


def main():
    """应用主函数：配置页面 → 初始化数据库 → 侧边栏导航 → 路由分发"""

    # ---------- 页面全局配置 ----------
    st.set_page_config(
        page_title="家庭记账工具",
        page_icon="💰",
        layout="centered"  # 居中布局，阅读体验更好
    )

    # ---------- 顶部标题 ----------
    st.title("💰 家庭记账工具")
    st.caption("简单好用的个人收支管理小工具")

    # ---------- 初始化数据库 ----------
    conn = init_db()

    # ---------- 侧边栏导航 ----------
    st.sidebar.title("📌 导航菜单")
    page = st.sidebar.radio(
        "选择功能",
        options=["录入账单", "查看账单", "删除账单", "分类统计"]
    )

    # ---------- 路由分发 ----------
    if page == "录入账单":
        render_add(conn)
    elif page == "查看账单":
        render_view(conn)
    elif page == "删除账单":
        render_delete(conn)
    elif page == "分类统计":
        render_statistics(conn)

    # ---------- 关闭数据库连接 ----------
    conn.close()


if __name__ == "__main__":
    main()
