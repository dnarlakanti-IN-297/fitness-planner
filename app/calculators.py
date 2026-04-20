from app.models import Gender, ActivityLevel, Goal, BMIResult, CalorieResult, MacroResult
from typing import Optional


def calculate_bmi(weight_kg: float, height_cm: float) -> BMIResult:
    """Calculate BMI and return category."""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # Calculate healthy weight range for the given height
    height_m = height_cm / 100
    min_healthy = 18.5 * (height_m ** 2)
    max_healthy = 24.9 * (height_m ** 2)

    return BMIResult(
        bmi=round(bmi, 1),
        category=category,
        healthy_weight_range={
            "min_kg": round(min_healthy, 1),
            "max_kg": round(max_healthy, 1)
        }
    )


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: Gender, body_fat_percentage: Optional[float] = None, use_katch_mcardle: bool = False) -> float:
    """
    Calculate Basal Metabolic Rate.

    By default uses Mifflin-St Jeor Equation.
    If use_katch_mcardle=True and body_fat_percentage is provided, uses Katch-McArdle Formula.
    """
    if use_katch_mcardle and body_fat_percentage is not None:
        # Katch-McArdle Formula (requires lean body mass)
        lean_body_mass_kg = weight_kg * (1 - body_fat_percentage / 100)
        bmr = 370 + (21.6 * lean_body_mass_kg)
    else:
        # Mifflin-St Jeor Equation (default)
        if gender == Gender.MALE:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    return round(bmr, 1)


def calculate_tdee(bmr: float, activity_level: ActivityLevel) -> float:
    """Calculate Total Daily Energy Expenditure."""
    multipliers = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHT: 1.375,
        ActivityLevel.MODERATE: 1.55,
        ActivityLevel.ACTIVE: 1.725,
        ActivityLevel.VERY_ACTIVE: 1.9
    }

    return round(bmr * multipliers[activity_level], 1)


def calculate_target_calories(tdee: float, goal: Goal) -> CalorieResult:
    """Calculate target calories based on fitness goal."""
    descriptions = {
        Goal.LOSE_WEIGHT: "500 calorie deficit for steady weight loss",
        Goal.GAIN_MUSCLE: "300 calorie surplus for muscle growth",
        Goal.MAINTAIN: "Maintenance calories to maintain current weight",
        Goal.IMPROVE_ENDURANCE: "Slight surplus to support training"
    }

    adjustments = {
        Goal.LOSE_WEIGHT: -500,
        Goal.GAIN_MUSCLE: 300,
        Goal.MAINTAIN: 0,
        Goal.IMPROVE_ENDURANCE: 200
    }

    target = tdee + adjustments[goal]

    return CalorieResult(
        bmr=round(tdee / 1.55, 1),  # Approximate BMR
        tdee=tdee,
        target_calories=round(target, 1),
        description=descriptions[goal]
    )


def calculate_macros(target_calories: float, goal: Goal) -> MacroResult:
    """Calculate macro split based on goal."""
    # Macro ratios (protein%, carbs%, fat%)
    macro_ratios = {
        Goal.LOSE_WEIGHT: (0.35, 0.35, 0.30),
        Goal.GAIN_MUSCLE: (0.30, 0.45, 0.25),
        Goal.MAINTAIN: (0.25, 0.45, 0.30),
        Goal.IMPROVE_ENDURANCE: (0.20, 0.55, 0.25)
    }

    protein_pct, carbs_pct, fat_pct = macro_ratios[goal]

    # Calories per gram: Protein=4, Carbs=4, Fat=9
    protein_calories = target_calories * protein_pct
    carbs_calories = target_calories * carbs_pct
    fat_calories = target_calories * fat_pct

    protein_grams = protein_calories / 4
    carbs_grams = carbs_calories / 4
    fat_grams = fat_calories / 9

    return MacroResult(
        protein_grams=round(protein_grams, 1),
        carbs_grams=round(carbs_grams, 1),
        fat_grams=round(fat_grams, 1),
        protein_calories=round(protein_calories, 1),
        carbs_calories=round(carbs_calories, 1),
        fat_calories=round(fat_calories, 1)
    )
