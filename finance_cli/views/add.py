"""
====================================================
    录入账单页面 — 表单填写并提交新账单
====================================================
"""

import streamlit as st
from datetime import date
from db import add_entry, CATEGORIES


def render(conn):
    """
    渲染录入账单页面。
    conn: 数据库连接对象
    """
    st.header("📝 录入新账单")

    # 使用 st.form 包裹表单，防止每次组件交互都触发页面刷新
    with st.form("add_form", clear_on_submit=True):
        # --- 金额输入 ---
        amount = st.number_input(
            label="💰 金额（元）",
            min_value=0.01,
            max_value=999999.99,
            step=0.01,
            format="%.2f",
            help="请输入支出金额，保留两位小数"
        )

        # --- 分类选择 ---
        category = st.selectbox(
            label="📂 分类",
            options=CATEGORIES,
            help="请选择消费分类"
        )

        # --- 日期选择 ---
        entry_date = st.date_input(
            label="📅 日期",
            value=date.today(),
            max_value=date.today(),  # 不允许选择未来日期
            help="选择消费日期"
        )

        # --- 备注输入 ---
        note = st.text_area(
            label="📝 备注（选填）",
            max_chars=200,
            placeholder="例如：午饭外卖、地铁通勤……",
            help="可选填备注信息，最多 200 字"
        )

        # --- 提交按钮 ---
        submitted = st.form_submit_button("✅ 提交账单", type="primary")

        if submitted:
            if amount <= 0:
                st.error("❌ 金额必须大于 0，请重新输入")
            else:
                # 将日期转为 "YYYY-MM-DD" 格式的字符串存入数据库
                date_str = entry_date.strftime("%Y-%m-%d")
                add_entry(conn, amount, category, date_str, note)
                st.success(f"✅ 添加成功！{category} ¥{amount:.2f}")
                st.balloons()
