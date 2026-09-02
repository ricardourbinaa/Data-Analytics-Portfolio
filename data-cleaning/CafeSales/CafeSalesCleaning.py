import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/ricar/OneDrive/Desktop/DataCleaningProject/dirty_cafe_sales.csv')

#Fixing Headers

df.columns = (
    df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
)

#Finding and Dropping Unknowns

unknown_tokens = ["ERROR", "Unknown", "UNKNOWN", "UNK", "?", "", " "]
df = df.replace(unknown_tokens, pd.NA)

#Fixing numerics

numeric_tokens = ['quantity', 'price_per_unit', 'total_spent']
df[numeric_tokens] = df[numeric_tokens].apply(pd.to_numeric, errors='coerce')

df['total_spent'] = df['quantity'] * df["price_per_unit"]

#Fixing Dates

df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

#Handle missing values

df["item"] = df["item"].fillna("Missing Item")
df["payment_method"] = df["payment_method"].fillna("Unknown Payment")
df["location"] = df["location"].fillna("Unknown Location")

df["quantity"] = df["quantity"].fillna(df["quantity"].median())
df["price_per_unit"] = df["price_per_unit"].fillna(df["price_per_unit"].median())
df["total_spent"] = df["quantity"] * df["price_per_unit"]

#Removing rows beyond repair 

df = df.dropna(subset=["quantity", "price_per_unit"])

#Saving Cleaned Dataset

df.to_csv("C:/Users/ricar/OneDrive/Desktop/DataCleaningProject/cleaned_cafe_sales.csv", index=False)


#--------------------------------------------------------------------------------------
# Analysis Layer
# Revenue, Best selling items, highest revenue items, perfered payment, when is the most money made?, in store vs takeout 

total_revenue = df['total_spent'].sum()
print("Total Revenue:", total_revenue)

best_selling_items = (
    df.groupby("item")["quantity"]
    .sum()
    .sort_values(ascending=False)
)

print(best_selling_items)

revenue_by_item = (
    df.groupby('item')['total_spent']
    .sum()
    .sort_values(ascending=False)
)
print(revenue_by_item)

payment_breakdown = df['payment_method'].value_counts()
print(payment_breakdown)

location_revenue = (
    df.groupby('location')['total_spent']
    .sum()
)
print(location_revenue)

df['month'] = df['transaction_date'].dt.to_period("M")
monthly_revenue = (
    df.groupby("month")['total_spent']
    .sum()
    .sort_index()
)
print(monthly_revenue)