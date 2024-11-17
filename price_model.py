import streamlit as st
import pandas as pd     


df = pd.read_csv("test_data.csv")
# df = df.drop(columns="Unnamed: 0").reset_index(drop=True)
print(pd.DataFrame(df))
# print(df[df.duplicated()])
# print(df.duplicated().sum()) 
# def searchCOnfig():
    
    
    
#     data = pd.read_csv("C:/Users/XPS 15/OneDrive/Documents/carbin africa/carbin_webscraping/datasets/3300ccCars.csv")
#     st.title("Vehicle Price Prediction")
    
#     st.write()
    
#     carBrand = st.selectbox("Brand", set(data["Brand"].tolist()))
#     carModel = st.selectbox("Model", set(data["Model"].tolist()))
#     condition = st.selectbox("Condition", set(data["Condition"].tolist()))
#     year = st.selectbox("Year",set(data["Year"].tolist()))
#     transmission = st.selectbox("Transmission",set(data["Transmission"].tolist()))
#     Color = st.selectbox("COlor", set(data["Colour"].tolist()))
#     Mileage = st.number_input("Mileage")
    
#     st.button("Predict")
#     # FuelType = st.selectbox("Fuel Type", set(data["Fuel Type"].tolist()))
    
# print(searchCOnfig())