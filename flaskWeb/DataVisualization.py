from dataclasses import dataclass
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import requests

def calculate_bmr(weight, height, age, sex):
    if sex == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:  # female
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

# Function to calculate daily calorie needs
def calculate_calorie_needs(bmr, activity_level):
    return float(bmr) * float(activity_level)

# Function to calculate macronutrient goals
def calculate_macros_protein(weight):
    protein_grams = 1.6 * weight
    return protein_grams        

def calculate_macros_fat(calorie_goal):
    fat_calories = calorie_goal * 0.25
    fat_grams = fat_calories / 9
    return fat_grams

def calculate_macros_carbs(calorie_goal, weight):
    protein_grams = 1.6 * weight
    fat_calories = calorie_goal * 0.25
    carb_calories = calorie_goal - (protein_grams * 4) - fat_calories
    carb_grams = carb_calories / 4
    return carb_grams

def calculate_weight_loss_plan(current_weight, goal_weight, height, age, sex, activity_level):
    activity_levels = {
    "1": 1.2,
    "2": 1.375,
    "3": 1.55,
    "4": 1.725,
    "5": 1.9
}
    
    weekly_loss_rate = 0.5  
    weight_loss_needed = current_weight - goal_weight
    weeks_to_goal = weight_loss_needed / weekly_loss_rate
    daily_calorie_deficit = (weekly_loss_rate * 7700) / 7
    bmr = calculate_bmr(current_weight, height, age, sex)
    maintenance_calories = calculate_calorie_needs(bmr, activity_level)
    new_calorie_goal = maintenance_calories - daily_calorie_deficit

    return weeks_to_goal, new_calorie_goal

def get_nutritional_data(food_name, serving_size, app_id, app_key):
    api_endpoint = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "ingr": f"{food_name} {serving_size}"
    }
    response = requests.get(api_endpoint, params=params)

    #IMPORTANT: block checks status code, 200 means it is successful, else it returns none. This is just how it be.
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


app_id = "9eaa615e"  # Edamam app ID
app_key = "823633324aefbe4dd49f24180783c007"  #Edamam app key

'''weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in cm: "))
age = int(input("Enter your age: "))
sex = input("Enter your sex (male/female): ")
current_weight_kg = float(input("Enter your current weight in kg: "))
goal_weight_kg = float(input("Enter your goal weight in kg: "))

print("How active are you?")
print("1. Lazy (little or no exercise)")
print("2. Lightly active (light exercise/sports 1-3 days a week)")
print("3. Moderately active (moderate exercise/sports 3-5 days a week)")
print("4. Very active (hard exercise/sports 6-7 days a week)")
print("5. Extra active (very hard exercise/sports & physical job or 2x training)")
activity_input = input("Choose your activity level (1-5): ")

activity_levels = {
    "1": 1.2,
    "2": 1.375,
    "3": 1.55,
    "4": 1.725,
    "5": 1.9
}
activity_level = activity_levels.get(activity_input, 1.2)

bmr = calculate_bmr(weight, height, age, sex)
calorie_goal = calculate_calorie_needs(bmr, activity_level)


weeks_to_goal, new_calorie_goal = calculate_weight_loss_plan(current_weight_kg, goal_weight_kg, weight, height, age, sex)
new_protein_goal, new_fat_goal, new_carb_goal = calculate_macros(new_calorie_goal, weight)

print(f"It will take approximately {weeks_to_goal:.1f} weeks to reach your goal weight of {goal_weight_kg} kg.")
print(f"Your daily calorie goal is now {new_calorie_goal:.0f} calories.")
print(f"Daily macronutrient goals: {new_protein_goal:.0f}g of protein, {new_fat_goal:.0f}g of fat, {new_carb_goal:.0f}g of carbs.")

@dataclass
class Food:
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int

today = []
done = False

while not done:
    print("""
        (1) Add new food
        (2) Visualize Progress
        (q) Quit
          """)
    choice = input("Choose option: ")

    if choice == "1":
        print("Adding new food!")
        name = input("Enter Food Name: ")
        serving = input("Enter serving size (e.g., 100g, 1 cup): ")
        food_data = get_nutritional_data(name, serving, app_id, app_key)
        if food_data is not None:
            calories = food_data.get("calories", 0)
            protein = food_data.get('totalNutrients', {}).get('PROCNT', {}).get('quantity', 0)
            fat = food_data.get("totalNutrients", {}).get('FAT', {}).get('quantity', 0)
            carbs = food_data.get("totalNutrients", {}).get('CHOCDF', {}).get('quantity', 0)
            food = Food(name, calories, protein, fat, carbs)
            today.append(food)
            print("Success")
            print("The macros for " + name)
            print("Calories " + str(calories))
            print("Protein " + str(protein))
            print("Fat " + str(fat))
            print("Carb " + str(carbs))
        else:
            print("Failed to fetch food data. Please correctly spell your food name or enter the appropriate serving size.")

    elif choice == "2":
        calorie_sum = sum(food.calories for food in today)
        protein_sum = sum(food.protein for food in today)
        fats_sum = sum(food.fat for food in today)
        carbs_sum = sum(food.carbs for food in today)

        figure, axes = plt.subplots(2, 2)
        axes[0, 0].pie([protein_sum, fats_sum, carbs_sum], labels=["Proteins", "Fats", "Carbs"], autopct="%1.1f%%")
        axes[0, 0].set_title("Macronutrients Distribution")

        axes[0, 1].bar([0, 1, 2], [protein_sum, fats_sum, carbs_sum], width=0.4)
        axes[0, 1].bar([0.5, 1.5, 2.5], [new_protein_goal, new_fat_goal, new_carb_goal], width=0.4)
        axes[0, 1].set_title("Macronutrients Progress")

        axes[1, 0].pie([calorie_sum, new_calorie_goal - calorie_sum], labels=["Calories", "Remaining"],
                       autopct="%1.1f%%")
        axes[1, 0].set_title("Calories Goal Progress")

        axes[1, 1].plot(list(range(len(today))), np.cumsum([food.calories for food in today]), label="Calories Eaten")
        axes[1, 1].plot(list(range(len(today))), [new_calorie_goal] * len(today), label="Calorie Goal")
        axes[1, 1].legend()
        axes[1, 1].set_title("Calories Goal Over Time")

        figure.tight_layout()
        plt.show()

    elif choice == "q":
        done = True
    else:
        print("Invalid choice!")
        '''