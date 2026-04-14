from fastapi import FastAPI
from app.models import UserProfile, BMIResult, CalorieResult, MacroResult, WorkoutPlan, DailyMealPlan, FitnessResponse
from app.calculators import calculate_bmi, calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros
from app.workout_engine import generate_workout_plan
from app.diet_engine import generate_meal_plan

# Import CloudBees Feature Management SDK
from rox.server.rox_server import Rox
from rox.server.flags.rox_flag import RoxFlag
from rox.core.entities.rox_string import RoxString
from rox.core.entities.rox_int import RoxInt
from rox.core.entities.rox_double import RoxDouble


# Create Roxflags in the Flags container class
class Flags:
    def __init__(self):
        # Define the feature flags
        self.enableTutorial = RoxFlag(False)
        self.titleColors = RoxString('White', ['White', 'Blue', 'Green', 'Yellow'])
        self.page = RoxInt(1, [1, 2, 3])
        self.percentage = RoxDouble(99.9, [10.5, 50.0, 99.9])


flags = Flags()

# Register the flags container
Rox.register(flags)

# Setup the environment key with timeout
try:
    cancel_event = Rox.setup("f47b55c1-76cb-4102-b266-4b7050af889c").result(timeout=10)
    print('✅ Rox connected successfully!')
except Exception as e:
    print(f'⚠️ Rox connection failed: {e}')
    print('   Flags will use default values')

# Boolean flag example
print('enableTutorial is {}'.format(flags.enableTutorial.is_enabled()))

# String flag example
print('color is {}'.format(flags.titleColors.get_value()))

# Int flag example
print('page is {}'.format(flags.page.get_value()))

# Double flag example
print('percentage is {}'.format(flags.percentage.get_value()))


app = FastAPI(
    title="Fitness & Diet Planner API",
    description="Generate personalized workout and meal plans based on your fitness goals",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Fitness & Diet Planner API",
        "version": "1.0.0",
        "endpoints": {
            "POST /calculate/bmi": "Calculate BMI",
            "POST /calculate/calories": "Calculate calorie needs",
            "POST /calculate/macros": "Calculate macro split",
            "POST /generate/workout": "Generate workout plan",
            "POST /generate/meal-plan": "Generate meal plan",
            "POST /generate/complete-plan": "Generate complete fitness plan"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/calculate/bmi", response_model=BMIResult)
def calculate_bmi_endpoint(weight_kg: float, height_cm: float):
    """
    Calculate Body Mass Index (BMI).

    - **weight_kg**: Weight in kilograms
    - **height_cm**: Height in centimeters
    """
    return calculate_bmi(weight_kg, height_cm)


@app.post("/calculate/calories", response_model=CalorieResult)
def calculate_calories_endpoint(profile: UserProfile):
    """
    Calculate calorie needs based on user profile.

    Returns BMR, TDEE, and target calories based on goal.
    """
    bmr = calculate_bmr(profile.weight, profile.height, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)
    return calculate_target_calories(tdee, profile.goal)


@app.post("/calculate/macros", response_model=MacroResult)
def calculate_macros_endpoint(profile: UserProfile):
    """
    Calculate macro split (protein/carbs/fat) based on user profile and goal.
    """
    bmr = calculate_bmr(profile.weight, profile.height, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)
    calorie_result = calculate_target_calories(tdee, profile.goal)
    return calculate_macros(calorie_result.target_calories, profile.goal)


@app.post("/generate/workout", response_model=WorkoutPlan)
def generate_workout_endpoint(profile: UserProfile):
    """
    Generate a weekly workout plan based on goal and available equipment.
    """
    return generate_workout_plan(profile.goal, profile.equipment)


@app.post("/generate/meal-plan", response_model=DailyMealPlan)
def generate_meal_plan_endpoint(profile: UserProfile):
    """
    Generate a daily meal plan based on calorie needs and dietary preferences.
    """
    bmr = calculate_bmr(profile.weight, profile.height, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)
    calorie_result = calculate_target_calories(tdee, profile.goal)
    return generate_meal_plan(calorie_result.target_calories, profile.diet_preference)


@app.post("/generate/complete-plan", response_model=FitnessResponse)
def generate_complete_plan(profile: UserProfile):
    """
    Generate a complete fitness plan including:
    - BMI calculation
    - Calorie needs
    - Macro split
    - Weekly workout plan
    - Daily meal plan
    """
    # Calculate all metrics
    bmi = calculate_bmi(profile.weight, profile.height)
    bmr = calculate_bmr(profile.weight, profile.height, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)
    calories = calculate_target_calories(tdee, profile.goal)
    macros = calculate_macros(calories.target_calories, profile.goal)

    # Generate plans
    workout_plan = generate_workout_plan(profile.goal, profile.equipment)
    meal_plan = generate_meal_plan(calories.target_calories, profile.diet_preference)

    return FitnessResponse(
        profile=profile,
        bmi=bmi,
        calories=calories,
        macros=macros,
        workout_plan=workout_plan,
        meal_plan=meal_plan
    )
