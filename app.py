import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="নাসরিন বস্ত্রালয় - হিসাব খাতা", layout="centered")

# ডেটাবেজ ইনিশিয়ালাইজেশন
if "customers" not in st.session_state:
    st.session_state.customers = {
        "রহিম শেখ": {
            "phone": "919876543210", 
            "transactions": [
                {"date": "2026-06-01", "desc": "বাকি শাড়ি", "type": "Given", "amount": 4500}
            ]
        },
        "করিম মণ্ডল": {
            "phone": "919123456789", 
            "transactions": [
                {"date": "2026-06-05", "desc": "প্যান্ট ও শার্ট", "type": "Given", "amount": 1200}
            ]
        }
    }

if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None

st.title("📖 নাসরিন বস্ত্রালয় - হিসাব খাতা")
st.caption("OkCredit Style Digital Ledger System")
st.markdown("---")

# মোট হিসাব (Net Balance) বের করার ফাংশন
total_due = 0
for name, data in st.session_state.customers.items():
    cust_bal = sum([t['amount'] if t['type']=='Given' else -t['amount'] for t in data['transactions']])
    if cust_bal > 0:
        total_due += cust_bal

# ড্যাশবোর্ড ব্যালেন্স কার্ড
st.markdown(f"""
<div style="background-color: #F4F6F7; padding: 15px; border-radius: 10px; border: 1px solid #D5D8DC; margin-bottom: 15px;">
    <span style="font-size: 13px; color: #566573; font-weight: bold;">Net Balance (মোট হিসাব)</span><br>
    <span style="font-size: 24px; font-weight: bold; color: #C0392B;">₹ {total_due}</span>
    <span style="float: right; font-size: 13px; color: #7F8C8D; margin-top: 10px;">You'll Get (পাবেন)</span>
</div>
""", unsafe_allow_html=True)

# যদি কোনো খদ্দের সিলেক্ট করা না থাকে (মেইন লিস্ট ভিউ)
if st.session_state.selected_customer is None:
    
    # নতুন খদ্দের যোগ করার ফর্ম
    with st.expander("➕ নতুন খদ্দের যোগ করুন"):
        with st.form("add_cust"):
            new_name = st.text_input("খদ্দেরের নাম:")
            new_phone = st.text_input("WhatsApp নম্বর (যেমন: 919876543210):")
            submitted = st.form_submit_button("যোগ করুন")
            if submitted and new_name:
                if new_name in st.session_state.customers:
                    st.warning("এই নামের খদ্দের ইতিমধ্যেই আছে!")
                else:
                    st.session_state.customers[new_name] = {"phone": new_phone, "transactions": []}
                    st.success(f"{new_name} সফলভাবে যোগ করা হয়েছে!")
                    st.rerun()

    st.subheader("👥 খদ্দেরের তালিকা")
    search_txt = st.text_input("🔍 খদ্দেরের নাম দিয়ে খুঁজুন...")
    st.markdown("---")
    
    if not st.session_state.customers:
        st.info("কোনো খদ্দের নেই। উপরে নতুন খদ্দের যোগ করুন।")
    else:
        for name, data in st.session_state.customers.items():
            if search_txt and search_txt.lower() not in name.lower():
                continue
                
            # হিসাব কষা
            bal = sum([t['amount'] if t['type']=='Given' else -t['amount'] for t in data['transactions']])
            
            col1, col2, col3 = st.columns([2.5, 1.2, 1])
            with col1:
                # খদ্দেরের নামের ওপর ক্লিক করলে তার প্রোফাইল ওপেন হবে
                if st.button(f"👤 {name}", key=f"btn_{name}"):
                    st.session_state.selected_customer = name
                    st.rerun()
                st.caption(f"📱 {data['phone']}")
            with col2:
                if bal > 0:
                    st.markdown(f"<div style='text-align: right; color: #C0392B; font-weight: bold;'>₹ {bal}<br><span style='font-size: 10px; color: #7F8C8D;'>Due</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: right; color: #27AE60; font-weight: bold;'>₹ 0<br><span style='font-size: 10px; color: #7F8C8D;'>Settled</span></div>", unsafe_allow_html=True)
            with col3:
                if data['phone']:
                    wa_msg = f"Namaskar {name}, apnar dokane mot baki ache: Rs. {bal}. Anugraho kore porishodh korun."
                    wa_url = f"https://wa.me/{data['phone']}?text={urllib.parse.quote(wa_msg)}"
                    st.markdown(f"<a href='{wa_url}' target='_blank'><button style='background-color:#25D366; color:white; border:none; border-radius:4px; padding:5px 8px; font-size:11px; font-weight:bold;'>💬 WA</button></a>", unsafe_allow_html=True)
            st.markdown("<hr style='margin: 4px 0px; opacity: 0.15;'>", unsafe_allow_html=True)

# যদি কোনো নির্দিষ্ট খদ্দেরের নামের ওপর ক্লিক করা হয় (OkCredit Ledger Page)
else:
    cust = st.session_state.selected_customer
    data = st.session_state.customers[cust]
    
    if st.button("⬅️ খদ্দেরের তালিকায় ফিরে যান"):
        st.session_state.selected_customer = None
        st.rerun()
        
    st.markdown(f"### 👤 {cust} - এর খাতা")
    cust_bal = sum([t['amount'] if t['type']=='Given' else -t['amount'] for t in data['transactions']])
    st.write(f"বর্তমান বাকি: **₹ {cust_bal}**")
    st.markdown("---")
    
    # লেনদেন এন্ট্রি করার অপশন (Given / Got Buttons)
    st.subheader("নতুন এন্ট্রি যোগ করুন:")
    with st.form("txn_entry_form"):
        t_type = st.radio("লেনদেনের ধরন:", ["🔴 আপনি মাল দিলেন (You Gave)", "🟢 টাকা পেলেন (You Got)"], horizontal=True)
        t_amount = st.number_input("টাকার পরিমাণ (₹):", min_value=1.0, step=10.0)
        t_desc = st.text_input("বিবরণ বা আইটেমের নাম (যেমন: শাড়ি, ক্যাশ ইত্যাদি):")
        
        save_txn = st.form_submit_button("এন্ট্রি সেভ করুন")
        if save_txn:
            actual_type = "Given" if "Given" in t_type else "Got"
            new_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "desc": t_desc if t_desc else "General",
                "type": actual_type,
                "amount": t_amount
            }
            st.session_state.customers[cust]['transactions'].append(new_entry)
            st.success("হিসাব সফলভাবে সেভ করা হয়েছে!")
            st.rerun()

    st.markdown("---")
    st.subheader("📜 লেনদেনের ইতিহাস (History)")
    if not data['transactions']:
        st.info("কোনো লেনদেন নেই।")
    else:
        for t in reversed(data['transactions']):
            color = "#C0392B" if t['type'] == "Given" else "#27AE60"
            sign = "+ ₹" if t['type'] == "Given" else "- ₹"
            st.markdown(f"""
                <div style="background-color: #FAFAFA; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 4px solid {color};">
                    <small style="color: gray;">{t['date']}</small><br>
                    <b>{t['desc']}</b>
                    <span style="float: right; color: {color}; font-weight: bold;">{sign} {t['amount']}</span>
                </div>
            """, unsafe_allow_html=True)
