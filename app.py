import streamlit as st
import datetime
import urllib.parse
from PIL import Image

# 1. Page Configuration & Custom HTML Favicon for Earth Logo
st.set_page_config(
    page_title="Nasrin Bastralaya - Hisab Khata",
    page_icon="🌍",
    layout="centered"
)

# Forcefully injecting Earth Logo into browser tab and PWA app icon head
st.markdown("""
    <head>
        <link rel="icon" href="https://emojicdn.elk.sh/🌍">
    </head>
    <style>
    .net-balance-box {
        background-color: #F4F6F7;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #D5D8DC;
        margin-bottom: 15px;
    }
    .badge-def {
        background-color: #FADBD8;
        color: #922B21;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
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
            "balance": 1200, 
            "reg_date": "2026-06-05", 
            "transactions": [("2026-06-05", "প্যান্ট ও শার্ট", 1200)]
        }
    }

if "active_view" not in st.session_state:
    st.session_state.active_view = "Ledger"

if "shop_dp" not in st.session_state:
    st.session_state.shop_dp = None

# --- OK Credit Style Header with Earth Logo & Owner DP ---
header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.markdown("### 🌍 নাসরিন বস্ত্রালয় - হিসাব খাতা")
    st.caption("OK Credit Style Digital Ledger")
with header_col2:
    if st.session_state.shop_dp is not None:
        st.image(st.session_state.shop_dp, width=45, caption="Owner")
    else:
        st.markdown("👤 **DP**")

# --- OK Credit Style Navigation Tabs ---
nav1, nav2, nav3, nav4 = st.columns(4)
with nav1:
    if st.button("📖 Ledger", use_container_width=True):
        st.session_state.active_view = "Ledger"
with nav2:
    if st.button("➕ Add", use_container_width=True):
        st.session_state.active_view = "Add"
with nav3:
    if st.button("💬 WhatsApp", use_container_width=True):
        st.session_state.active_view = "WhatsApp"
with nav4:
    if st.button("⚙️ More", use_container_width=True):
        st.session_state.active_view = "More"

st.markdown("---")

# 1. LEDGER VIEW
if st.session_state.active_view == "Ledger":
    total_due = sum(d["balance"] for d in st.session_state.customers.values() if d["balance"] > 0)
    total_adv = sum(abs(d["balance"]) for d in st.session_state.customers.values() if d["balance"] < 0)
    net_bal = total_due - total_adv
    
    st.markdown(f"""
        <div class="net-balance-box">
            <span style="font-size: 13px; color: #566573; font-weight: bold;">Net Balance (মোট হিসাব)</span><br>
            <span style="font-size: 24px; font-weight: bold; color: {'#C0392B' if net_bal > 0 else '#27AE60'};">₹ {net_bal}</span>
            <span style="float: right; font-size: 13px; color: #7F8C8D; margin-top: 10px;">You'll Get (পাবেন)</span>
        </div>
    """, unsafe_allow_html=True)
    
    search_txt = st.text_input("🔍", placeholder="খদ্দেরের নাম দিয়ে খুঁজুন...", label_visibility="collapsed")
    st.markdown("---")
    
    for name, data in st.session_state.customers.items():
        if search_txt and search_txt.lower() not in name.lower():
            continue
            
        bal = data["balance"]
        ph = data["phone"]
        reg_d = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
        is_def = (datetime.date.today() - reg_d).days > 365 and bal > 0
        
        col_c1, col_c2, col_c3 = st.columns([2.2, 1.3, 1])
        with col_c1:
            st.markdown(f"**👤 {name}**")
            if is_def:
                st.markdown("<span class='badge-def'>DEFAULTER (1+ Yr)</span>", unsafe_allow_html=True)
            else:
                st.caption(f"📱 {ph}")
                
        with col_c2:
            if bal > 0:
                st.markdown(f"<div style='text-align: right; color: #C0392B; font-weight: bold;'>₹ {bal}<br><span style='font-size: 10px; color: #7F8C8D;'>Due</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: right; color: #27AE60; font-weight: bold;'>₹ 0<br><span style='font-size: 10px; color: #7F8C8D;'>Settled</span></div>", unsafe_allow_html=True)
                
        with col_c3:
            if ph:
                wa_url = f"https://wa.me/{ph}?text=Namaskar%20{name},%20Nasrin%20Bastralaya%20due%20is%20Rs%20{bal}."
                st.markdown(f"<a href='{wa_url}' target='_blank'><button style='background-color:#25D366; color:white; border:none; border-radius:4px; padding:5px 10px; font-size:12px; font-weight:bold;'>💬 WA</button></a>", unsafe_allow_html=True)
                
        st.markdown("<hr style='margin: 4px 0px; opacity: 0.15;'>", unsafe_allow_html=True)

# 2. ADD CUSTOMER VIEW
elif st.session_state.active_view == "Add":
    st.subheader("➕ নতুন খদ্দের যোগ করুন")
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
                st.session_state.active_view = "Ledger"
                st.rerun()

# 3. WHATSAPP REMINDER VIEW
elif st.session_state.active_view == "WhatsApp":
    st.subheader("💬 WhatsApp রিমাইন্ডার সেন্টার")
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0:
            st.markdown(f"**👤 {name}** (বাকি: ₹ {data['balance']})")
            ph = data["phone"]
            if ph:
                msg = f"নমস্কার {name}, নাসরিন বস্ত্রালয় থেকে আপনার মোট বাকি ₹ {data['balance']} টাকা পরিশোধ করার জন্য অনুরোধ করা হচ্ছে।"
                enc_msg = urllib.parse.quote(msg)
                wa_link = f"https://wa.me/{ph}?text={enc_msg}"
                st.markdown(f"<a href='{wa_link}' target='_blank'><button style='background-color:#25D366; color:white; padding:6px 15px; border:none; border-radius:5px; font-weight:bold;'>📱 WhatsApp-এ রিমাইন্ডার পাঠান</button></a>", unsafe_allow_html=True)
            st.markdown("---")
    if st.button("⬅️ খাতা বা ড্যাশবোর্ডে ফিরে যান"):
        st.session_state.active_view = "Ledger"
        st.rerun()

# 4. MORE / SETTINGS & DP UPLOAD VIEW
elif st.session_state.active_view == "More":
    st.subheader("⚙️ প্রোফাইল ও সেটিংস (Profile & DP Upload)")
    
    st.markdown("### 📷 আপনার নিজস্ব ডিপি (DP) বা দোকানের ছবি আপলোড করুন")
    uploaded_file = st.file_uploader("ছবি চয়ন করুন (Choose Image)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state.shop_dp = image
        st.success("✅ আপনার ডিপি সফলভাবে সেট করা হয়েছে! ওপরের কোণায় দেখতে পাবেন।")
        st.image(image, width=120, caption="Uploaded DP Preview")
        
    st.markdown("---")
    st.markdown("• **PDF Bill & Statement Generation**")
    st.markdown("• **1+ Year Defaulter Bill List**")
    st.markdown("• **Voice Typing & Item Billing**")
    
    if st.button("⬅️ খাতা বা ড্যাশবোর্ডে ফিরে যান"):
        st.session_state.active_view = "Ledger"
        st.rerun()
