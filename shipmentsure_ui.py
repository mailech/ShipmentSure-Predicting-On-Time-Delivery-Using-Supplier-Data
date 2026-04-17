import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

st.set_page_config(layout="wide")

st.title("📦 ShipmentSure Delivery Prediction")



# LOAD MODELS

lr=joblib.load("logistic_model.pkl")
rf=joblib.load("rf_model.pkl")
xgb=joblib.load("xgb_model.pkl")
best=joblib.load("best_model.pkl")

# LOAD ENCODERS

warehouse_enc=joblib.load("warehouse_encoder.pkl")
shipment_enc=joblib.load("shipment_encoder.pkl")
importance_enc=joblib.load("importance_encoder.pkl")
gender_enc=joblib.load("gender_encoder.pkl")


# TABS

tab1,tab2,tab3,tab4=st.tabs([

"📦 Prediction Center",
"🤖 Model Performance",
"📊 Evaluation Metrics",
"📈 Dataset Analytics"

])


# =========================================
# TAB 1 PREDICTION
# =========================================

with tab1:

    st.subheader("Enter Shipment Details")

    col1,col2,col3=st.columns(3)

    with col1:

        warehouse=st.selectbox(
        "Warehouse Block",
        warehouse_enc.classes_
        )

        shipment=st.selectbox(
        "Mode of Shipment",
        shipment_enc.classes_
        )

        importance=st.selectbox(
        "Product Importance",
        importance_enc.classes_
        )


    with col2:

        calls=st.slider(
        "Customer Care Calls",
        0,10,3
        )

        rating=st.slider(
        "Customer Rating",
        1,5,3
        )

        gender=st.selectbox(
        "Gender",
        gender_enc.classes_
        )


    with col3:

        cost=st.number_input(
        "Product Cost",
        100,10000,2000
        )

        prior=st.number_input(
        "Prior Purchases",
        0,20,3
        )

        discount=st.slider(
        "Discount Offered",
        0,70,10
        )

        weight=st.number_input(
        "Weight (grams)",
        100,8000,3000
        )


    if st.button("Predict Delivery Status"):

        data=np.array([[

        warehouse_enc.transform([warehouse])[0],
        shipment_enc.transform([shipment])[0],
        calls,
        rating,
        cost,
        prior,
        importance_enc.transform([importance])[0],
        gender_enc.transform([gender])[0],
        discount,
        weight

        ]])

        pred=best.predict(data)

        prob=best.predict_proba(data)


        st.divider()

        if pred[0]==1:

            st.error("⚠️ Shipment will be DELAYED")

        else:

            st.success("✅ Shipment will arrive ON TIME")


        st.subheader("Prediction Confidence")

        st.write("On Time Probability:",round(prob[0][0]*100,2),"%")

        st.write("Delay Probability:",round(prob[0][1]*100,2),"%")


# =========================================
# TAB 2 MODEL PERFORMANCE
# =========================================

with tab2:

    st.subheader("Model Accuracy Comparison")

    model_df=pd.DataFrame({

    "Model":[

    "Logistic Regression",
    "Random Forest",
    "XGBoost"

    ],

    "Accuracy":[

    0.63,
    0.66,
    0.67

    ]

    })

    fig=px.bar(

    model_df,
    x="Model",
    y="Accuracy",
    color="Model",
    title="Model Accuracy Comparison"

    )

    st.plotly_chart(fig,use_container_width=True)




# =========================================
# TAB 3 EVALUATION METRICS
# =========================================

with tab3:

    st.subheader("Confusion Matrix")

    df=pd.read_csv("Train.csv")

    df=df.drop("ID",axis=1)


    df["Warehouse_block"]=warehouse_enc.transform(df["Warehouse_block"])

    df["Mode_of_Shipment"]=shipment_enc.transform(df["Mode_of_Shipment"])

    df["Product_importance"]=importance_enc.transform(df["Product_importance"])

    df["Gender"]=gender_enc.transform(df["Gender"])


    X=df.drop("Reached.on.Time_Y.N",axis=1)

    y=df["Reached.on.Time_Y.N"]


    pred=best.predict(X)


    cm=confusion_matrix(y,pred)

    fig,ax=plt.subplots()

    sns.heatmap(cm,annot=True,fmt="d",cmap="Blues")

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    st.pyplot(fig)


    st.subheader("Classification Report")

    report=classification_report(y,pred,output_dict=True)

    report_df=pd.DataFrame(report).transpose()

    st.dataframe(report_df)


# =========================================
# TAB 4 DATASET ANALYTICS
# =========================================

with tab4:

    df=pd.read_csv("Train.csv")

    st.subheader("Dataset Preview")

    st.dataframe(df.head())


    st.subheader("Delivery Status Distribution")

    fig,ax=plt.subplots()

    sns.countplot(

    x="Reached.on.Time_Y.N",

    data=df

    )

    st.pyplot(fig)


    st.subheader("Shipment Mode Distribution")

    fig,ax=plt.subplots()

    sns.countplot(

    x="Mode_of_Shipment",

    data=df

    )

    st.pyplot(fig)


    st.subheader("Discount vs Delivery")

    fig,ax=plt.subplots()

    sns.boxplot(

    x="Reached.on.Time_Y.N",

    y="Discount_offered",

    data=df

    )

    st.pyplot(fig)


    st.subheader("Product Cost Distribution")

    fig=px.histogram(

    df,

    x="Cost_of_the_Product",

    color="Reached.on.Time_Y.N"

    )

    st.plotly_chart(fig)


    st.subheader("Feature Correlation Heatmap")

    numeric=df.select_dtypes(include=np.number)

    fig,ax=plt.subplots(figsize=(10,6))

    sns.heatmap(

    numeric.corr(),

    annot=True,

    cmap="coolwarm"

    )

    st.pyplot(fig)


# FEATURE IMPORTANCE BONUS

try:

    st.subheader("Feature Importance")

    importance=rf.feature_importances_

    features=X.columns

    imp_df=pd.DataFrame({

    "Feature":features,

    "Importance":importance

    })

    fig=px.bar(

    imp_df,

    x="Importance",

    y="Feature",

    orientation="h"

    )

    st.plotly_chart(fig)

except:

    st.write("Feature importance not available")