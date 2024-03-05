import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

customers_df=pd.read_csv("customers.csv")
payments_reviews_df=pd.read_csv("payments_reviews.csv")

datetime_columns = ["review_creation_date"]
payments_reviews_df.sort_values(by="review_creation_date", inplace=True)
payments_reviews_df.reset_index(inplace=True)
 
for column in datetime_columns:
    payments_reviews_df[column] = pd.to_datetime(payments_reviews_df[column])

min_date = payments_reviews_df["review_creation_date"].min()
max_date = payments_reviews_df["review_creation_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = payments_reviews_df[(payments_reviews_df["review_creation_date"] >= str(start_date)) & 
                (payments_reviews_df["review_creation_date"] <= str(end_date))]

st.header('E-Commerce Public Report :sparkles:')

st.subheader('Number of Reviews per Month')
monthly_orders_df = main_df.resample(rule='M', on='review_creation_date').agg({
    "order_id": "nunique",
    "payment_value": "sum"
})
monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
monthly_orders_df = monthly_orders_df.reset_index()
monthly_orders_df.rename(columns={
    "order_id": "order_count",
    "payment_value": "revenue"
}, inplace=True)

#Numbers of Reviews per Month
plt.figure(figsize=(10, 5)) 
plt.plot(monthly_orders_df["review_creation_date"], monthly_orders_df["order_count"], marker='o', linewidth=2, color="#72BCD4") 
plt.title("Number of Reviews per Month", loc="center", fontsize=20) 
plt.xticks(fontsize=10) 
plt.yticks(fontsize=10) 
plt.xlabel("Date", fontsize=12)
plt.ylabel("Number of Reviews", fontsize=12)

st.pyplot(plt.gcf())

st.subheader('Total Revenue per Month')
#Total revenue per month
plt.figure(figsize=(10, 5)) 
plt.plot(monthly_orders_df["review_creation_date"], monthly_orders_df["revenue"], marker='o', linewidth=2, color="#72BCD4") 
plt.title("Total Revenue per Month", loc="center", fontsize=20) 
plt.xticks(fontsize=10) 
plt.yticks(fontsize=10) 
plt.xlabel("Date", fontsize=12)
plt.ylabel("Total Revenue", fontsize=12)

st.pyplot(plt.gcf())

#Jumlah pelanggan berdasarkan states
st.subheader('Number of Customer by States')
bystate_df = customers_df.groupby(by="customer_state").customer_id.nunique().reset_index()
bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
plt.figure(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_
)
plt.title("Number of Customer by States", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='y', labelsize=12)
st.pyplot(plt.gcf())

#Persentase tipe pembayaran
st.subheader('Percentage of Payment Types')
payment_type_counts = main_df['payment_type'].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(payment_type_counts, labels=payment_type_counts.index, autopct='%1.1f%%', startangle=140)
ax.set_title('Percentage of Payment Types')
ax.axis('equal') 

st.pyplot(fig)

st.subheader('Number of Reviews by Review Score')
#Jumlah review
review_counts = main_df['review_score'].value_counts().sort_index()
review_scores = review_counts.index

fig = plt.figure(figsize=(10, 6))
plt.bar(review_scores, review_counts, color='skyblue')

plt.xlabel('Review Score')
plt.ylabel('Number of Reviews')
plt.title('Number of Reviews by Review Score')

st.pyplot(fig)
