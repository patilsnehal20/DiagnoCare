import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Get the current directory (which will be 'pages/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load your dataset
df = pd.read_csv(os.path.join(BASE_DIR, "diet_data.csv"))

# Encode categorical variables
le_condition = LabelEncoder()
le_diet = LabelEncoder()

# Replace 'None' with 'No Condition'
df['condition'] = df['condition'].replace('None', 'No Condition')

# Normalize text formatting just in case
df['condition'] = df['condition'].str.strip().str.title()

df['condition_encoded'] = le_condition.fit_transform(df['condition'])
df['diet_encoded'] = le_diet.fit_transform(df['diet_type'])

# Features and labels
X = df[['age', 'bmi', 'condition_encoded']]
y = df['diet_encoded']

# Train a simple Decision Tree
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model and encoders to same directory
joblib.dump(model, os.path.join(BASE_DIR, 'diet_model.pkl'))
joblib.dump(le_condition, os.path.join(BASE_DIR, 'condition_encoder.pkl'))
joblib.dump(le_diet, os.path.join(BASE_DIR, 'diet_encoder.pkl'))

print("✅ Model trained and saved!")
