# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

#Loading the fruit options from the table
cnx = st.connection("snowflake")
session = cnx.session()
my_df = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data = my_df, use_container_width = True)
#st.stop()

#Converting snowpark dataframe to pandas dataframe to use the loc function
pd_df = my_df.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#creating a text box for the name
name = st.text_input("Name on Smoothie:", placeholder = "John Doe")
st.write("The name on the smoothie will be: ", name)


#Creating a multi select box
ingredients_list = st.multiselect("Choose upto 5 ingredients: ", options = my_df, max_selections=5, )

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]  
        #st.write('The search value for ', fruit,' is ', search_on, '.')
      
        #Printing fruit nutrition information
        st.subheader(fruit + " nutrition information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        #st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width = True)


    st.write(ingredients_string)

    insert = """insert into orders(ingredients, name_on_order) values('"""+ingredients_string+"""', '"""+name+"""')"""
    st.write(insert)
    
    button = st.button("Submit Order")
    
    if button:
        session.sql(insert).collect()
        st.success("Your Smoothie is ordered, "+name+"!", icon = "✅")
