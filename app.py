import streamlit as st
import datetime
import urllib.parse

st.set_page_config(
    page_title="Nasrin Bastralaya - Hisab Khata",
    page_icon="🌍",
    layout="centered"
)

# Custom Styling for OK Credit Floating Action Buttons & UI
st.markdown("""
    <style>
    .customer-card {
        background-color: #FFFFFF;
        padding: 10px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-bottom: 1px solid #E5E7E9;
    }
    .defaulter-badge {
        background-color: #FADBD8;
        color: #922B21;
        padding: 1px 5px;
        border-radius: 3px;
        font-size: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "customers" not in st.session_state:
    st.session_state.customers = {
        "প্রান্ত হাঁড়িয়াড়পাড়া": {
            "phone": "919876543210", 
            "balance": 400, 
            "reg_date": "2024-04-17", 
            "transactions": [("2024-04-17", "₹100 Payment Added", 100)]
        },
        "কালো মির্জা": {
            "phone": "919123456789", 
            "balance": 710, 
            "reg_date": "2024-04-17", 
            "transactions": [("2024-04-17", "₹100 Payment Added", 100)]
        },
        "দীপা": {
            "phone": "919333344445", 
            "balance": 700, 
            "reg_date": "2024-04-16", 
            "transactions": [("2024-04-16", "₹200 Payment Added", 200)]
        }
    }

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Ledger"

# Bottom Navigation Bar (Functional OK Credit Style)
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("📖 Ledger"):
        st.session_state.active_tab = "Ledger"
with nav_col2:
    if st.button("💰 Collection"):
        st.session_state.active_tab = "Collection"
with nav_col3:
    if st.button("⭐ My Plan"):
        st.session_state.active_tab = "My Plan"
with nav_col4:
    if st.button("⚙️ More"):
        st.session_state.active_tab = "More"

st.markdown("---")

# Main Logic based on Functional Navigation Tabs
if st.session_state.active_tab == "Ledger":
    st.subheader("🛍️ নাসরিন বস্ত্রালয় - খাতা")
    
    # Filter options
    f1, f2, f3 = st.columns(3)
    with f1:
        show_cust = st.button("👤 Customer")
    with f2:
        show_supp = st.button("📦 Supplier")
    with f3:
        show_due = st.button("⏳ Due Today")
        
    st.markdown("---")
    
    # Floating Action Buttons simulation right above the list for instant action
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        if st.button("💬 1-Click WhatsApp Vasooli"):
            st.session_state.active_tab = "AutoReminders"
            st.rerun()
    with act_col2:
        if st.button("➕ Add New Customer"):
            st.session_state.active_tab = "AddCustomer"
            st.rerun()
            
    st.markdown("---")
    
    # Customer List Display
    for name, data in st.session_state.customers.items():
        bal = data["balance"]
        ph = data["phone"]
        reg_date_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
        diff_days = (datetime.date.today() - reg_date_obj).days
        is_defaulter = diff_days > 365 and bal > 0
        
        col_a, col_b, col_c = st.columns([2.5, 1.5, 1])
        with col_a:
            st.markdown(f"**{name}**")
            if is_defaulter:
                st.markdown("<span class='defaulter-badge'>DEFAULTER</span>", unsafe_allow_html=True)
            else:
                st.caption(f"✓ Last update on {data['reg_date']}")
                
        with col_b:
            if bal > 0:
                st.markdown(f"<div style='text-align: right; color: #C0392B; font-weight: bold;'>₹{bal}<br><span style='font-size: 11px; color: #7F8C8D;'>Due</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: right; color: #27AE60; font-weight: bold;'>₹0<br><span style='font-size: 11px; color: #7F8C8D;'>Settled</span></div>", unsafe_allow_html=True)
                
        with col_c:
            if ph:
                wa_url = f"https://wa.me/{ph}?text=Namaskar%20{name},%20Nasrin%20Bastralaya%20due%20is%20Rs%20{bal}."
                st.markdown(f"<a href='{wa_url}' target='_blank'><button style='background-color:#25D366; color:white; border:none; border-radius:4px; padding:6px 10px; font-size:12px; font-weight:bold;'>💬 WA</button></a>", unsafe_allow_html=True)
                
        st.markdown("<hr style='margin: 4px 0px; opacity: 0.15;'>", unsafe_allow_html=True)

elif st.session_state.active_tab == "AddCustomer":
    st.subheader("➕ নতুন খদ্দের যুক্ত করুন")
    with st.form("add_form"):
        c_name = st.text_input("খদ্দেরের নাম (Customer Name)")
        c_phone = st.text_input("WhatsApp নম্বর (Phone Number)")
        c_due = st.number_input("প্রারম্ভিক বাকি (Opening Due)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("সেভ করুন")
        
        if submitted and c_name:
            if c_name in st.session_state.customers:
                st.warning("এই নামের খদ্দের ইতিমধ্যেই রয়েছে!")
            else:
                cur_date = str(datetime.date.today())
                st.session_state.customers[c_name] = {
                    "phone": c_phone,
                    "balance": c_due,
                    "reg_date": cur_date,
                    "transactions": [(cur_date, "Opening Due", c_due)] if c_due > 0 else []
                }
                st.success(f"{c_name} সফলভাবে যোগ করা হয়েছে!")
                st.session_state.active_tab = "Ledger"
                st.rerun()

elif st.session_state.active_tab == "AutoReminders":
    st.subheader("💬 WhatsApp রিমাইন্ডার সেন্টার")
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0:
            st.markdown(f"**{name}** (বাকি: ₹{data['balance']})")
            ph = data["phone"]
            if ph:
                wa_url = f"https://wa.me/{ph}?text=Namaskar%20{name},%20please%20clear%20due%20Rs%20{data['balance']}%20at%20Nasrin%20Bastralaya."
                st.markdown(f"<a href='{wa_url}' target='_blank'><button style='background-color:#25D366; color:white; padding:6px 12px; border:none; border-radius:4px; font-weight:bold;'>💬 WhatsApp Send</button></a>", unsafe_allow_html=True)
            st.markdown("---")
    if st.button("⬅️ Back to Ledger"):
        st.session_state.active_tab = "Ledger"
        st.rerun()

elif st.session_state.active_tab == "Collection":
    st.subheader("💰 Collection Summary")
    total_col = sum(d["balance"] for d in st.session_state.customers.values() if d["balance"] > 0)
    st.metric("Total Market Collections Due", f"₹ {total_col}")

elif st.session_state.active_tab == "My Plan":
    st.subheader("⭐ My Plan & Subscription")
    st.success("Your app is running smoothly on Cloud.")

elif st.session_state.active_tab == "More":
    st.subheader("⚙️ More Options & Settings")
    st.markdown("• **Bills & Reports Management**")
    st.markdown("• **Stock & Inventory Control**")
    st.markdown("• **Auto Reminder Settings**")
