import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Finance App", page_icon="💸", layout="wide")

if "categories" not in st.session_state:
    st.session_state.categories = {
        "uncategorized": []
    }

if os.path.exists("categories.json"):
    with open("categories.json", "r") as f:
        st.session_state.categories = json.load(f)

def save_categories():
    """
    Save the categories to a JSON file.
    """
    with open("categories.json", "w") as f:
        json.dump(st.session_state.categories, f)

def add_category(category):
    """
    Add a new category to the session state.
    """
    if category not in st.session_state.categories:
        st.session_state.categories[category] = []
        save_categories()

def categorize_transaction(transaction, category):
    """
    Categorize a transaction and add it to the specified category.
    """
    if category not in st.session_state.categories:
        st.session_state.categories[category] = []
    st.session_state.categories[category].append(transaction)
    save_categories()

def load_transacations(file):
    """
    Load transactions from a CSV file and return a DataFrame.
    """
    df = pd.read_csv(file)
    st.write(df)
    categorize_transaction(df, "uncategorized")
    return df


def main():
    st.title("Finance App")
    st.write("This is a simple finance app that allows you to upload a CSV file and visualize the data.")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = load_transacations(uploaded_file)

        add_category = st.text_input("Add a new category:")
        add_button = st.button("Add Category")
        
        if add_button and add_category:
            if  add_category not in st.session_state.categories:
                st.session_state.categories[add_category] = []
                save_categories()
                st.success(f"Category '{add_category}' added successfully!")
                st.rerun()


main()