import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


# LOAD DATA

df=pd.read_csv("Train.csv")

# DROP ID

df=df.drop("ID",axis=1)


# ENCODING

le_warehouse=LabelEncoder()
le_shipment=LabelEncoder()
le_importance=LabelEncoder()
le_gender=LabelEncoder()


df["Warehouse_block"]=le_warehouse.fit_transform(df["Warehouse_block"])

df["Mode_of_Shipment"]=le_shipment.fit_transform(df["Mode_of_Shipment"])

df["Product_importance"]=le_importance.fit_transform(df["Product_importance"])

df["Gender"]=le_gender.fit_transform(df["Gender"])


# SAVE ENCODERS

joblib.dump(le_warehouse,"warehouse_encoder.pkl")
joblib.dump(le_shipment,"shipment_encoder.pkl")
joblib.dump(le_importance,"importance_encoder.pkl")
joblib.dump(le_gender,"gender_encoder.pkl")


# FEATURES / TARGET

X=df.drop("Reached.on.Time_Y.N",axis=1)

y=df["Reached.on.Time_Y.N"]


# SPLIT

X_train,X_test,y_train,y_test=train_test_split(

X,
y,
test_size=0.2,
random_state=42

)


# MODELS

lr=LogisticRegression(max_iter=2000)

rf=RandomForestClassifier()

xgb=XGBClassifier()


# TRAIN

lr.fit(X_train,y_train)

rf.fit(X_train,y_train)

xgb.fit(X_train,y_train)


# PREDICT

lr_pred=lr.predict(X_test)

rf_pred=rf.predict(X_test)

xgb_pred=xgb.predict(X_test)


# ACCURACY

lr_acc=accuracy_score(y_test,lr_pred)

rf_acc=accuracy_score(y_test,rf_pred)

xgb_acc=accuracy_score(y_test,xgb_pred)


print("Logistic:",lr_acc)

print("Random Forest:",rf_acc)

print("XGBoost:",xgb_acc)


# SAVE MODELS

joblib.dump(lr,"logistic_model.pkl")

joblib.dump(rf,"rf_model.pkl")

joblib.dump(xgb,"xgb_model.pkl")


# BEST MODEL

models={

"lr":(lr,lr_acc),

"rf":(rf,rf_acc),

"xgb":(xgb,xgb_acc)

}

best=max(models,key=lambda x:models[x][1])

print("Best Model:",best)


joblib.dump(models[best][0],"best_model.pkl")