import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
result = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[result]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  streamlit.write('The user entered ', fruit_choice)

  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  streamlit.dataframe(fruityvice_normalized)
except URLError:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.text(f'Thanks for adding {add_my_fruit}')

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
