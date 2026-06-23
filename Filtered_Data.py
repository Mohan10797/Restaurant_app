import streamlit as st
import pandas as pd
import pymysql

# ─── Connection ───────────────────────────────────────────────
def get_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="my_pro"
    )
    return conn

def get_data(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# Page Config 
st.title("🔍 Combined Filter - Restaurant & Orders")
st.markdown("---")

# Tabs 
tab1, tab2 = st.tabs([":hamburger: Restaurant Filter", "📦 Orders Filter"])


with tab1:
    st.subheader(":hamburger: Restaurant Data Filters")

    # Load unique values for dropdowns
    try:
        locations = get_data("SELECT DISTINCT location FROM MY_PRO WHERE location IS NOT NULL ORDER BY location;")
        location_list = ["All"] + locations["location"].tolist()
    except:
        location_list = ["All"]

    try:
        cuisines = get_data("SELECT DISTINCT cuisines FROM MY_PRO WHERE cuisines IS NOT NULL ORDER BY cuisines;")
        cuisine_list = ["All"] + cuisines["cuisines"].tolist()
    except:
        cuisine_list = ["All"]

    # Sidebar-style filters inside tab
    col1, col2 = st.columns(2)

    with col1:
        sel_location = st.selectbox("📍 Location", location_list, key="r_loc")
        sel_cuisine  = st.selectbox("🍜 Cuisine",  cuisine_list,  key="r_cui")
        sel_online   = st.selectbox("💻 Online Order", ["All", "Yes", "No"], key="r_online")

    with col2:
        sel_book     = st.selectbox("📅 Book Table", ["All", "Yes", "No"], key="r_book")
        sel_rating   = st.slider("⭐ Rating Range", 0.0, 5.0, (0.0, 5.0), step=0.5, key="r_rate")
        sel_cost     = st.slider("💰 Cost Range (₹)", 0, 6000, (0, 6000), step=100, key="r_cost")

    if st.button("🔍 Search Restaurants", key="btn_rest"):
        with st.spinner("Fetching restaurant data..."):

            # Build dynamic query
            conditions = []
            values = []

            if sel_location != "All":
                conditions.append("location = %s")
                values.append(sel_location)

            if sel_cuisine != "All":
                conditions.append("cuisines LIKE %s")
                values.append(f"%{sel_cuisine}%")

            if sel_online != "All":
                conditions.append("online_order = %s")
                values.append(sel_online)

            if sel_book != "All":
                conditions.append("book_table = %s")
                values.append(sel_book)

            conditions.append("CAST(rate AS DECIMAL(10,2)) BETWEEN %s AND %s")
            values.append(sel_rating[0])
            values.append(sel_rating[1])

            conditions.append("approx_cost BETWEEN %s AND %s")
            values.append(sel_cost[0])
            values.append(sel_cost[1])

            where_clause = " AND ".join(conditions)
            query = f"""
                SELECT name, location, cuisines, rate, approx_cost,
                       online_order, book_table
                FROM MY_PRO
                WHERE {where_clause}
                ORDER BY rate DESC
                LIMIT 100;
            """

            df = get_data(query, params=values)

            if df.empty:
                st.warning("⚠️ No restaurants found for selected filters.")
            else:
                st.success(f"✅ {len(df)} restaurants found!")
                st.markdown(df.to_html(index=False), unsafe_allow_html=True)


with tab2:
    st.subheader("📦 Orders Data Filters")

    # Load unique values for dropdowns
    try:
        payments = get_data("SELECT DISTINCT payment_method FROM orders_cleaned WHERE payment_method IS NOT NULL ORDER BY payment_method;")
        payment_list = ["All"] + payments["payment_method"].tolist()
    except:
        payment_list = ["All"]

    try:
        restaurants = get_data("SELECT DISTINCT restaurant_name FROM orders_cleaned WHERE restaurant_name IS NOT NULL ORDER BY restaurant_name;")
        restaurant_list = ["All"] + restaurants["restaurant_name"].tolist()
    except:
        restaurant_list = ["All"]

    # ── Filters ──
    col3, col4 = st.columns(2)

    with col3:
        sel_payment    = st.selectbox("💳 Payment Method",  payment_list,    key="o_pay")
        sel_restaurant = st.selectbox("🏠 Restaurant Name", restaurant_list, key="o_rest")

    with col4:
        sel_discount   = st.selectbox("🏷️ Discount Used", ["All", "Yes", "No"], key="o_disc")
        sel_order_val  = st.slider("💵 Order Value Range (₹)", 0, 5000, (0, 5000), step=100, key="o_val")

    if st.button("🔍 Search Orders", key="btn_orders"):
        with st.spinner("Fetching orders data..."):

            # Build dynamic query
            conditions = []
            values = []

            if sel_payment != "All":
                conditions.append("payment_method = %s")
                values.append(sel_payment)

            if sel_restaurant != "All":
                conditions.append("restaurant_name = %s")
                values.append(sel_restaurant)

            if sel_discount != "All":
                conditions.append("discount_used = %s")
                values.append(sel_discount)

            conditions.append("order_value BETWEEN %s AND %s")
            values.append(sel_order_val[0])
            values.append(sel_order_val[1])

            where_clause = " AND ".join(conditions)
            query = f"""
                SELECT order_id, restaurant_name, order_value,
                       payment_method, discount_used
                FROM orders_cleaned
                WHERE {where_clause}
                ORDER BY order_value DESC
                LIMIT 100;
            """

            df = get_data(query, params=values)

            if df.empty:
                st.warning("⚠️ No orders found for selected filters.")
            else:
                st.success(f"✅ {len(df)} orders found!")
                st.markdown(df.to_html(index=False), unsafe_allow_html=True)