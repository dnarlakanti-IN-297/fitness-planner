import pytest
from app.calculators import calculate_bmi, calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros
from app.models import Gender, ActivityLevel, Goal


def test_calculate_bmi_normal():
    """Test BMI calculation for normal weight."""
    result = calculate_bmi(70, 175)
    assert result.bmi == 22.9
    assert result.category == "Normal weight"


def test_calculate_bmi_underweight():
    """Test BMI calculation for underweight."""
    result = calculate_bmi(50, 175)
    assert result.category == "Underweight"


def test_calculate_bmi_overweight():
    """Test BMI calculation for overweight."""
    result = calculate_bmi(85, 175)
    assert result.category == "Overweight"


def test_calculate_bmi_obese():
    """Test BMI calculation for obese."""
    result = calculate_bmi(100, 175)
    assert result.category == "Obese"


def test_calculate_bmr_male():
    """Test BMR calculation for male."""
    bmr = calculate_bmr(80, 180, 30, Gender.MALE)
    assert bmr > 0
    assert isinstance(bmr, float)


def test_calculate_bmr_female():
    """Test BMR calculation for female."""
    bmr = calculate_bmr(65, 165, 28, Gender.FEMALE)
    assert bmr > 0
    assert isinstance(bmr, float)
    # Female BMR should be lower than male with similar stats
    male_bmr = calculate_bmr(65, 165, 28, Gender.MALE)
    assert bmr < male_bmr


def test_calculate_tdee():
    """Test TDEE calculation."""
    bmr = 1500
    tdee = calculate_tdee(bmr, ActivityLevel.MODERATE)
    assert tdee == 2325.0  # 1500 * 1.55


def test_calculate_target_calories_lose_weight():
    """Test target calories for weight loss."""
    result = calculate_target_calories(2000, Goal.LOSE_WEIGHT)
    assert result.tdee == 2000
    assert result.target_calories == 1500.0  # 2000 - 500


def test_calculate_target_calories_gain_muscle():
    """Test target calories for muscle gain."""
    result = calculate_target_calories(2000, Goal.GAIN_MUSCLE)
    assert result.target_calories == 2300.0  # 2000 + 300


def test_calculate_macros_lose_weight():
    """Test macro calculation for weight loss."""
    macros = calculate_macros(2000, Goal.LOSE_WEIGHT)
    assert macros.protein_grams > 0
    assert macros.carbs_grams > 0
    assert macros.fat_grams > 0
    # Check total calories approximately match
    total_cals = (macros.protein_grams * 4) + (macros.carbs_grams * 4) + (macros.fat_grams * 9)
    assert abs(total_cals - 2000) < 10


def test_calculate_macros_gain_muscle():
    """Test macro calculation for muscle gain."""
    macros = calculate_macros(2500, Goal.GAIN_MUSCLE)
    # Muscle gain should have higher carbs percentage
    assert macros.carbs_grams > macros.protein_grams
    assert macros.protein_grams > macros.fat_grams
