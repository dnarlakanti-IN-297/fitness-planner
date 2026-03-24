import pytest
from app.diet_engine import generate_meal_plan
from app.models import DietPreference


def test_generate_meal_plan_balanced():
    """Test meal plan generation for balanced diet."""
    meal_plan = generate_meal_plan(2000, DietPreference.BALANCED)
    assert meal_plan.breakfast
    assert meal_plan.lunch
    assert meal_plan.dinner
    assert len(meal_plan.snacks) > 0
    assert meal_plan.total_calories > 0


def test_generate_meal_plan_vegan():
    """Test meal plan generation for vegan diet."""
    meal_plan = generate_meal_plan(2200, DietPreference.VEGAN)
    assert meal_plan.breakfast.name
    assert meal_plan.total_protein > 0


def test_generate_meal_plan_keto():
    """Test meal plan generation for keto diet."""
    meal_plan = generate_meal_plan(1800, DietPreference.KETO)
    # Keto should have low carbs
    assert meal_plan.breakfast.carbs < 15
    assert meal_plan.total_carbs < meal_plan.total_fat


def test_generate_meal_plan_high_protein():
    """Test meal plan generation for high protein diet."""
    meal_plan = generate_meal_plan(2500, DietPreference.HIGH_PROTEIN)
    # High protein should have more protein than other macros
    assert meal_plan.total_protein > 100


def test_meal_plan_calories_reasonable():
    """Test that meal plan calories are close to target."""
    target = 2000
    meal_plan = generate_meal_plan(target, DietPreference.BALANCED)
    # Allow 400 calorie variance
    assert abs(meal_plan.total_calories - target) < 400


def test_all_diet_preferences():
    """Test that all diet preferences work."""
    for pref in DietPreference:
        meal_plan = generate_meal_plan(2000, pref)
        assert meal_plan.breakfast
        assert meal_plan.lunch
        assert meal_plan.dinner
