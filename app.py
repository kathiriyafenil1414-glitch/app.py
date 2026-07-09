import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meesho Business Manager", layout="wide")

st.title("📈 Meesho Business Manager Pro")

if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=['Date', 'Order ID', 'Product', 'Selling Price', 'Cost', 'Status', 'Profit/Loss'])

st.sidebar.header("Add New Order")
with st.sidebar.form("order_form"):
    date = st.date_input("Date")
    oid = st.text_input("Order ID")
    prod = st.selectbox("Select Product", ["TT 500ML", "Kurti", "Dicer", "Other"])
    sell_price = st.number_input("Selling Price (Received Amount)", min_value=0.0)
    cost = st.number_input("Cost (Product + Packing)", min_value=0.0)
    status = st.selectbox("Status", ["Delivered", "Cancelled", "RTO"])
    
    submitted = st.form_submit_button("Save Order")
    if submitted:
        pl = sell_price - cost
        new_order = {'Date': date, 'Order ID': oid, 'Product': prod, 'Selling Price': sell_price, 'Cost': cost, 'Status': status, 'Profit/Loss': pl}
        st.session_state.orders = pd.concat([st.session_state.orders, pd.DataFrame([new_order])], ignore_index=True)
        st.success("Order saved successfully!")

st.subheader("Business Overview")
if not st.session_state.orders.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", len(st.session_state.orders))
    col2.metric("Total Profit/Loss", f"₹{st.session_state.orders['Profit/Loss'].sum():.2f}")
    col3.metric("Successful Deliveries", len(st.session_state.orders[st.session_state.orders['Status']=='Delivered']))
    
    st.dataframe(st.session_state.orders, use_container_width=True)
else:
    st.info("No orders yet. Add your first order from the sidebar.")
