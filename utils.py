def calculate_bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        health_status = "Underweight"
    elif 18.5 <= bmi < 24.9:
        health_status = "Normal weight"
    elif 25 <= bmi < 29.9:
        health_status = "Overweight"
    else:
        health_status = "Obesity"
    return bmi, health_status

def calculate_calories(weight, height, age, gender, activity_level, weight_loss_plan):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    if activity_level == "Sedentary":
        bmr *= 1.2
    elif activity_level == "Moderate":
        bmr *= 1.55
    elif activity_level == "Active":
        bmr *= 1.725

    # Adjust for weight loss plan
    if weight_loss_plan == "Mild (0.5 kg/week)":
        calories = bmr - 500
    elif weight_loss_plan == "Moderate (1 kg/week)":
        calories = bmr - 1000
    else:
        calories = bmr - 1500

    return calories
