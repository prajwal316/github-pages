import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
# For this example, we'll create a synthetic dataset
np.random.seed(42)
n_samples = 10000

# Create features
amount = np.random.normal(100, 50, n_samples)
time = np.random.randint(0, 24, n_samples)
day_of_week = np.random.randint(0, 7, n_samples)
is_weekend = (day_of_week >= 5).astype(int)

# Create the target variable (fraud)
fraud = np.random.choice([0, 1], n_samples, p=[0.99, 0.01])  # 1% fraud rate

# Introduce some patterns for fraudulent transactions
amount[fraud == 1] *= 1.5  # Fraudulent transactions tend to be larger
time[fraud == 1] = np.random.normal(3, 2, sum(fraud))  # Fraudulent transactions often happen late at night

# Create the dataframe
df = pd.DataFrame({
    'amount': amount,
    'time': time,
    'day_of_week': day_of_week,
    'is_weekend': is_weekend,
    'fraud': fraud
})

# Display the first few rows and data info
print(df.head())
print(df.info())

# Perform some basic EDA
print("\nDistribution of fraudulent transactions:")
print(df['fraud'].value_counts(normalize=True))

plt.figure(figsize=(10, 6))
sns.boxplot(x='fraud', y='amount', data=df)
plt.title('Distribution of Transaction Amounts by Fraud Status')
plt.savefig('amount_distribution.png')
plt.close()

# Prepare the data for modeling
X = df.drop('fraud', axis=1)
y = df['fraud']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('confusion_matrix.png')
plt.close()

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': abs(model.coef_[0])
})
feature_importance = feature_importance.sort_values('importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Feature Importance')
plt.savefig('feature_importance.png')
plt.close()

print("\nFeature Importance:")
print(feature_importance)

# Save the model
import joblib
joblib.dump(model, 'fraud_detection_model.joblib')
print("\nModel saved as 'fraud_detection_model.joblib'")

print("\nFraud Detection project completed successfully!")