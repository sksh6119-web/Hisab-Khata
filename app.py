from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="নাসরিন বস্ত্রালয় - খাতা", page_icon="📖", layout="centered"
)

st.title("📖 নাসরিন বস্ত্রালয় - কাস্টমার খাতা")
st.write("আপনার কাস্টমারদের বাকি ও জমার হিসাব খুব সহজেই রাখুন।")

# Session state to store customer ledger data
if "ledger" not in st.session_state:
  st.session_state.ledger = pd.DataFrame(
      columns=["তারিখ", "কাস্টমারের নাম", "ধরণ", "টাকার পরিমাণ", "বিবরণ"]
  )

# Sidebar or main form to add entry
st.subheader("➕ নতুন লেনদেন যোগ করুন")
with st.form("ledger_form"):
  col1, col2 = st.columns(2)
  with col1:
    date = st.date_input("তারিখ", datetime.now())
  with col2:
    trans_type = st.selectbox(
        "লেনদেনের ধরণ", ["বাকি (Due/Credit)", "জমা/পেমেন্ট (Payment)"]
    )

  customer_name = st.text_input("কাস্টমারের নাম")
  amount = st.number_input(
      "টাকার পরিমাণ (₹)", min_value=0.0, format="%.2f", step=10.0
  )
  description = st.text_input("বিবরণ (যেমন: শাড়ি, কুর্তি ইত্যাদি)")

  submitted = st.form_submit_button("হিসাব যোগ করুন")
  if submitted:
    if customer_name.strip() == "":
      st.error("দয়া করে কাস্টমারের নাম লিখুন!")
    elif amount <= 0:
      st.error("সঠিক টাকার পরিমাণ দিন!")
    else:
      new_row = {
          "তারিখ": str(date),
          "কাস্টমারের নাম": customer_name.strip(),
          "ধরণ": trans_type,
          "টাকার পরিমাণ": amount,
          "বিবরণ": description,
      }
      st.session_state.ledger = pd.concat(
          [st.session_state.ledger, pd.DataFrame([new_row])], ignore_index=True
      )
      st.success(f"✅ {customer_name}-এর হিসাব সফলভাবে যোগ করা হয়েছে!")

st.markdown("---")
st.subheader("📋 কাস্টমার লেনদেন তালিকা")

if st.session_state.ledger.empty:
  st.info("এখনো কোনো হিসাব যোগ করা হয়নি। ওপরের ফর্ম থেকে হিসাব যোগ করা শুরু করুন।")
else:
  # Display data table
  st.dataframe(st.session_state.ledger, use_container_width=True)

  # Summary calculation
  df = st.session_state.ledger
  total_due = df[df["ধরণ"] == "বাকি (Due/Credit)"]["টাকার পরিমাণ"].sum()
  total_paid = df[df["ধরণ"] == "জমা/পেমেন্ট (Payment)"]["টাকার পরিমাণ"].sum()
  net_balance = total_due - total_paid

  st.markdown("### 📊 হিসাবের সারসংক্ষেপ")
  mcol1, mcol2, mcol3 = st.columns(3)
  mcol1.metric("মোট বাকি (Total Due)", f"₹ {total_due:.2f}")
  mcol2.metric("মোট জমা (Total Paid)", f"₹ {total_paid:.2f}")
  mcol3.metric("নেট পাওনা (Net Balance)", f"₹ {net_balance:.2f}")
