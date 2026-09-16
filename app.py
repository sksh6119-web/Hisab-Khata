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
    .stButton>button {
        border-radius: 6px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Multi-Language Support
LANGS = {
    "বাংলা (Bengali)": {
        "title": "🛍️ নাসরিন বস্ত্রালয় - হিসাব খাতা",
        "caption": "Smart Ledger, Voice Bill & PDF System",
        "net_bal": "Net Balance (মোট হিসাব)",
        "you_get": "পাবেন (You'll Get)",
        "you_give": "দেবেন (You'll Give)",
        "search_ph": "খদ্দেরের নাম দিয়ে খুঁজুন...",
        "add_cust": "➕ নতুন খদ্দের যোগ"
    },
    "English": {
        "title": "🛍️ Nasrin Bastralaya - Hisab Khata",
        "caption": "Smart Ledger, Voice Bill & PDF System",
        "net_bal": "Net Balance",
        "you_get": "You'll Get",
        "you_give": "You'll Give",
        "search_ph": "Search customer name...",
        "add_cust": "➕ Add Customer"
    }
}

selected_lang = st.sidebar.selectbox("🌐 ভাষা / Language", list(LANGS.keys()))
t = LANGS[selected_lang]

st.markdown(f"### {t['title']}")
st.caption(t['caption'])
st.markdown("---")

# Session State Initialization
if "customers" not in st.session_state:
    st.session_state.customers = {
        "রহিম শেখ": {
            "phone": "919876543210", 
            "balance": 4500, 
            "reg_date": "2024-01-10", 
            "transactions": [("2024-01-10", "বাকি শাড়ি - ₹4500", 4500)]
        },
        "করিম মণ্ডল": {
            "phone": "919123456789", 
            "balance": 1200, 
            "reg_date": "2026-06-05", 
            "transactions": [("2026-06-05", "প্যান্ট ও শার্ট বাকি - ₹1200", 1200)]
        }
    }

# Sidebar Navigation (OK Credit Style Tabs)
app_tab = st.sidebar.radio("📋 মেনু (OK Credit Style)", [
    "Ledger (খাতা)", 
    "Add Customer (খদ্দের যোগ)", 
    "Voice & Item Billing (ভয়েস ও মাল বাকি বিল)", 
    "Auto-Reminders (অটো-মেসেজ ও ভয়েস)", 
    "PDF Bill Report (পিডিএফ বিল রিপোর্ট)", 
    "Defaulter List (ডিফল্টার লিস্ট)"
])

# 1. Ledger Tab
if app_tab == "Ledger (খাতা)":
    total_get = sum(data["balance"] for data in st.session_state.customers.values() if data["balance"] > 0)
    total_give = sum(abs(data["balance"]) for data in st.session_state.customers.values() if data["balance"] < 0)
    net_val = total_get - total_give
    
    st.markdown(f"""
        <div class="net-balance-card">
            <span style="font-size: 14px; color: #566573; font-weight: bold;">{t['net_bal']}</span><br>
            <span style="font-size: 22px; font-weight: bold; color: {'#C0392B' if net_val > 0 else '#27AE60'};">₹ {net_val}</span>
            <span style="float: right; font-size: 14px; color: #566573; margin-top: 8px;">{t['you_get']}</span>
        </div>
    """, unsafe_allow_html=True)
    
    search_q = st.text_input("🔍", placeholder=t["search_ph"], label_visibility="collapsed")
    st.markdown("---")
    
    for name, data in st.session_state.customers.items():
        if search_q and search_q.lower() not in name.lower():
            continue
            
        bal = data["balance"]
        reg_date_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
        diff_days = (datetime.date.today() - reg_date_obj).days
        is_defaulter = diff_days > 365 and bal > 0
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"**👤 {name}**")
            if is_defaulter:
                st.markdown(f"<span style='background-color: #FADBD8; color: #922B21; padding: 2px 6px; border-radius: 4px; font-size: 11px;'>⚠️ DEFAULTER</span>", unsafe_allow_html=True)
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
        
    if "active_customer" in st.session_state and st.session_state.active_customer in st.session_state.customers:
        ac_name = st.session_state.active_customer
        ac_data = st.session_state.customers[ac_name]
        st.markdown("---")
        st.subheader(f"📁 {ac_name} - Statement")
        for dt, desc, amt in ac_data["transactions"]:
            st.text(f"📅 {dt} | {desc} : ₹ {amt}")

# 2. Add Customer Tab
elif app_tab == "Add Customer (খদ্দের যোগ)":
    st.subheader("➕ নতুন খদ্দের যুক্ত করুন")
    saved_contacts_list = ["রিয়া বস্ত্রালয়", "মণ্ডল ব্রাদার্স", "বিপ্লব মৈত্র", "সুবল দম্পতি", "পার্থ কসমেটিক্স"]
    
    with st.form("add_cust_form"):
        quick_select = st.selectbox("📞 কন্টাক্ট বা জিমেইল থেকে বাছুন (Quick Pick):", ["-- নিজে টাইপ করুন বা নতুন দিন --"] + saved_contacts_list)
        c_name = st.text_input("খদ্দেরের নাম (Customer Name)", value="" if quick_select == "-- নিজে টাইপ করুন বা নতুন দিন --" else quick_select)
        c_phone = st.text_input("WhatsApp নম্বর (Phone Number)")
        c_due = st.number_input("প্রারম্ভিক বাকি (Opening Due)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("খদ্দের সেভ করুন")
        
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
                st.success(f"সফলভাবে {c_name} যোগ করা হয়েছে!")

# 3. Voice & Item Billing Tab (Key Feature Requested)
elif app_tab == "Voice & Item Billing (ভয়েস ও মাল বাকি বিল)":
    st.subheader("🎙️ ভয়েস টাইপিং ও মাল বাকি বিল এন্ট্রি")
    st.info("💡 টিপস: লেখার বক্সে ট্যাপ করার পর কিবোর্ডের মাইক্রোফোন (Voice Typing) আইকনে ক্লিক করে মুখে বলে দিন (যেমন: 'দুটি জামদানি শাড়ি ও এক জোড়া প্যান্ট বাকি দিলাম ৩০০০ টাকা')। কিবোর্ড নিজে থেকেই লিখে নেবে!")
    
    if not st.session_state.customers:
        st.warning("প্রথমে খদ্দের যুক্ত করুন।")
    else:
        sel_cust = st.selectbox("খদ্দের নির্বাচন করুন", list(st.session_state.customers.keys()))
        
        with st.form("voice_item_form"):
            item_desc = st.text_area("🛒 কী মাল দেওয়া হলো তার বিবরণ (Voice Type বা টাইপ করুন):", placeholder="যেমন: ১টি সিল্ক শাড়ি, ২ কিমি কাপড় বাকি দেওয়া হলো...")
            bill_amount = st.number_input("বাকি টাকার পরিমাণ (₹)", min_value=1.0, step=10.0)
            submit_bill = st.form_submit_button("বিল ও বাকি নিশ্চিত করুন")
            
            if submit_bill:
                today_str = str(datetime.date.today())
                st.session_state.customers[sel_cust]["balance"] += bill_amount
                full_desc = f"মাল বাকি: {item_desc} (₹{bill_amount})"
                st.session_state.customers[sel_cust]["transactions"].append((today_str, full_desc, bill_amount))
                st.success(f"✅ {sel_cust}-এর অ্যাকাউন্টে সফলভাবে বিল ও ₹{bill_amount} বাকি যোগ করা হয়েছে!")

# 4. Auto-Reminders & Voice Note Tips
elif app_tab == "Auto-Reminders (অটো-মেসেজ ও ভয়েস)":
    st.subheader("🤖 WhatsApp ও ভয়েস মেসেজ রিমাইন্ডার")
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0:
            st.markdown(f"**👤 {name}** (বাকি: ₹ {data['balance']})")
            msg_text = f"নমস্কার {name}, নাসরিন বস্ত্রালয় থেকে জানানো যাচ্ছে যে আপনার মোট বাকি ₹ {data['balance']} টাকা। দয়া করে শীঘ্রই দোকানে এসে হিসাব পরিশোধ করুন।"
            ed_msg = st.text_area(f"মেসেজ ({name})", value=msg_text, key=f"auto_txt_{name}")
            
            ph = data["phone"]
            if ph:
                enc = urllib.parse.quote(ed_msg)
                wa_link = f"https://wa.me/{ph}?text={enc}"
                
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25D366; color:white; padding:8px 15px; border:none; border-radius:5px; width:100%; font-weight:bold;">📱 WhatsApp-এ বিল ও রিমাইন্ডার পাঠান</button></a>', unsafe_allow_html=True)
                st.caption("🎙️ টিপস: WhatsApp চ্যাটে গিয়ে আপনি সরাসরি ভয়েস নোট (Voice Note) রেকর্ড করেও মুখে রিমাইন্ডার পাঠিয়ে দিতে পারেন।")
            st.markdown("---")

# 5. PDF Bill Report Tab
elif app_tab == "PDF Bill Report (পিডিএফ বিল রিপোর্ট)":
    st.subheader("📄 পিডিএফ বিল ও স্টেটমেন্ট তৈরি")
    st.info("💡 এই পেজ থেকে খদ্দেরের সম্পূর্ণ বিলের তালিকা দেখে সরাসরি প্রিন্ট বা পিডিএফ সেভ করে নিতে পারবেন।")
    
    if st.session_state.customers:
        pdf_c = st.selectbox("গ্রাহক নির্বাচন করুন", list(st.session_state.customers.keys()), key="pdf_sel")
        c_dat = st.session_state.customers[pdf_c]
        
        if st.button("বিল রিপোর্ট প্রিভিউ দেখুন"):
            st.success(f"✅ {pdf_c}-এর অফিশিয়াল বিল প্রস্তুত!")
            st.markdown("---")
            st.markdown("### 🛍️ নাসরিন বস্ত্রালয়")
            st.caption("তেমাথা বাজার, বেলসর, পূর্ব বর্ধমান | ফোন: 91XXXXXXXXXX")
            st.markdown(f"**গ্রাহক:** {pdf_c} | **ফোন:** {c_dat['phone']}")
            st.markdown(f"**তারিখ:** {datetime.date.today()}")
            st.markdown("---")
            st.write("**লেনদেন ও মালের বিবরণী:**")
            for dt, ds, am in c_dat["transactions"]:
                st.text(f"• {dt} | {ds}")
            st.markdown("---")
            st.markdown(f"### **বর্তমান মোট পাওনা (Total Due): ₹ {c_dat['balance']}**")
            st.markdown("---")
            st.info("🖨️ **কীভাবে পিডিএফ করবেন:** মোবাইল ব্রাডজারের ওপরের বা নিচের ৩-ডট (...) মেনুতে ট্যাপ করে **'Print'** বা **'Share / Save as PDF'** সিলেক্ট করলেই এটি সরাসরি পিডিএফ ফাইল আকারে সেভ হয়ে যাবে এবং খদ্দেরকে পাঠাতে পারবেন।")

# 6. Defaulter List Tab
elif app_tab == "Defaulter List (ডিফল্টার লিস্ট)":
    st.subheader("⚠️ দীর্ঘমেয়াদী বকেয়া ও ডিফল্টার তালিকা (১ বছরের বেশি)")
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
                st.markdown(f'<a href="{d_wa}" target="_blank"><button style="background-color:#E74C3C; color:white; padding:6px 15px; border:none; border-radius:4px; font-weight:bold;">⚠️ Remind Defaulter via WhatsApp</button></a>', unsafe_allow_html=True)
                st.markdown("---")
    if not found_def:
        st.success("🎉 কোনো দীর্ঘমেয়াদী ডিফল্টার নেই!")
