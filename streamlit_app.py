# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

#Loading the fruit options from the table
session = get_active_session()
my_df = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME'))

#creating a text box for the name
name = st.text_input("Name on Smoothie:", placeholder = "John Doe")
st.write("The name on the smoothie will be: ", name)


#Creating a multi select box
ingredients_list = st.multiselect("Choose upto 5 ingredients: ", options = my_df, max_selections=5, )

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

    st.write(ingredients_string)

    insert = """insert into orders(ingredients, name_on_order) values('"""+ingredients_string+"""', '"""+name+"""')"""
    st.write(insert)
    
    button = st.button("Submit Order")
    
    if button:
        session.sql(insert).collect()
        st.success("Your Smoothie is ordered, "+name+"!", icon = "✅")