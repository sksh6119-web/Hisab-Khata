import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="হিসাব খাতা", page_icon="📖", layout="centered")

st.title("📖 হিসাব খাতা (Hisab Khata)")
st.write("আপনার দৈনন্দিন আয় এবং ব্যয়ের হিসাব রাখুন খুব সহজেই।")

# সেভ করার জন্য সেশন স্টেট ব্যবহার
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

with st.form("entry_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("তারিখ", datetime.now())
        trans_type = st.selectbox("খাতের ধরণ", ["আয় (Income)", "ব্যয় (Expense)"])
    with col2:
        amount = st.number_input("টাকার পরিমাণ (₹)", min_value=0.0, step=1.0)
        category = st.text_input("বিবরণ / ক্যাটাগরি", placeholder="যেমন: বাজার, দোকান বিক্রি ইত্যাদি")
    
    submitted = st.form_submit_button("হিসাব যোগ করুন")
    
    if submitted:
        if amount > 0:
            st.session_state.transactions.append({
                "তারিখ": str(date),
                "ধরণ": trans_type,
                "পরিমাণ (₹)": amount,
                "বিবরণ": category if category else "অন্যান্য"
            })
            st.success("হিসাব সফলভাবে যোগ করা হয়েছে!")
        else:
            st.warning("দয়া করে সঠিক টাকার পরিমাণ লিখুন।")

# হিসাবের তালিকা ও হিসাব নিকাশ
if len(st.session_state.transactions) > 0:
    st.divider()
    st.subheader("📊 সকল লেনদেনের তালিকা")
    
    df = pd.DataFrame(st.session_state.transactions)
    st.dataframe(df, use_container_width=True)
    
    # মোট আয় ও ব্যয়ের হিসাব
    total_income = df[df["ধরণ"] == "আয় (Income)"]["পরিমাণ (₹)"].sum()
    total_expense = df[df["ধরণ"] == "ব্যয় (Expense)"]["পরিমাণ (₹)"].sum()
    balance = total_income - total_expense
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("মোট আয়", f"₹ {total_income}")
    col_b.metric("মোট ব্যয়", f"₹ {total_expense}")
    col_c.metric("অবশিষ্ট জের", f"₹ {balance}")
else:
    st.info("এখনো কোনো হিসাব যোগ করা হয়নি। ওপরের ফর্ম থেকে হিসাব যোগ করা শুরু করুন।")
