import streamlit as st
import datetime
import urllib.parse

st.set_page_config(
    page_title="নাসরিন বস্ত্রালয় - হিসাব খাতা",
    page_icon="📖",
    layout="centered"
)

# একদম খালি ডেটাবেজ (কোনো পূর্বনির্ধারিত নাম রাখা হয়নি)
if "customers" not in st.session_state:
    st.session_state.customers = {}

if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None

st.title("📖 নাসরিন বস্ত্রালয় - হিসাব খাতা")
st.caption("OkCredit Style Digital Ledger System")
st.markdown("---")

# মোট নেট ব্যালেন্স (Net Balance) হিসাব
total_due = 0
for name, data in st.session_state.customers.items():
    cust_bal = sum([t['amount'] if t['type']=='Given' else -t['amount'] for t in data['transactions']])
    if cust_bal > 0:
        total_due += cust_bal

st.markdown(f"""
<div style="background-color: #F8F9F9; padding: 16px; border-radius: 8px; border: 1px solid #D5D8DC; margin-bottom: 20px;">
    <div style="font-size: 13px; color: #566573; font-weight: bold;">Net Balance (মোট হিসাব)</div>
    <div style="font-size: 24px; font-weight: bold; color: #C0392B; margin-top: 5px;">₹ {total_due}</div>
    <div style="font-size: 13px; color: #7F8C8D; float: right; margin-top: -25px;">You'll Get (পাবেন)</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.selected_customer is None:
    # নতুন খদ্দের যোগ করার এক্সপ্যান্ডার
    with st.expander("➕ নতুন খদ্দের যোগ করুন"):
        with st.form("add_cust_form"):
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
        st.info("আপনার খাতায় এখনো কোনো খদ্দের নেই। উপরে 'নতুন খদ্দের যোগ করুন' থেকে খদ্দের যোগ করুন।")
    else:
        for name, data in st.session_state.customers.items():
            if search_txt and search_txt.lower() not in name.lower():
                continue
                
            bal = sum([t['amount'] if t['type']=='Given' else -t['amount'] for t in data['transactions']])
            
            col1, col2, col3 = st.columns([2.2, 1.3, 1])
            with col1:
                if st.button(f"👤 {name}", key=f"btn_{name}", use_container_width=True):
                    st.session_state.selected_customer = name
                    st.rerun()
                st.caption(f"📱 {data['phone']}")
            with col2:
                if bal > 0:
                    st.markdown(f"<div style='text-align: right; color: #C0392B; font-weight: bold; padding-top: 5px;'>₹ {bal}<br><span style='font-size: 10px; color: #7F8C8D;'>Due</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: right; color: #27AE60; font-weight: bold; padding-top: 5px;'>₹ 0<br><span style='font-size: 10px; color: #7F8C8D;'>Settled</span></div>", unsafe_allow_html=True)
            with col3:
                if data['phone']:
                    wa_msg = f"নমস্কার {name}, নাসরিন বস্ত্রালয় থেকে আপনার মোট বাকি ₹ {bal} টাকা পরিশোধ করার জন্য অনুরোধ করা হচ্ছে।"
                    wa_url = f"https://wa.me/{data['phone']}?text={urllib.parse.quote(wa_msg)}"
                    st.markdown(f"<a href='{wa_url}' target='_blank'><button style='background-color:#25D366; color:white; border:none; border-radius:4px; padding:6px 10px; font-size:12px; font-weight:bold; width:100%; margin-top:5px;'>💬 WA</button></a>", unsafe_allow_html=True)
            
            st.markdown("<div style='border-bottom: 1px solid #EAEDED; margin: 8px 0px;'></div>", unsafe_allow_html=True)

else:
    cust = st.session_state.selected_customer
    data = st.session_state.customers[cust]
    
    if st.button("⬅️ খদ্দেরের তালিকায় ফিরে যান"):
        st.session_state.selected_customer = None
        st.rerun()
        
    st.markdown(f"### 👤 {cust} - এর হিসাব খাতা")
    cust_bal = sum([t['amount'] if t['type']=='Given' else -t['amount'] for t in data['transactions']])
    st.write(f"মোট বকেয়া: **₹ {cust_bal}**")
    st.markdown("---")
    
    st.subheader("নতুন এন্ট্রি যোগ করুন:")
    with st.form("txn_entry_form"):
        t_type = st.radio("লেনদেনের ধরন:", ["🔴 আপনি মাল দিলেন (You Gave)", "🟢 টাকা পেলেন (You Got)"], horizontal=True)
        t_amount = st.number_input("টাকার পরিমাণ (₹):", min_value=1.0, step=10.0)
        t_desc = st.text_input("বিবরণ বা আইটেমের নাম (যেমন: শাড়ি, প্যান্ট ইত্যাদি):")
        
        save_txn = st.form_submit_button("এন্ট্রি সেভ করুন")
        if save_txn:
            actual_type = "Given" if "Given" in t_type else "Got"
            new_entry = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
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
                <div style="background-color: #F8F9F9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid {color}; border: 1px solid #E5E7E9;">
                    <span style="font-size: 11px; color: #7F8C8D;">{t['date']}</span><br>
                    <b style="font-size: 15px; color: #2C3E50;">{t['desc']}</b>
                    <span style="float: right; color: {color}; font-weight: bold; font-size: 16px;">{sign} {t['amount']}</span>
                </div>
            """, unsafe_allow_html=True)
