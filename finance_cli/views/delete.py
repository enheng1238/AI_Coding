"""
====================================================
    删除账单页面 — 输入 ID 并确认后删除
====================================================
"""

import streamlit as st
from db import delete_entry


def render(conn):
    """
    渲染删除账单页面。
    conn: 数据库连接对象
    """
    st.header("🗑️ 删除账单")

    # 警告提示 — 删除不可撤销
    st.warning("⚠️ 删除操作不可撤销，请确认无误后再操作！")

    # --- 输入要删除的 ID ---
    delete_id = st.number_input(
        label="请输入要删除的账单编号（ID）",
        min_value=1,
        step=1,
        format="%d",
        help="账单的唯一编号，可在「查看账单」页面找到"
    )

    # --- 预览要删除的记录 ---
    with st.expander("🔍 点击查看此 ID 的账单详情"):
        c = conn.cursor()
        c.execute("SELECT * FROM entries WHERE id = ?", (int(delete_id),))
        row = c.fetchone()
        if row:
            st.write(f"**编号**: {row['id']}")
            st.write(f"**金额**: ¥{row['amount']:.2f}")
            st.write(f"**分类**: {row['category']}")
            st.write(f"**日期**: {row['date']}")
            st.write(f"**备注**: {row['note'] or '（无）'}")
        else:
            st.info("未找到此编号的记录")

    # --- 确认复选框 ---
    confirm = st.checkbox("✅ 我确认要删除这条记录")

    # --- 删除按钮 ---
    if st.button("🗑️ 删除", type="primary", disabled=not confirm):
        success = delete_entry(conn, int(delete_id))
        if success:
            st.success(f"✅ 已成功删除编号为 {delete_id} 的账单")
            st.rerun()  # 刷新页面，让用户看到变化
        else:
            st.error(f"❌ 未找到编号为 {delete_id} 的账单，请检查 ID 是否正确")
