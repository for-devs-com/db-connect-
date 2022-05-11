import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, inspect
from streamlit.errors import Error

### Dashboard Config ###
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
    page_title="DB-ADMIN"
)
st.container()
col1, col2 = st.columns([2, 2])

### Your Conection variables  ###
host = "localhost"
port = 
database = ""
user = ""
password = ""

# UBER DATA
DATE_COLUMN = 'date/time'
DATA_URL = ("https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz")


#  Loading UBER data
@st.cache  # st.cache is a Function decorator to memorize function executions.
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


#  Initialize connection to psql-db.
try:
    con = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

#  Query
all_students = pd.read_sql_query('select * from student', con)

############
### Body ###

st.title('PostgreSql Dataframe')
with st.container():



    with col1:
        st.subheader('Dataframe')
        st.write("Total of students: ", all_students.shape[0])

        #  printing psql data
        psql_data_load_state = st.text('Cargando contenidos...')
        st.write(all_students.head(20))
        psql_data_load_state.text('Trabajo terminado')


        data_load_state = st.text('Loading data...')  # Create a text element and let the reader know the data is loading.
        data = load_data(10000)  # Load 10,000 rows of data into the UBER dataframe.
        data_load_state.text("Done!")  # Notify the reader that the data was successfully loaded.

        # Filter
        hour_to_filter = st.slider('hour', 0, 17, 23)
        filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
        st.subheader('Map of all pickups at %s:00' % hour_to_filter)
        st.map(filtered_data)

    with col2:

        # Form
        st.subheader('Connect to your PostgreSql DB')
        st.text('test your local db')
        st.text_input('Host:')
        st.text_input('Port:')
        st.text_input('Database:', help="Your psql db name")
        st.text_input('User:')
        st.text_input('Pass:', type="password")


        # Grafico de barras
        st.subheader('Number of pickups by hour')
        hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
        st.bar_chart(hist_values)

        # Row data
        st.subheader('Raw data')
        st.write(data)

