import streamlit as st
import pandas as pd
import pymysql

def get_connecion():
    conn=pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="my_pro"
    )
    return conn

def get_data(query):
    conn=get_connecion()
    df=pd.read_sql(query,conn)
    conn.close()
    return df
st.title(":hamburger: Restaurant Orders")
queries = {"1 .Total Revenue in Orders":"SELECT SUM(order_value)AS total_revenue FROM orders_cleaned;",
           "2 .High Orders":"SELECT restaurant_name,COUNT(*) AS total_orders FROM orders_cleaned GROUP BY restaurant_name ORDER BY total_orders DESC LIMIT 5;",
           "3 .Payment Methsod Wise Orders":"SELECT payment_method,COUNT(*) AS total_orders FROM orders_cleaned GROUP BY payment_method ORDER BY total_orders DESC LIMIT 5;",
           "4 .Orders Price More then 1000":"SELECT order_id,restaurant_name,order_value FROM orders_cleaned WHERE order_value >1000 ORDER BY order_value DESC LIMIT 5;",
           "5 .Avg Discounts Of Orders":"SELECT discount_used,AVG(order_value)AS average_spend FROM orders_cleaned GROUP BY discount_used;"}

selected_query=st.selectbox("select a query:",list(queries.keys()))
if st.button("Run Query"):
    with st.spinner("fetching data..."):
        df=get_data(queries[selected_query])
        st.success("Query executed successfully!")
        st.markdown(df.to_html(index=False),unsafe_allow_html=True)