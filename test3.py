import streamlit as st
import pandas as pd

# Sample data
data = {'Name': ['John', 'Jane', 'Doe'],
        'Age': [25, 30, 22]}

df = pd.DataFrame(data)

# Streamlit app
st.title('Streamlit Download Example')

# Display the dataframe
st.write('Sample DataFrame:', df)

# Create a download link for the dataframe as a CSV file
csv_data = df.to_csv(index=False)
st.download_button(label='Download CSV', data=csv_data, file_name='sample_data.csv', key='download_button')

# Alternatively, you can use st.markdown to create a download link
csv_link = f'<a href="data:file/csv;base64,{b64encode(csv_data.encode()).decode()}" download="sample_data.csv">Download CSV</a>'
st.markdown(csv_link, unsafe_allow_html=True)
