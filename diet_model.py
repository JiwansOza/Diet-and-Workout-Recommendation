import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the meal dataset
df_meal = pd.read_csv('meal.csv')

# Select relevant columns for prediction
X = df_meal[['Carbs', 'Fat', 'Protein', 'Fiber']]
y = df_meal['Cal/gm']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Function to predict calories based on user input
def predict_calories(carbs, fat, protein, fiber):
    prediction = model.predict([[carbs, fat, protein, fiber]])
    return prediction[0]
