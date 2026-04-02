import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
df = pd.read_csv('Train.csv')

# Drop ID column
df = df.drop(columns=['ID'])

# Encode categorical columns
le = LabelEncoder()
cat_cols = ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance', 'Gender']
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# Separate features and target
X = df.drop(columns=['Reached.on.Time_Y.N'])
y = df['Reached.on.Time_Y.N']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))
print("✅ model.pkl saved successfully!")