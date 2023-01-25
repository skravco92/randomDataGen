import streamlit as st
import pandas as pd
from faker import Faker
from config import locale_providers, optional_fields
import base64
import time

# Function to generate default data frame
def generate_defaul(n, l, random_seed=200):
    fake = Faker(l)
    # Generate simple profile data using the Faker instance
    d = [fake.simple_profile() for i in range(n)]
    df = pd.DataFrame(d)
    return df

# Function to generate custom data frame
def generate_custom(n, l, f, random_seed=200):
    fake = Faker(l)
    # Generate profile data using the Faker instance and the specified fields
    d = [fake.profile(fields=f) for i in range(n)]
    df = pd.DataFrame(d)
    return df

# Function to download the generated data in the specified format
def download(data, format_type="csv"):
    if format_type == "json":
        file = data.to_json()
    elif format_type == "xslx":
        file = data.to_xlsx()
    else:
        file = data.to_csv(index=False)

    # Get the current local time
    current_time = time.localtime()
    time_str = time.strftime("%a%d%b:%Y%H%M%S", current_time)

    # Encode the file as a base64 string
    b64 = base64.b64encode(file.encode()).decode()
    
    # Add a button to the user interface to download the file
    st.markdown("### Download ###")
    title = "random_df_{}.{}.".format(time_str, format_type)
    href = f'<a href = "data:file/{format_type};base64,{b64}" download="{title}"> Click Here! </a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    
    st.title("randomDataGenerator")

    # Sidebar with options for the user to select
    tree = ["default", "custom"]
    c = st.sidebar.selectbox("menu", tree)

    rows = st.sidebar.number_input("number", 5, 500)
    locale = st.sidebar.multiselect(
        "Locale", locale_providers, default="en_US")
    dataformat = st.sidebar.selectbox("Save As: ", ["csv", "json", "xlsx"])

    # Check which option the user selected and apply respective functions  
    if c == "default":
        st.subheader("Default Frame")

        df = generate_defaul(rows, locale)
        st.dataframe(df)

        with st.expander("Download file: "):
            download(df, dataformat)

    else:
        st.subheader("Custom Frame")
        fields = st.sidebar.multiselect("Fields", optional_fields, default="username")

        df = generate_custom(rows, locale, fields)
        st.dataframe(df)

        with st.expander("Download file: "):
            download(df, dataformat)

if __name__ == "__main__":
    main()
