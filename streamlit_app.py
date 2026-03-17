# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app.
st.title("🥤 Customize your Smoothie! 🥤")
st.write("Choose the fruits 🍌 🍓 🍍 🍎 🥭 🌰 you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on the smoothie will be: " + name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Query fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
fruit_options = [row.FRUIT_NAME for row in my_dataframe.collect()]

ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:", fruit_options, max_selections=5
)

# if ingredient_list:
#     ingredients_string = " ".join(ingredient_list)
#     st.write("You selected:", ingredient_list)
if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)
    ingrediants_string = ''    
    for fruit_chosen in ingredient_list:
        ingrediants_string+= fruit_chosen + ' '
        st.subheader(fruit_chosen+ ' Nutrition Information')
        # External API call (fixed URL string)
# try:
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
    st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# except requests.exceptions.RequestException as e:
#     st.error(f"API request failed: {e}")
    st.write("You selected:", ingredient_list)

    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """
    st.write(my_insert_stmt)

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!! ✅")

# External API call (fixed URL string)
# try:
#     smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#     st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
# except requests.exceptions.RequestException as e:
    # st.error(f"API request failed: {e}")
