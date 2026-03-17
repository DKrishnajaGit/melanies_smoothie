import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# Title and intro
st.title("🥤 Customize your Smoothie! 🥤")
st.write("Choose the fruits 🍌 🍓 🍍 🍎 🥭 🌰 you want in your custom smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie")
if name_on_order:
    st.write("The name on the smoothie will be: " + name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Query fruit options including SEARCH_ON
snow_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

# Convert to Pandas for easier lookup
pd_df = snow_df.to_pandas()

# Ingredient selection (GUI shows FRUIT_NAME)
ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:", pd_df["FRUIT_NAME"].tolist(), max_selections=5
)

# Display selection and show SEARCH_ON values
if ingredient_list:
    ingredients_string = " ".join(ingredient_list)
    st.write("You selected:", ingredient_list)

    for fruit_chosen in ingredient_list:
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"].iloc[0]
        st.write("The search value for", fruit_chosen, "is", search_on, ".")

    # Prepare insert statement
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)

    # Submit order
    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!! ✅")
