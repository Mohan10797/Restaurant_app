import streamlit as st
import pandas as pd
df=pd.read_csv("new_cleaned_data.csv")
st.title(":hamburger: Uber Eats Restaurant")
queries = {
    "1 .Which Bangalore locations have the highest average restaurant ratings": "SELECT location,AVG(CAST(rate AS DECIMAL(10,2)))as avg_rating FROM MY_PRO GROUP BY location ORDER BY avg_rating DESC LIMIT 10;",
    "2 .Which locations are over-saturated with restaurants": "SELECT location,COUNT(*)as restaurant_count FROM MY_PRO GROUP BY location ORDER BY restaurant_count DESC LIMIT 10;",
    "3 .Does online ordering improve restaurant ratings": "SELECT online_order,AVG(rate) as average_rating FROM MY_PRO GROUP BY online_order;",
    "4 .Table booking correlate with higher customer ratings": "SELECT book_table,AVG(rate) as average_rating FROM MY_PRO GROUP BY book_table;",
    "5 .What price range delivers the best customer satisfaction": "SELECT approx_cost as cost,AVG(rate) as avg_rating FROM MY_PRO GROUP BY cost ORDER BY avg_rating DESC LIMIT 10;",
    "6 .Low mid and premium priced restaurants performance": "SELECT CASE WHEN approx_cost<=500 THEN 'Low' WHEN approx_cost<=1000 THEN 'Mid' ELSE 'Premium' END as price_range,AVG(rate) as avg_rating FROM MY_PRO GROUP BY price_range;",
    "7 .Most common Cuisines in Bangalore": "SELECT cuisines,COUNT(*)AS restaurant_count FROM MY_PRO GROUP BY cuisines ORDER BY restaurant_count DESC LIMIT 10;",
    "8 .Which cuisines receive the highest average ratings": "SELECT cuisines, AVG(rate) AS avg_rating, COUNT(*) AS count FROM MY_PRO GROUP BY cuisines HAVING count>10 ORDER BY avg_rating DESC LIMIT 10;",
    "9 .What is the relationship between restaurant cost and rating": "SELECT approx_cost,AVG(rate)AS avg_rating,COUNT(*) AS total_restaurants FROM MY_PRO GROUP BY approx_cost ORDER BY approx_cost;",
    "10 .Which locations are ideal for premium restaurant onboarding":"SELECT location, AVG(rate) as avg_rating, AVG(approx_cost) as avg_cost FROM MY_PRO WHERE approx_cost > (SELECT AVG(approx_cost) FROM MY_PRO) GROUP BY location ORDER BY avg_rating DESC, avg_cost DESC LIMIT 10;" 
}
selected_query=st.selectbox("select a query:",list(queries.keys()))
if st.button("Run Query"):
    with st.spinner("fetching data..."):
        conn=st.connection("pandas_sql",type="sql")
        df=conn.query(queries[selected_query])
        st.success("Query executed successfully!")
        st.markdown(df.to_html(index=False),unsafe_allow_html=True)
