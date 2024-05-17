import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Konfigurasi Page
st.set_page_config("Personal Loan Prediction", page_icon=':moneybag:', layout='wide' )

# Konfigurasi markdown header
style = "<style>h2 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)

# Session state configuration
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# /=============Function==========/
def load_model():
    with open("RFClassifier.sav", "rb") as file:
        model = pickle.load(file)
    return model

def predict(data:pd.DataFrame):
    model = load_model()
    prob = model.predict_proba(data)
    prob = prob[:,1]
    return prob


#/ ===============Title============/
st.title("Personal Loan")
st.write('Welocome to the **Personal Loan** Prediction Tool')
st.divider()

with st.sidebar:
    st.header("Menu")
    st.divider()
    st.button("Home", use_container_width=True)
    st.button("Setting", use_container_width=True)
    st.button("About", use_container_width=True)

# /=====================Main Pages=================/
# Membuat 2 kolom
left_panel, right_panel = st.columns(2, gap="Medium")

# --- Left Panel
left_panel.header("Information Panel")
# Membuat Tabs Overview di Left Panel
tabs1, tabs2 = left_panel.tabs(['Overview', 'Benefits'])

# Tabs 1: Benefit
tabs1.subheader("Overview")
tabs1.write("---Ini merupakan Overview---")
# Tabs 1: Benefit
tabs2.subheader("Benefit")
tabs2.write("---Ini merupakan Benefit---")

# /***** Right Panel *********/
right_panel.header("Prediction")

placeholder = right_panel.empty()
btn_placeholder = right_panel.empty()
feature_container = placeholder.container()

cust_id = feature_container.text_input("Customer ID", label_visibility='hidden', placeholder="Customer ID")
right_panel.write(cust_id)

feature_left, feature_right = right_panel.columns(2)

# Feature Left
feature_left.write("**Personal Information**")
feature_left.divider()
age = feature_left.number_input("Age", min_value=17, max_value=75, step=5, label_visibility='collapsed', placeholder="Please input your age")
education = feature_left.selectbox("Education", options=["Undergraduate", "Graduate", "Advance/Professional"])
income = feature_left.number_input("Annual Income ($ thousands)", step=10)
family = feature_left.number_input("Family Size", min_value=1, max_value=100)
experience = feature_left.number_input("Profesional Experience", step=1)
mortgage = feature_left.number_input("Mortgage Value of house ($ thousands)", step=10)

# Feature Right
feature_right.write("**Bank Account Information**")
feature_right.divider()
ccavg = feature_right.number_input("Monthly Credit Card Spending ($ thousands)", step=10)
ccd = feature_right.selectbox("Have Credit Card Account", options=['Yes', 'No'])
cda = feature_right.selectbox("Have Certificate Deposite Account", options=['Yes', 'No'])
security = feature_right.selectbox("Have Security Account", options=['Yes', 'No'])
online = feature_right.selectbox("Using internet Banking", options=['Yes', 'No'])

# Mapping
education_map = {"Undergraduate" : 1, "Graduate":2, "Advanced/Professional":3}
education = education_map[education]

bool_map = {"Yes":1, "No":0}
ccd = bool_map[ccd]
cda = bool_map[cda]
security = bool_map[security]
online = bool_map[online]

# Submit Button
feature_container.divider()
btn_submit = right_panel.button("Submit", use_container_width=True)

if btn_submit:
    st.session_state['submitted'] = True

if st.session_state['submitted']:
    data = pd. DataFrame(data=[cust_id, age, education, income, family, experience, mortgage,
                            ccavg, ccd, cda, security, online ],
                        columns=['Value'],
                        index=['Customer ID', 'Age', 'Education', 'Income', 'Family', 'Experience', 'Mortgage', 'CCAvg', 'CreditCard', 'CD Account',
                            'Securities Account', 'Online'])
    placeholder.dataframe(data, use_container_width=True)

    btn_placeholder.empty()
    btn_cancel = right_panel.button("Cancel", use_container_width=True)
    btn_predict = right_panel.button("Predict", use_container_width=True)

    if btn_cancel:
        st.session_state['submitted'] = False
        st.rerun()

    if btn_predict:
        data = data.T.drop('Customer ID', axis=1)
        pred = round(predict(data)[0] * 100, 2)
        right_panel.success(f"Customer with ID: {cust_id} have {pred}% to accept the Personal Loan Offer")
        st.balloons()
        # btn_predict = right_panel.button("Predict", use_container_width=True, disabled=True)