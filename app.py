import streamlit as st
import datetime
import urllib.parse

# Page configuration with Earth Logo Favicon
st.set_page_config(
    page_title="Nasrin Bastralaya - Hisab Khata",
    page_icon="🌍",
    layout="centered"
)

# App Header
st.title("🛍️ নাসরিন বস্ত্রালয় - হিসাব খাতা")
st.caption("অটো-মেসেজ, WhatsApp ও সাধারণ SMS রিমাইন্ডার সিস্টেম")
st.markdown("---")

# Session State for data storage simulation
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

# Sidebar Menu for Navigation
menu = st.sidebar.selectbox("মেনু নির্বাচন করুন", [
    "📊 ড্যাশবোর্ড ও খাতা", 
    "➕ নতুন খদ্দের যোগ", 
    "💰 লেনদেন (টাকা জমা/বাকি)", 
    "🤖 প্রতিদিনের অটো-মেসেজ (Daily Auto-Reminder)", 
    "📄 পিডিএফ বিল ও রিপোর্ট",
    "⚠️ এক বছরের পুরনো ডিফল্টার লিস্ট"
])

# 1. Dashboard & Ledger
if menu == "📊 ড্যাশবোর্ড ও খাতা":
    st.subheader("📋 খদ্দেরের খাতা (OK/Khata Style)")
    
    if not st.session_state.customers:
        st.info("এখনো কোনো খদ্দেরের হিসাব যোগ করা হয়নি।")
    else:
        total_market = sum(data["balance"] for data in st.session_state.customers.values())
        st.metric(label="মোট পাওনা টাকা (Total Market Dues)", value=f"₹ {total_market}")
        st.markdown("---")
        
        for name, data in st.session_state.customers.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**👤 {name}**")
                st.caption(f"📱 ফোন: {data['phone']}")
            with col2:
                if data["balance"] > 0:
                    st.error(f"বাকি: ₹ {data['balance']}")
                else:
                    st.success("হিসাব পরিশোধ (0)")
            with col3:
                if st.button("ডিটেইলস", key=f"btn_{name}"):
                    st.session_state.selected_customer = name

        if "selected_customer" in st.session_state and st.session_state.selected_customer in st.session_state.customers:
            c_name = st.session_state.selected_customer
            c_data = st.session_state.customers[c_name]
            st.markdown("---")
            st.subheader(f"📁 {c_name}-এর লেনদেনের বিবরণী")
            for date, desc, amt in c_data["transactions"]:
                st.text(f"তারিখ: {date} | বিবরণ: {desc} | পরিমাণ: ₹ {amt}")

# 2. Add New Customer
elif menu == "➕ নতুন খদ্দের যোগ":
    st.subheader("নতুন খদ্দেরের নাম ও ফোন নম্বর এন্ট্রি করুন")
    with st.form("add_customer_form"):
        new_name = st.text_input("খদ্দেরের নাম")
        new_phone = st.text_input("ফোন নম্বর (যেমন: 919876543210)")
        initial_due = st.number_input("প্রারম্ভিক বাকি (যদি থাকে)", min_value=0.0, step=10.0)
        submit_btn = st.form_submit_button("সেভ করুন")
        
        if submit_btn and new_name:
            if new_name in st.session_state.customers:
                st.warning("এই নামের খদ্দের ইতিমধ্যেই তালিকায় আছে!")
            else:
                current_date = str(datetime.date.today())
                st.session_state.customers[new_name] = {
                    "phone": new_phone,
                    "balance": initial_due,
                    "reg_date": current_date,
                    "transactions": [(current_date, "প্রাথমিক বাকি", initial_due)] if initial_due > 0 else []
                }
                st.success(f"সফলভাবে {new_name}-এর হিসাব যোগ করা হয়েছে!")

# 3. Transaction Management
elif menu == "💰 লেনদেন (টাকা জমা/বাকি)":
    st.subheader("টাকা বাকি দেওয়া অথবা জমা নেওয়া")
    if not st.session_state.customers:
        st.warning("প্রথমে খদ্দের যুক্ত করুন।")
    else:
        selected_cust = st.selectbox("খদ্দের বাছুন", list(st.session_state.customers.keys()))
        trans_type = st.radio("লেনদেনের ধরন", ["মাল বাকি দেওয়া (টাকা পাবে)", "টাকা জমা নেওয়া (পরিশোধ)"])
        amount = st.number_input("টাকার পরিমাণ (₹)", min_value=1.0, step=10.0)
        note = st.text_input("বিবরণ (যেমন: শাড়ি কেনা, ক্যাশ পেমেন্ট ইত্যাদি)")
        
        if st.button("লেনদেন নিশ্চিত করুন"):
            current_date = str(datetime.date.today())
            if trans_type == "মাল বাকি দেওয়া (টাকা পাবে)":
                st.session_state.customers[selected_cust]["balance"] += amount
                st.session_state.customers[selected_cust]["transactions"].append((current_date, f"বাকি: {note}", amount))
                st.success(f"{selected_cust}-এর অ্যাকাউন্টে ₹ {amount} বাকি যোগ করা হয়েছে।")
            else:
                st.session_state.customers[selected_cust]["balance"] -= amount
                st.session_state.customers[selected_cust]["transactions"].append((current_date, f"জমা: {note}", -amount))
                st.success(f"{selected_cust}-এর কাছ থেকে ₹ {amount} জমা নেওয়া হয়েছে।")

# 4. Daily Auto-Message & Dual Options (WhatsApp + Normal SMS)
elif menu == "🤖 প্রতিদিনের অটো-মেসেজ (Daily Auto-Reminder)":
    st.subheader("🤖 প্রতিদিনের অটো-জেনারেটেড রিমাইন্ডার মেসেজ")
    st.caption("অ্যাপ খুললেই আজকের তারিখ অনুযায়ী সমস্ত বকেয়া খদ্দেরের জন্য অটো-মেসেজ তৈরি হয়ে যাবে। আপনি WhatsApp বা সাধারণ SMS-এর মাধ্যমে পাঠিয়ে দিতে পারবেন।")
    
    if not st.session_state.customers:
        st.info("কোনো খদ্দেরের ডেটা নেই।")
    else:
        today_date = datetime.date.today()
        st.info(f"📅 আজকের তারিখ: {today_date} | সিস্টেম অটো-মেসেজ স্ট্যাটাস: এক্টিভ ✅")
        
        for name, data in st.session_state.customers.items():
            if data["balance"] > 0:
                st.markdown(f"### 👤 খদ্দের: {name} (বাকি: ₹ {data['balance']})")
                
                # Auto Capsule Message Generation
                auto_msg = f"নমস্কার {name}, নাসরিন বস্ত্রালয় থেকে জানানো যাচ্ছে যে আপনার মোট বাকি ₹ {data['balance']} টাকা। দয়া করে শীঘ্রই দোকানে এসে হিসাব পরিশোধ করুন।"
                
                edited_msg = st.text_area(f"অটো মেসেজ খসড়া ({name})", value=auto_msg, key=f"msg_{name}")
                
                c_phone = data["phone"]
                if c_phone:
                    encoded_msg = urllib.parse.quote(edited_msg)
                    
                    # Links for WhatsApp and Normal SMS
                    wa_url = f"https://wa.me/{c_phone}?text={encoded_msg}"
                    sms_url = f"sms:{c_phone}?body={encoded_msg}"
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; padding:8px 15px; border:none; border-radius:5px; width:100%; cursor:pointer;">📱 WhatsApp পাঠান</button></a>', unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f'<a href="{sms_url}"><button style="background-color:#007bff; color:white; padding:8px 15px; border:none; border-radius:5px; width:100%; cursor:pointer;">✉️ সাধারণ SMS পাঠান</button></a>', unsafe_allow_html=True)
                else:
                    st.warning("এই খদ্দেরের কোনো ফোন নম্বর যুক্ত করা নেই।")
                st.markdown("---")

# 5. PDF Bill & Report
elif menu == "📄 পিডিএফ বিল ও রিপোর্ট":
    st.subheader("খদ্দেরের হিসাবের বিল ও বিবরণী")
    if not st.session_state.customers:
        st.info("কোনো খদ্দেরের ডেটা নেই।")
    else:
        pdf_cust = st.selectbox("রিপোর্ট বা বিলের জন্য খদ্দের বাছুন", list(st.session_state.customers.keys()))
        c_info = st.session_state.customers[pdf_cust]
        
        if st.button("বিল প্রিভিউ ও প্রিন্ট রিপোর্ট"):
            st.success(f"✅ {pdf_cust}-এর হিসাবের বিল প্রস্তুত!")
            st.write(f"**ব্যবসা:** নাসরিন বস্ত্রালয় (তেমাথা বাজার, বেলসর)")
            st.write(f"**গ্রাহক:** {pdf_cust}")
            st.write(f"**ফোন নম্বর:** {c_info['phone']}")
            st.write(f"**মোট বকেয়া:** ₹ {c_info['balance']}")
            st.write("---")
            st.write("লেনদেনের ইতিহাস:")
            for dt, desc, amt in c_info["transactions"]:
                st.text(f"• {dt} | {desc} : ₹ {amt}")
            st.info("💡 টিপস: আপনি মোবাইল ব্রাউজারের মেনু থেকে 'Print' বা 'Save as PDF' অপশন ব্যবহার করে সরাসরি পিডিএফ ফাইল তৈরি করে খদ্দেরকে পাঠাতে পারবেন।")

# 6. Defaulter List (1+ Year Old Dues)
elif menu == "⚠️ এক বছরের পুরনো ডিফল্টার লিস্ট":
    st.subheader("⚠️ দীর্ঘমেয়াদী বাকি বা ডিফল্টার খদ্দেরদের তালিকা (১ বছরের বেশি পুরনো)")
    
    today = datetime.date.today()
    defaulters_found = False
    
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0 and "reg_date" in data:
            reg_date_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
            diff_days = (today - reg_date_obj).days
            
            if diff_days > 365:
                defaulters_found = True
                st.error(f"👤 **{name}** | ফোন: {data['phone']} | বাকি: ₹ {data['balance']} | স্থায়িত্ব: {diff_days} দিন ধরে বকেয়া!")
                
                def_msg = f"জরুরি বার্তা: নমস্কার {name}, নাসরিন বস্ত্রালয়-এ আপনার দীর্ঘদিনের বকেয়া ₹ {data['balance']} টাকা অতিসত্বর পরিশোধ করার জন্য অনুরোধ করা হচ্ছে।"
                encoded_def_msg = urllib.parse.quote(def_msg)
                def_wa_url = f"https://wa.me/{data['phone']}?text={encoded_def_msg}"
                def_sms_url = f"sms:{data['phone']}?body={encoded_def_msg}"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<a href="{def_wa_url}" target="_blank"><button style="background-color:#d9534f; color:white; padding:5px 15px; border:none; border-radius:4px; width:100%; cursor:pointer;">⚠️ WhatsApp ডিফল্টার</button></a>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<a href="{def_sms_url}"><button style="background-color:#333; color:white; padding:5px 15px; border:none; border-radius:4px; width:100%; cursor:pointer;">✉️ SMS ডিফল্টার</button></a>', unsafe_allow_html=True)
                st.markdown("---")
                
    if not defaulters_found:
        st.success("🎉 চমৎকার! ১ বছরের বেশি পুরনো কোনো বকেয়া বা ডিফল্টার খদ্দের নেই।")
