import streamlit as st
import datetime
import urllib.parse

# Page configuration
st.set_page_config(
    page_title="Nasrin Bastralaya - Hisab Khata",
    page_icon="🌍",
    layout="centered"
)

# Custom CSS for OK Credit Style UI
st.markdown("""
    <style>
    .net-balance-card {
        background-color: #F0F3F4;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #D5D8DC;
        margin-bottom: 15px;
    }
    .customer-row {
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-bottom: 1px solid #EAEDED;
    }
    </style>
""", unsafe_allow_html=True)

# Multi-Language Support
LANGS = {
    "বাংলা (Bengali)": {
        "title": "🛍️ নাসরিন বস্ত্রালয় - হিসাব খাতা",
        "caption": "Digital Ledger & Collection System",
        "net_bal": "Net Balance (মোট হিসাব)",
        "you_get": "পাবেন (You'll Get)",
        "you_give": "দেবেন (You'll Give)",
        "search_ph": "খদ্দেরের নাম দিয়ে খুঁজুন...",
        "add_cust": "➕ নতুন খদ্দের যোগ"
    },
    "English": {
        "title": "🛍️ Nasrin Bastralaya - Hisab Khata",
        "caption": "Digital Ledger & Collection System",
        "net_bal": "Net Balance",
        "you_get": "You'll Get",
        "you_give": "You'll Give",
        "search_ph": "Search customer name...",
        "add_cust": "➕ Add Customer"
    },
    "हिन्दी (Hindi)": {
        "title": "🛍️ नसरीन वस्त्रालय - हिसाब खाता",
        "caption": "Digital Ledger & Collection System",
        "net_bal": "Net Balance",
        "you_get": "आपको मिलेगा",
        "you_give": "आपको देना है",
        "search_ph": "ग्राहक का नाम खोजें...",
        "add_cust": "➕ नया ग्राहक"
    }
}

selected_lang = st.sidebar.selectbox("🌐 ভাষা / Language", list(LANGS.keys()))
t = LANGS[selected_lang]

st.markdown(f"### {t['title']}")
st.caption(t['caption'])
st.markdown("---")

# Session State Initialization with OK Credit type data
if "customers" not in st.session_state:
    st.session_state.customers = {
        "L BABU": {
            "phone": "919876543210", 
            "balance": 6750, 
            "reg_date": "2024-01-10", 
            "transactions": [("2024-01-10", "Pending Collection Since 42 months", 6750)]
        },
        "ছবি ভাবি": {
            "phone": "919123456789", 
            "balance": 2010, 
            "reg_date": "2026-08-19", 
            "transactions": [("2026-08-19", "Credit Added", 2010)]
        },
        "জামাই কয়রাপুর": {
            "phone": "919111122223", 
            "balance": 0, 
            "reg_date": "2026-08-14", 
            "transactions": [("2026-08-14", "Payment Settled", 0)]
        },
        "চন্দন দাসপাড়া": {
            "phone": "919333344445", 
            "balance": 1250, 
            "reg_date": "2025-06-06", 
            "transactions": [("2025-06-06", "Credit Added", 1250)]
        }
    }

# OK Credit Style Navigation Tabs (Simulated via Sidebar or Radio)
app_tab = st.sidebar.radio("📋 মেনু (OK Credit Style)", ["Ledger (খাতা)", "Add Customer (নতুন খদ্দের)", "Transactions (লেনদেন)", "Auto-Reminders (অটো-মেসেজ)", "PDF Bills (বিল ও রিপোর্ট)", "Defaulter List (ডিফল্টার লিস্ট)"])

# 1. Ledger Tab (OK Credit Main Interface)
if app_tab == "Ledger (খাতা)":
    # Calculate Net Balance
    total_get = sum(data["balance"] for data in st.session_state.customers.values() if data["balance"] > 0)
    total_give = sum(abs(data["balance"]) for data in st.session_state.customers.values() if data["balance"] < 0)
    net_val = total_get - total_give
    
    # OK Credit Style Net Balance Box
    st.markdown(f"""
        <div class="net-balance-card">
            <span style="font-size: 14px; color: #566573; font-weight: bold;">{t['net_bal']}</span><br>
            <span style="font-size: 22px; font-weight: bold; color: {'#C0392B' if net_val > 0 else '#27AE60'};">₹ {net_val}</span>
            <span style="float: right; font-size: 14px; color: #566573; margin-top: 8px;">{t['you_get']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Search Bar
    search_q = st.text_input("🔍", placeholder=t["search_ph"], label_visibility="collapsed")
    st.markdown("---")
    
    # Customer List (OK Credit UI Look)
    for name, data in st.session_state.customers.items():
        if search_q and search_q.lower() not in name.lower():
            continue
            
        bal = data["balance"]
        # Check if defaulter (> 365 days)
        reg_date_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
        diff_days = (datetime.date.today() - reg_date_obj).days
        is_defaulter = diff_days > 365 and bal > 0
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            first_letter = name[0]
            st.markdown(f"**👤 {name}**")
            if is_defaulter:
                st.markdown(f"<span style='background-color: #FADBD8; color: #922B21; padding: 2px 6px; border-radius: 4px; font-size: 11px;'>⚠️ DEFAULTER ({diff_days//30} mos)</span>", unsafe_allow_html=True)
            else:
                st.caption(f"📱 {data['phone']}")
                
        with col2:
            if bal > 0:
                st.markdown(f"<div style='text-align: right; color: #C0392B; font-weight: bold;'>₹ {bal}<br><span style='font-size: 11px; color: #7F8C8D;'>Due</span></div>", unsafe_allow_html=True)
            elif bal < 0:
                st.markdown(f"<div style='text-align: right; color: #27AE60; font-weight: bold;'>₹ {abs(bal)}<br><span style='font-size: 11px; color: #7F8C8D;'>Advance</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: right; color: #2C3E50; font-weight: bold;'>₹ 0<br><span style='font-size: 11px; color: #7F8C8D;'>Settled</span></div>", unsafe_allow_html=True)
                
        with col3:
            if st.button("হিসাব", key=f"ledger_btn_{name}"):
                st.session_state.active_customer = name
                
        st.markdown("<hr style='margin: 4px 0px; opacity: 0.15;'>", unsafe_allow_html=True)
        
    # Selected Customer Details View
    if "active_customer" in st.session_state and st.session_state.active_customer in st.session_state.customers:
        ac_name = st.session_state.active_customer
        ac_data = st.session_state.customers[ac_name]
        st.markdown("---")
        st.subheader(f"📁 {ac_name} - Statement")
        for dt, desc, amt in ac_data["transactions"]:
            st.text(f"📅 {dt} | {desc} : ₹ {amt}")

# 2. Add Customer Tab
elif app_tab == "Add Customer (নতুন খদ্দের)":
    st.subheader("➕ নতুন খদ্দের যুক্ত করুন (OK Credit Style)")
    with st.form("add_cust_form"):
        c_name = st.text_input("খদ্দেরের নাম (Customer Name)")
        c_phone = st.text_input("WhatsApp নম্বর (Phone Number)")
        c_due = st.number_input("প্রারম্ভিক বাকি (Opening Due)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("সেভ করুন")
        
        if submitted and c_name:
            if c_name in st.session_state.customers:
                st.warning("এই নামের খদ্দের ইতিমধ্যেই আছে!")
            else:
                cur_date = str(datetime.date.today())
                st.session_state.customers[c_name] = {
                    "phone": c_phone,
                    "balance": c_due,
                    "reg_date": cur_date,
                    "transactions": [(cur_date, "Opening Balance", c_due)] if c_due > 0 else []
                }
                st.success(f"{c_name} সফলভাবে যোগ করা হয়েছে!")

# 3. Transactions Tab
elif app_tab == "Transactions (লেনদেন)":
    st.subheader("💰 লেনদেন রেকর্ড করুন (Give / Receive)")
    if not st.session_state.customers:
        st.warning("কোনো খদ্দের নেই।")
    else:
        sel_c = st.selectbox("খদ্দের বাছুন", list(st.session_state.customers.keys()))
        t_type = st.radio("ধরণ", ["মাল বাকি দেওয়া (You Gave)", "টাকা জমা নেওয়া (You Received)"])
        t_amt = st.number_input("টাকার পরিমাণ (₹)", min_value=1.0, step=10.0)
        t_note = st.text_input("নোট / বিল বিবরণী")
        
        if st.button("লেনদেন নিশ্চিত করুন"):
            today_str = str(datetime.date.today())
            if "Gave" in t_type:
                st.session_state.customers[sel_c]["balance"] += t_amt
                st.session_state.customers[sel_c]["transactions"].append((today_str, f"Gave: {t_note}", t_amt))
                st.success(f"₹ {t_amt} বাকি যোগ করা হয়েছে।")
            else:
                st.session_state.customers[sel_c]["balance"] -= t_amt
                st.session_state.customers[sel_c]["transactions"].append((today_str, f"Received: {t_note}", -t_amt))
                st.success(f"₹ {t_amt} জমা নেওয়া হয়েছে।")

# 4. Auto-Reminders Tab
elif app_tab == "Auto-Reminders (অটো-মেসেজ)":
    st.subheader("🤖 WhatsApp ও SMS অটো-রিমাইন্ডার")
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0:
            st.markdown(f"**👤 {name}** (বাকি: ₹ {data['balance']})")
            msg_text = f"নমস্কার {name}, নাসরিন বস্ত্রালয়-এ আপনার মোট বাকি ₹ {data['balance']} টাকা। দয়া করে শীঘ্রই পরিশোধ করুন।"
            ed_msg = st.text_area(f"মেসেজ ({name})", value=msg_text, key=f"auto_txt_{name}")
            
            ph = data["phone"]
            if ph:
                enc = urllib.parse.quote(ed_msg)
                wa_link = f"https://wa.me/{ph}?text={enc}"
                sms_link = f"sms:{ph}?body={enc}"
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25D366; color:white; padding:6px 12px; border:none; border-radius:5px; width:100%; font-weight:bold;">📱 WhatsApp Vasooli</button></a>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<a href="{sms_link}"><button style="background-color:#333; color:white; padding:6px 12px; border:none; border-radius:5px; width:100%; font-weight:bold;">✉️ SMS Reminder</button></a>', unsafe_allow_html=True)
            st.markdown("---")

# 5. PDF Bills Tab
elif app_tab == "PDF Bills (বিল ও রিপোর্ট)":
    st.subheader("📄 বিল এবং স্টেটমেন্ট রিপোর্ট")
    if st.session_state.customers:
        pdf_c = st.selectbox("গ্রাহক নির্বাচন", list(st.session_state.customers.keys()), key="pdf_sel")
        c_dat = st.session_state.customers[pdf_c]
        if st.button("বিল জেনারেট করুন"):
            st.success(f"✅ বিল তৈরি হয়েছে: {pdf_c}")
            st.write(f"**Nasrin Bastralaya (Tematha Bazar, Belshor)**")
            st.write(f"Customer: {pdf_c} | Phone: {c_dat['phone']}")
            st.write(f"Total Due: ₹ {c_dat['balance']}")
            st.markdown("---")
            for dt, ds, am in c_dat["transactions"]:
                st.text(f"{dt} | {ds} : ₹ {am}")
            st.info("💡 টিপস: ব্রাউজারের থ্রি-ডট মেনু থেকে 'Print / Save as PDF' সিলেক্ট করুন।")

# 6. Defaulter List Tab
elif app_tab == "Defaulter List (ডিফল্টার লিস্ট)":
    st.subheader("⚠️ দীর্ঘমেয়াদী বকেয়া ও ডিফল্টার তালিকা (OK Credit Style)")
    today_dt = datetime.date.today()
    found_def = False
    
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0 and "reg_date" in data:
            r_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
            d_diff = (today_dt - r_obj).days
            if d_diff > 365:
                found_def = True
                st.error(f"👤 **{name}** | বাকি: ₹ {data['balance']} | স্থায়িত্ব: {d_diff//30} মাস ধরে বকেয়া!")
                d_msg = f"জরুরি বার্তা: নাসরিন বস্ত্রালয়-এর দীর্ঘদিনের বকেয়া ₹ {data['balance']} দ্রুত পরিশোধ করুন।"
                d_enc = urllib.parse.quote(d_msg)
                d_wa = f"https://wa.me/{data['phone']}?text={d_enc}"
                st.markdown(f'<a href="{d_wa}" target="_blank"><button style="background-color:#E74C3C; color:white; padding:5px 12px; border:none; border-radius:4px; font-weight:bold;">⚠️ Remind Defaulter</button></a>', unsafe_allow_html=True)
                st.markdown("---")
    if not found_def:
        st.success("🎉 কোনো দীর্ঘমেয়াদী ডিফল্টার নেই!")
