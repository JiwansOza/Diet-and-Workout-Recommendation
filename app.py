import streamlit as st
import pandas as pd
from diet_model import predict_calories
import plotly.express as px

# Load datasets
df_meal = pd.read_csv('meal.csv')
df_recipe = pd.read_csv('recipe.csv', on_bad_lines='skip')  # Load recipe dataset, skip bad lines

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100  # Convert height to meters
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 24.9:
        status = "Healthy"
    elif 25 <= bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obese"
    return bmi, status

# Function to calculate daily calorie needs
def calculate_daily_calories(weight, activity_level, plan):
    if activity_level == 'Sedentary':
        base_calories = weight * 24
    elif activity_level == 'Moderate':
        base_calories = weight * 30
    else:
        base_calories = weight * 35
    
    if plan == 'Lose weight':
        daily_calories = base_calories - 500
    elif plan == 'Gain weight':
        daily_calories = base_calories + 500
    else:
        daily_calories = base_calories

    return daily_calories

# Function to distribute calories across meals
def distribute_calories(total_calories):
    breakfast_calories = total_calories * 0.3
    lunch_calories = total_calories * 0.4
    dinner_calories = total_calories * 0.3
    return breakfast_calories, lunch_calories, dinner_calories

# Function to pick multiple meals based on calorie target
def pick_multiple_meals(meal_type, target_calories, diet_preference, num_meals=3):
    filtered_meals = df_meal[(df_meal[meal_type] == 1) & (df_meal[diet_preference] == 1)]
    
    filtered_meals['predicted_calories'] = filtered_meals.apply(
        lambda row: predict_calories(row['Carbs'], row['Fat'], row['Protein'], row['Fiber']),
        axis=1
    )
    
    selected_meals = filtered_meals.iloc[(filtered_meals['predicted_calories'] - target_calories).abs().argsort()[:num_meals]]
    return selected_meals

# Function to get recipe for a meal
def get_recipe(meal_name):
    recipe = df_recipe[df_recipe['Recipe Name'] == meal_name]['Ingredients'].values
    return recipe[0] if len(recipe) > 0 else "No recipe available."

# Function to create pie chart for calorie distribution
def plot_calorie_distribution(breakfast_calories, lunch_calories, dinner_calories):
    labels = ['Breakfast', 'Lunch', 'Dinner']
    sizes = [breakfast_calories, lunch_calories, dinner_calories]

    fig = px.pie(names=labels, values=sizes, title='Calorie Distribution Across Meals', 
                  hole=0.3, color_discrete_sequence=px.colors.sequential.Greens)
    return fig

# Function to create bar chart for BMI category
def plot_bmi_distribution(bmi, status):
    categories = ['Underweight', 'Healthy', 'Overweight', 'Obese']
    values = [0, 0, 0, 0]
    
    if status == "Underweight":
        values[0] += 1
    elif status == "Healthy":
        values[1] += 1
    elif status == "Overweight":
        values[2] += 1
    else:
        values[3] += 1
    
    fig = px.bar(x=categories, y=values, title='BMI Distribution', 
                  labels={'x': 'BMI Categories', 'y': 'Count'},
                  color=categories, color_discrete_sequence=px.colors.qualitative.Set3)
    return fig

# Main Streamlit app interface
st.set_page_config(page_title="Diet & Workout Recommendation System", page_icon="🍽️", layout="wide")

# Displaying the image prominently
 # Replace with your image URL
st.title("🍽️ Diet & 🏋️‍♂️Workout Recommendation System")

st.markdown("#### Get personalized meal recommendations based on your preferences and daily calorie needs.")
st.markdown("---")  # Divider line
if 'image_visible' not in st.session_state:
    st.session_state.image_visible = True  # Default to True

# Display image if the session state allows
# if st.session_state.image_visible:
    st.image("image.jpg", caption="Healthy Diet & Fitness", use_column_width='auto' , width=600)

# Sidebar for user input
st.sidebar.header("Please Provide Your Details")
age = st.sidebar.number_input('Enter your age', min_value=1, help="Your age in years.")
weight = st.sidebar.number_input('Enter your weight (kg)', min_value=1, help="Your weight in kilograms.")
height = st.sidebar.number_input('Enter your height (cm)', min_value=1, help="Your height in centimeters.")
gender = st.sidebar.selectbox('Select your gender', ['Male', 'Female'], help="Select your gender.")
activity_level = st.sidebar.selectbox('Activity level', ['Sedentary', 'Moderate', 'Active'], help="Your activity level.")
weight_loss_plan = st.sidebar.selectbox('Weight loss plan', ['Maintain weight', 'Lose weight', 'Gain weight'], help="Select your weight management plan.")
diet_preference = st.sidebar.selectbox('Diet Preference', ['Veg', 'Non-veg'], help="Select your dietary preference.")

# Button to generate results with an icon
if st.sidebar.button('Generate Diet Plan  🥗'):
    st.session_state.image_visible = False  # Hide image after interaction # Hide image after interaction
    if weight <= 0 or height <= 0:
        st.error("Please enter valid weight and height.")
    else:
        with st.spinner('Generating your diet plan...'):
            # Calculate BMI and health status
            bmi, status = calculate_bmi(weight, height)
            st.markdown(f"### Your BMI: `{bmi:.2f}`")
            if status == "Healthy":
                st.success(f"Health Status: {status}")
            elif status == "Underweight":
                st.warning(f"Health Status: {status}")
            else:
                st.error(f"Health Status: {status}")

            # Calculate total daily calories needed
            daily_calories = calculate_daily_calories(weight, activity_level, weight_loss_plan)
            st.write(f"Total Calories to intake per day: {daily_calories:.2f} kcal")

            # Distribute calories across meals (Breakfast, Lunch, Dinner)
            breakfast_calories, lunch_calories, dinner_calories = distribute_calories(daily_calories)

            # Plot calorie distribution and BMI distribution side by side
            st.subheader('Visual Analysis')
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(plot_calorie_distribution(breakfast_calories, lunch_calories, dinner_calories), use_container_width=True)

            with col2:
                st.plotly_chart(plot_bmi_distribution(bmi, status), use_container_width=True)

            # Generate meal recommendations
            st.subheader('Recommended Meal Plan 🍽️')
            # Create a table for meal recommendations
            st.write("### Meals for the Day")

            # Create side-by-side columns for breakfast, lunch, and dinner
            col1, col2, col3 = st.columns(3)

            # Breakfast
            with col1:
                st.write("**Breakfast** 🍳")
                breakfast_meals = pick_multiple_meals('Breakfast', breakfast_calories, diet_preference, num_meals=3)
                for index, meal in breakfast_meals.iterrows():
                    with st.expander(f"{meal['Meals']}"):
                        recipe = get_recipe(meal['Meals'])
                        st.write(f"Recipe: {recipe}")
                        st.write(f"Calories: {meal['predicted_calories']:.2f} kcal")

            # Lunch
            with col2:
                st.write("**Lunch** 🍲")
                lunch_meals = pick_multiple_meals('Lunch', lunch_calories, diet_preference, num_meals=3)
                for index, meal in lunch_meals.iterrows():
                    with st.expander(f"{meal['Meals']}"):
                        recipe = get_recipe(meal['Meals'])
                        st.write(f"Recipe: {recipe}")
                        st.write(f"Calories: {meal['predicted_calories']:.2f} kcal")

            # Dinner
            with col3:
                st.write("**Dinner** 🍛")
                dinner_meals = pick_multiple_meals('Dinner', dinner_calories, diet_preference, num_meals=3)
                for index, meal in dinner_meals.iterrows():
                    with st.expander(f"{meal['Meals']}"):
                        recipe = get_recipe(meal['Meals'])
                        st.write(f"Recipe: {recipe}")
                        st.write(f"Calories: {meal['predicted_calories']:.2f} kcal")

            st.balloons()  # Celebration balloons when the diet plan is generated
            st.success("Your diet plan has been generated successfully!")

# Reset button to clear inputs
if st.sidebar.button('Reset Inputs 🔄'):
    st.session_state.image_visible = True  # Show image again
    st.experimental_rerun()
