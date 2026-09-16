import streamlit as st
import datetime
import urllib.parse

st.set_page_config(
    page_title="Nasrin Bastralaya - Hisab Khata",
    page_icon="🌍",
    layout="centered"
)

LANGS = {
    "Bengali": {
        "title": "Nasrin Bastralaya - Hisab Khata",
        "caption": "Smart Ledger & WhatsApp Integration",
        "net_bal": "Net Balance",
        "search_ph": "Search customer name...",
        "add_cust": "Add New Customer"
    },
    "English": {
        "title": "Nasrin Bastralaya - Hisab Khata",
        "caption": "Smart Ledger & WhatsApp Integration",
        "net_bal": "Net Balance",
        "search_ph": "Search customer name...",
        "add_cust": "Add New Customer"
    }
}

selected_lang = st.sidebar.selectbox("Language / ভাষা", list(LANGS.keys()))
t = LANGS[selected_lang]

st.markdown("### 🛍️ " + t["title"])
st.caption(t["caption"])
st.markdown("---")

if "customers" not in st.session_state:
    st.session_state.customers = {
        "Rahim Sk": {
            "phone": "919876543210", 
            "balance": 4500, 
            "reg_date": "2024-01-10", 
            "transactions": [("2024-01-10", "Saree Due - Rs 4500", 4500)]
        },
        "Karim Mondal": {
            "phone": "919123456789", 
            "balance": 1200, 
            "reg_date": "2026-06-05", 
            "transactions": [("2026-06-05", "Pant & Shirt Due - Rs 1200", 1200)]
        }
    }

app_tab = st.sidebar.radio("Menu", [
    "Ledger", 
    "Add Customer", 
    "Voice & Item Billing", 
    "Auto-Reminders", 
    "PDF Bill Report", 
    "Defaulter List"
])

if app_tab == "Ledger":
    total_get = sum(data["balance"] for data in st.session_state.customers.values() if data["balance"] > 0)
    total_give = sum(abs(data["balance"]) for data in st.session_state.customers.values() if data["balance"] < 0)
    net_val = total_get - total_give
    
    st.write("Net Balance: Rs " + str(net_val))
    
    search_q = st.text_input("Search", placeholder=t["search_ph"], label_visibility="collapsed")
    st.markdown("---")
    
    for name, data in st.session_state.customers.items():
        if search_q and search_q.lower() not in name.lower():
            continue
            
        bal = data["balance"]
        ph = data["phone"]
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown("**👤 " + name + "**")
            if ph:
                wa_quick_url = "https://wa.me/" + ph + "?text=Namaskar%20" + name + ",%20Nasrin%20Bastralaya%20hisab."
                st.markdown("📱 [WhatsApp Link] (" + wa_quick_url + ")")
            else:
                st.caption("No phone number")
                
        with col2:
            if bal > 0:
                st.markdown("Due: Rs " + str(bal))
            elif bal < 0:
                st.markdown("Advance: Rs " + str(abs(bal)))
            else:
                st.markdown("Settled: Rs 0")
                
        with col3:
            if st.button("Details", key="btn_" + name):
                st.session_state.active_customer = name
                
        st.markdown("---")
        
    if "active_customer" in st.session_state and st.session_state.active_customer in st.session_state.customers:
        ac_name = st.session_state.active_customer
        ac_data = st.session_state.customers[ac_name]
        st.markdown("---")
        st.subheader("Statement: " + ac_name)
        for dt, desc, amt in ac_data["transactions"]:
            st.text(dt + " | " + desc + " : Rs " + str(amt))

elif app_tab == "Add Customer":
    st.subheader("Add New Customer")
    saved_contacts_list = ["Riya Bastralaya", "Mondal Brothers", "Biplab Maitra", "Subol Couple", "Partha Cosmetics"]
    
    with st.form("add_cust_form"):
        quick_select = st.selectbox("Select from Quick Contacts:", ["-- Type manually --"] + saved_contacts_list)
        c_name = st.text_input("Customer Name", value="" if quick_select == "-- Type manually --" else quick_select)
        c_phone = st.text_input("WhatsApp Phone Number (e.g., 919876543210)")
        c_due = st.number_input("Opening Due (Rs)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("Save Customer")
        
        if submitted and c_name:
            if c_name in st.session_state.customers:
                st.warning("Customer already exists!")
            else:
                cur_date = str(datetime.date.today())
                st.session_state.customers[c_name] = {
                    "phone": c_phone,
                    "balance": c_due,
                    "reg_date": cur_date,
                    "transactions": [(cur_date, "Opening Balance", c_due)] if c_due > 0 else []
                }
                st.success("Successfully added " + c_name + "!")

elif app_tab == "Voice & Item Billing":
    st.subheader("Voice Typing & Item Billing")
    st.info("Tip: Tap the text box and use your keyboard microphone icon for voice typing.")
    
    if not st.session_state.customers:
        st.warning("Please add a customer first.")
    else:
        sel_cust = st.selectbox("Select Customer", list(st.session_state.customers.keys()))
        
        with st.form("voice_item_form"):
            item_desc = st.text_area("Item Description:", placeholder="e.g., 1 Silk Saree, 2 meters cloth...")
            bill_amount = st.number_input("Due Amount (Rs)", min_value=1.0, step=10.0)
            submit_bill = st.form_submit_button("Confirm Bill & Due")
            
            if submit_bill:
                today_str = str(datetime.date.today())
                st.session_state.customers[sel_cust]["balance"] += bill_amount
                full_desc = "Items: " + item_desc + " (Rs " + str(bill_amount) + ")"
                st.session_state.customers[sel_cust]["transactions"].append((today_str, full_desc, bill_amount))
                st.success("Successfully added due!")

elif app_tab == "Auto-Reminders":
    st.subheader("WhatsApp & Voice Reminders")
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0:
            st.markdown("**👤 " + name + "** (Due: Rs " + str(data["balance"]) + ")")
            msg_text = "Namaskar " + name + ", total due amount at Nasrin Bastralaya is Rs " + str(data["balance"]) + ". Please clear your account soon."
            ed_msg = st.text_area("Message (" + name + ")", value=msg_text, key="auto_txt_" + name)
            
            ph = data["phone"]
            if ph:
                enc = urllib.parse.quote(ed_msg)
                wa_link = "https://wa.me/" + ph + "?text=" + enc
                st.markdown("[Send WhatsApp Reminder] (" + wa_link + ")")
            st.markdown("---")

elif app_tab == "PDF Bill Report":
    st.subheader("PDF Bill & Statement Generation")
    if st.session_state.customers:
        pdf_c = st.selectbox("Select Customer", list(st.session_state.customers.keys()), key="pdf_sel")
        c_dat = st.session_state.customers[pdf_c]
        
        if st.button("Generate Bill Preview"):
            st.success("Official bill ready for " + pdf_c + "!")
            st.markdown("---")
            st.markdown("### Nasrin Bastralaya")
            st.caption("Tematha Bazar, Belshor, Purba Bardhaman")
            st.markdown("Customer: " + pdf_c + " | Phone: " + c_dat["phone"])
            st.markdown("Date: " + str(datetime.date.today()))
            st.markdown("---")
            st.write("Transaction History:")
            for dt, ds, am in c_dat["transactions"]:
                st.text("- " + dt + " | " + ds)
            st.markdown("---")
            st.markdown("### Total Due: Rs " + str(c_dat["balance"]))

elif app_tab == "Defaulter List":
    st.subheader("Long-term Defaulter List (1+ Year)")
    today_dt = datetime.date.today()
    found_def = False
    
    for name, data in st.session_state.customers.items():
        if data["balance"] > 0 and "reg_date" in data:
            r_obj = datetime.datetime.strptime(data["reg_date"], "%Y-%m-%d").date()
            d_diff = (today_dt - r_obj).days
            if d_diff > 365:
                found_def = True
                st.error("👤 " + name + " | Due: Rs " + str(data["balance"]))
                d_msg = "Urgent: Please clear your long pending due at Nasrin Bastralaya."
                d_enc = urllib.parse.quote(d_msg)
                d_wa = "https://wa.me/" + data["phone"] + "?text=" + d_enc
                st.markdown("[Remind Defaulter via WhatsApp] (" + d_wa + ")")
                st.markdown("---")
    if not found_def:
        st.success("No long-term defaulters found!")
