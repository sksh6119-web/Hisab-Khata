import streamlit as st
import datetime
import urllib.parse

# Page configuration with Earth Logo Favicon & Wide/Centered layout
st.set_page_config(
    page_title="Nasrin Bastralaya - Hisab Khata",
    page_icon="🌍",
    layout="centered"
)

# Custom CSS styling for OK Credit / KhataBook UI look & feel
st.markdown("""
    <style>
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 14px;
        color: #7F8C8D;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #27AE60;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .due-card {
        background-color: #FDEDEC;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #E74C3C;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Multi-Language Dictionary (Indian Languages Support)
LANGS = {
    "বাংলা (Bengali)": {
        "title": "🛍️ নাসরিন বস্ত্রালয় - হিসাব খাতা",
        "caption": "OK Credit স্টাইল ডিজিটাল খাতা ও অটো-রিমাইন্ডার সিস্টেম",
        "menu_select": "মেনু নির্বাচন করুন",
        "dash": "📊 ড্যাশবোর্ড ও খাতা",
        "add_cust": "➕ নতুন খদ্দের যোগ",
        "trans": "💰 লেনদেন (টাকা জমা/বাকি)",
        "auto_msg": "🤖 প্রতিদিনের অটো-মেসেজ",
        "pdf_rep": "📄 বিল ও রিপোর্ট",
        "def_list": "⚠️ এক বছরের পুরনো ডিফল্টার লিস্ট",
        "total_due": "মোট পাওনা টাকা (Total Market Dues)",
        "total_advance": "মোট জমা টাকা (Advance)",
        "no_cust": "এখনো কোনো খদ্দেরের হিসাব যোগ করা হয়নি।",
        "search_ph": "খদ্দেরের নাম দিয়ে খুঁজুন..."
    },
    "हिन्दी (Hindi)": {
        "title": "🛍️ नसरीन वस्त्रालय - हिसाब खाता",
        "caption": "OK Credit स्टाइल डिजिटल खाता और ऑटो-रिमाइंडर",
        "menu_select": "मेनू चुनें",
        "dash": "📊 डैशबोर्ड और खाता",
        "add_cust": "➕ नया ग्राहक जोड़ें",
        "trans": "💰 लेनदेन (उधार/जमा)",
        "auto_msg": "🤖 दैनिक ऑटो-मैसेज",
        "pdf_rep": "📄 बिल और रिपोर्ट",
        "def_list": "⚠️ एक साल पुरानी डिफॉल्टर लिस्ट",
        "total_due": "कुल बाकी राशि (Total Market Dues)",
        "total_advance": "कुल जमा राशि (Advance)",
        "no_cust": "अभी तक कोई ग्राहक नहीं जोड़ा गया है।",
        "search_ph": "ग्राहक का नाम खोजें..."
    },
    "English": {
        "title": "🛍️ Nasrin Bastralaya - Hisab Khata",
        "caption": "OK Credit Style Digital Ledger & Auto-Reminders",
        "menu_select": "Select Menu",
        "dash": "📊 Dashboard & Ledger",
        "add_cust": "➕ Add New Customer",
        "trans": "💰 Transactions (Give/Receive)",
        "auto_msg": "🤖 Daily Auto-Messages",
        "pdf_rep": "📄 Bills & Reports",
        "def_list": "⚠️ 1+ Year Defaulter List",
        "total_due": "Total Market Dues",
        "total_advance": "Total Advance",
        "no_cust": "No customer records added yet.",
        "search_ph": "Search customer name..."
    }
}

# Language Selector in Sidebar
selected_lang = st.sidebar.selectbox("🌐 ভাষা / भाषा / Language", list(LANGS.keys()))
t = LANGS[selected_lang]

# App Header Display
st.markdown(f'<div class="main-header">{t["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{t["caption"]}</div>', unsafe_allow_html=True)
st.markdown("---")

# Session State for Data Storage
if "customers" not in st.session_state:
    st.session_state.customers = {
        "রহিম শেখ": {
            "phone": "919876543210", 
            "balance": 4500, 
            "reg_date": "2024-01-10", 
            "transactions": [("2024-01-10", "বাকি শাড়ি", 4500)]
        },
        "করিম মণ্ডল": {
            "phone": "919123456789", 
            "balance": -500, # Advance example
            "reg_date": "2026-06-05", 
            "transactions": [("2026-06-05", "অগ্রিম জমা", -500)]
        }
    }

# Sidebar Navigation Menu (OK Credit Style Icons)
menu = st.sidebar.selectbox(t["menu_select"], [
    t["dash"], 
    t["add_cust"], 
    t["trans"], 
    t["auto_msg"], 
    t["pdf_rep"],
    t["def_list"]
])

# 1. Dashboard & Ledger (OK Credit Style Card Layout)
if menu == t["dash"]:
    if not st.session_state.customers:
        st.info(t["no_cust"])
    else:
        # Calculate totals
        total_market_due = sum(data["balance"] for data in st.session_state.customers.values() if data["balance"] > 0)
        total_advance = sum(abs(data["balance"]) for data in st.session_state.customers.values() if data["balance"] < 0)
        
        # OK Credit Style Top Summary Cards
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.error(f"🔴 {t['total_due']}\n\n### ₹ {total_market_due}")
        with col_m2:
            st.success(f"🟢 {t['total_advance']}\n\n### ₹ {total_advance}")
        
        st.markdown("---")
        
        # Search filter bar
        search_query = st.text_input("🔍", placeholder=t["search_ph"], label_visibility="collapsed")
        
        # Customer List Loop
        for name, data in st.session_state.customers.items():
            if search_query and search_query.lower() not in name.lower():
                continue
                
            bal = data["balance"]
            # Formatting color & text style based on balance
            if bal > 0:
                status_text = f"পাবেন (You'll Get): ₹ {bal}"
                card_style = "due-card"
            elif bal < 0:
                status_text = f"দেবেন (You'll Give): ₹ {abs(bal)}"
                card_style = "metric-card"
            else:
                status_text = "হিসাব সমান (Settled)"
                card_style = "metric-card"
                
            with st.container():
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    st.markdown(f"**👤 {name}**")
                    st.caption(f"📱 {data['phone']}")
                with c2:
                    if bal > 0:
                        st.markdown(f"<span style='color: #E74C3C; font-weight: bold;'>{status_text}</span>", unsafe_allow_html=True)
                    elif bal < 0:
                        st.markdown(f"<span style='color: #27AE60; font-weight: bold;'>{status_text}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='color: #2C3E50; font-weight: bold;'>{status_text}</span>", unsafe_allow_html=True)
                with c3:
                    if st.button("হিসাব", key=f"btn_{name}"):
                        st.session_state.selected_customer = name
                st.markdown("<hr style='margin: 5px 0px; opacity: 0.2;'>", unsafe_allow_html=True)

        # Selected Customer Detail View
        if "selected_customer" in st.session_state and st.session_state.selected_customer in st.session_state.customers:
            c_name = st.session_state.selected_customer
            c_data = st.session_state.customers[c_name]
            st.markdown("---")
            st.subheader(f"📁 {c_name}-এর হিসাবের বিবরণী (Statement)")
            for date, desc, amt in c_data["transactions"]:
                amt_str = f"₹ {amt}" if amt > 0 else f"₹ {abs(amt)} (জমা)"
                st.text(f"📅 {date} | {desc} : {amt_str}")

# 2. Add New Customer
elif menu == t["add_cust"]:
    st.subheader("➕ নতুন খদ্দের যুক্ত করুন")
    with st.form("add_customer_form"):
        new_name = st.text_input("খদ্দেরের নাম (Name)")
        new_phone = st.text_input("হোয়াটসঅ্যাপ ফোন নম্বর (Phone Number)")
        initial_due = st.number_input("প্রারম্ভিক বাকি বা লেনদেন (Opening Balance)", min_value=0.0, step=10.0)
        submit_btn = st.form_submit_button("খদ্দের সেভ করুন")
        
        if submit_btn and new_name:
            if new_name in st.session_state.customers:
                st.warning("এই নামের খদ্দের ইতিমধ্যেই তালিকায় আছে!")
            else:
                current_date = str(datetime.date.today())
                st.session_state.customers[new_name] = {
                    "phone": new_phone,
                    "balance": initial_due,
                    "reg_date": current_date,
                    "transactions": [(current_date, "প্রাথমিক হিসাব", initial_due)] if initial_due > 0 else []
                }
                st.success(f"સফলভাবে {new_name}-এর হিসাব যোগ করা হয়েছে!")

# 3. Transaction Management (Give/Receive)
elif menu == t["trans"]:
    st.subheader("💰 টাকা বাকি দেওয়া অথবা জমা নেওয়া")
    if not st.session_state.customers:
        st.warning("প্রথমে খদ্দের যুক্ত করুন।")
    else:
        selected_cust = st.selectbox("খদ্দের নির্বাচন করুন", list(st.session_state.customers.keys()))
        trans_type = st.radio("লেনদেনের ধরন", ["মাল বাকি দেওয়া (You Gave)", "টাকা জমা নেওয়া (You Received)"])
        amount = st.number_input("টাকার পরিমাণ (₹)", min_value=1.0, step=10.0)
        note = st.text_input("বিল বিবরণ / নোট (Note, e.g., Bill No / Items)")
        
        if st.button("লেনদেন রেকর্ড করুন"):
            current_date = str(datetime.date.today())
            if "বাকি" in trans_type or "Gave" in trans_type:
                st.session_state.customers[selected_cust]["balance"] += amount
                st.session_state.customers[selected_cust]["transactions"].append((current_date, f"বাকি: {note}", amount))
                st.success(f"সফলভাবে ₹ {amount} বাকি যোগ করা হয়েছে।")
            else:
                st.session_state.customers[selected_cust]["balance"] -= amount
                st.session_state.customers[selected_cust]["transactions"].append((current_date, f"জমা: {note}", -amount))
                st.success(f"সফলভাবে ₹ {amount} জমা নেওয়া হয়েছে।")

# 4. Daily Auto-Message & Reminders
elif menu == t["auto_msg"]:
    st.subheader("🤖 প্রতিদিনের অটো-জেনারেটেড WhatsApp ও SMS রিমাইন্ডার")
    if not st.session_state.customers:
        st.info("কোনো খদ্দেরের ডেটা নেই।")
    else:
        for name, data in st.session_state.customers.items():
            if data["balance"] > 0:
                st.markdown(f"### 👤 {name} (বাকি: ₹ {data['balance']})")
                auto_msg = f"নমস্কার {name}, নাসরিন বস্ত্রালয় থেকে জানানো যাচ্ছে যে আপনার মোট বাকি ₹ {data['balance']} টাকা। দয়া করে দ্রুত দোকানে এসে হিসাব পরিশোধ করুন।"
                edited_msg = st.text_area(f"মেসেজ ({name})", value=auto_msg, key=f"msg_{name}")
                
                c_phone = data["phone"]
                if c_phone:
                    encoded_msg = urllib.parse.quote(edited_msg)
                    wa_url = f"https://wa.me/{c_phone}?text={encoded_msg}"
                    sms_url = f"sms:{c_phone}?body={encoded_msg}"
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:8px 15px; border:none; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">📱 WhatsApp পাঠান</button></a>', unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f'<a href="{sms_url}"><button style="background-color:#007bff; color:white; padding:8px 15px; border:none; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">✉️ সাধারণ SMS পাঠান</button></a>', unsafe_allow_html=True)
                else:
                    st.warning("ফোন নম্বর নেই।")
                st.markdown("---")

# 5. PDF Bill & Report
elif menu == t["pdf_rep"]:
    st.subheader("📄 বিল ও স্টেটমেন্ট প্রিন্ট বা পিডিএফ")
    if not st.session_state.customers:
        st.info("কোনো ডেটা নেই।")
    else:
        pdf_cust = st.selectbox("খদ্দের বাছুন", list(st.session_state.customers.keys()))
        c_info = st.session_state.customers[pdf_cust]
        
        if st.button("বিল রিপোর্ট তৈরি করুন"):
            st.success(f"✅ বিল প্রস্তুত!")
            st.write(f"**ব্যবসা:** নাসরিন বস্ত্রালয় (তেমাথা বাজার, বেলসর)")
            st.write(f"**গ্রাহক:** {pdf_cust}")
            st.write(f"**ফোন:** {c_info['phone']}")
            st.write(f"**বর্তমান মোট বাকি:** ₹ {c_info['balance']}")
            st.write("---")
            for dt, desc, amt in c_info["transactions"]:
                st.text(f"• {dt} | {desc} : ₹ {amt}")
            st.info("💡 টিপস: মোবাইল ব্রাউজারের ৩ ডট মেনু থেকে 'Print / Save as PDF' অপশন সিলেক্ট করে পিডিএফ বানিয়ে নিন।")

# 6. Defaulter List (1+ Year Old Dues)
elif menu == t["def_list"]:
    st.subheader("⚠️ ১ বছরের বেশি পুরনো ডিফল্টার (বিলার) তালিকা")
    today = datetime.date.today()
    defaulters_found = False
    
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0 and "reg_date" in data:
            reg_date_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
            diff_days = (today - reg_date_obj).days
            
            if diff_days > 365:
                defaulters_found = True
                st.error(f"👤 **{name}** | ফোন: {data['phone']} | বাকি: ₹ {data['balance']} | স্থায়িত্ব: {diff_days} দিন!")
                
                def_msg = f"জরুরি বার্তা: নমস্কার {name}, নাসরিন বস্ত্রালয়-এ আপনার দীর্ঘদিনের বকেয়া ₹ {data['balance']} টাকা দ্রুত পরিশোধ করুন।"
                encoded_def_msg = urllib.parse.quote(def_msg)
                def_wa_url = f"https://wa.me/{data['phone']}?text={encoded_def_msg}"
                
                st.markdown(f'<a href="{def_wa_url}" target="_blank"><button style="background-color:#E74C3C; color:white; padding:6px 15px; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">⚠️ ডিফল্টারকে WhatsApp রিমাইন্ডার</button></a>', unsafe_allow_html=True)
                st.markdown("---")
                
    if not defaulters_found:
        st.success("🎉 চমৎকার! ১ বছরের বেশি পুরনো কোনো ডিফল্টার বাকি নেই।")
