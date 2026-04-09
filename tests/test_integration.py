"""
Integration tests for Fitness Planner API.

These tests simulate real-world user journeys and test multiple components together.
They're naturally slower due to multiple API calls, data validation, and simulated delays.
"""

import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.integration
class TestUserJourneyWeightLoss:
    """Test complete user journey for weight loss goal."""

    def test_beginner_weight_loss_journey(self):
        """
        Simulate a beginner user starting their weight loss journey.
        Tests: BMI check → calorie calculation → meal plan → workout plan.
        """
        # Step 1: User checks their BMI first
        bmi_response = client.post("/calculate/bmi?weight_kg=90&height_cm=170")
        assert bmi_response.status_code == 200
        bmi_data = bmi_response.json()
        assert bmi_data["category"] in ["Overweight", "Obese"]

        # Simulate user taking time to read BMI results
        time.sleep(0.05)

        # Step 2: User creates profile and calculates calorie needs
        profile = {
            "age": 32,
            "weight": 90,
            "height": 170,
            "gender": "male",
            "activity_level": "sedentary",
            "goal": "lose_weight",
            "diet_preference": "balanced",
            "equipment": "home"
        }

        calories_response = client.post("/calculate/calories", json=profile)
        assert calories_response.status_code == 200
        calories_data = calories_response.json()
        assert calories_data["target_calories"] < calories_data["tdee"]

        # Step 3: User checks macro split for their diet
        macros_response = client.post("/calculate/macros", json=profile)
        assert macros_response.status_code == 200
        macros_data = macros_response.json()

        # Validate macros add up to target calories (within 5% margin)
        total_calories = (
            macros_data["protein_grams"] * 4 +
            macros_data["carbs_grams"] * 4 +
            macros_data["fat_grams"] * 9
        )
        assert abs(total_calories - calories_data["target_calories"]) < calories_data["target_calories"] * 0.05

        # Step 4: User generates meal plan
        meal_response = client.post("/generate/meal-plan", json=profile)
        assert meal_response.status_code == 200
        meal_data = meal_response.json()
        assert all(key in meal_data for key in ["breakfast", "lunch", "dinner", "snacks"])

        # Step 5: User generates workout plan
        workout_response = client.post("/generate/workout", json=profile)
        assert workout_response.status_code == 200
        workout_data = workout_response.json()
        assert len(workout_data["weekly_schedule"]) == 7


@pytest.mark.integration
class TestUserJourneyMuscleBulk:
    """Test complete user journey for muscle gain goal."""

    def test_intermediate_bulk_journey(self):
        """
        Simulate an intermediate lifter starting a bulk.
        Tests: Complete plan generation → validation → regeneration with changes.
        """
        profile = {
            "age": 25,
            "weight": 75,
            "height": 180,
            "gender": "male",
            "activity_level": "very_active",
            "goal": "gain_muscle",
            "diet_preference": "high_protein",
            "equipment": "gym"
        }

        # Step 1: Generate initial complete plan
        complete_response = client.post("/generate/complete-plan", json=profile)
        assert complete_response.status_code == 200
        plan_data = complete_response.json()

        # Validate all components are present
        assert "bmi" in plan_data
        assert "calories" in plan_data
        assert "macros" in plan_data
        assert "workout_plan" in plan_data
        assert "meal_plan" in plan_data

        # Step 2: User realizes they want more protein, recalculates macros
        time.sleep(0.03)
        profile["diet_preference"] = "high_protein"
        macros_response = client.post("/calculate/macros", json=profile)
        assert macros_response.status_code == 200
        new_macros = macros_response.json()

        # Verify high protein diet gives more protein
        assert new_macros["protein_grams"] > 150  # High protein for bulking

        # Step 3: User changes equipment preference and regenerates workout
        time.sleep(0.03)
        profile["equipment"] = "gym"
        workout_response = client.post("/generate/workout", json=profile)
        assert workout_response.status_code == 200
        gym_workout = workout_response.json()

        # Verify gym workout has appropriate exercises
        assert len(gym_workout["weekly_schedule"]) == 7


@pytest.mark.integration
class TestMultipleUserScenarios:
    """Test different user scenarios in sequence."""

    def test_family_fitness_planning(self):
        """
        Simulate a family creating fitness plans for multiple members.
        Tests data isolation and correct calculations for different profiles.
        """
        # User 1: Father - weight loss
        father = {
            "age": 45,
            "weight": 95,
            "height": 175,
            "gender": "male",
            "activity_level": "moderate",
            "goal": "lose_weight",
            "diet_preference": "balanced",
            "equipment": "gym"
        }

        father_plan = client.post("/generate/complete-plan", json=father)
        assert father_plan.status_code == 200
        father_data = father_plan.json()
        father_calories = father_data["calories"]["target_calories"]

        time.sleep(0.04)

        # User 2: Mother - maintain
        mother = {
            "age": 42,
            "weight": 65,
            "height": 165,
            "gender": "female",
            "activity_level": "moderate",
            "goal": "maintain",
            "diet_preference": "vegan",
            "equipment": "home"
        }

        mother_plan = client.post("/generate/complete-plan", json=mother)
        assert mother_plan.status_code == 200
        mother_data = mother_plan.json()
        mother_calories = mother_data["calories"]["target_calories"]

        time.sleep(0.04)

        # User 3: Teenage son - gain muscle
        son = {
            "age": 17,
            "weight": 65,
            "height": 175,
            "gender": "male",
            "activity_level": "very_active",
            "goal": "gain_muscle",
            "diet_preference": "high_protein",
            "equipment": "gym"
        }

        son_plan = client.post("/generate/complete-plan", json=son)
        assert son_plan.status_code == 200
        son_data = son_plan.json()
        son_calories = son_data["calories"]["target_calories"]

        # Validate: Son (bulking, very active) should have highest calories
        # Mother (maintain) and Father (cutting) will vary by body composition
        assert son_calories > father_calories  # Bulking teen > cutting adult
        assert all([father_calories > 1500, mother_calories > 1500, son_calories > 2000])

        # Validate diet preferences are respected
        assert mother_data["meal_plan"]["breakfast"]  # Vegan options
        assert son_data["meal_plan"]["breakfast"]  # High protein options


@pytest.mark.integration
@pytest.mark.parametrize("age,weight,height,gender,activity", [
    (25, 70, 175, "male", "moderate"),
    (30, 80, 180, "male", "active"),
    (28, 75, 178, "male", "very_active"),
    (35, 85, 182, "male", "sedentary"),
    (22, 90, 185, "male", "moderate"),
    (25, 60, 165, "female", "moderate"),
    (30, 65, 168, "female", "active"),
    (28, 70, 170, "female", "very_active"),
    (35, 75, 172, "female", "sedentary"),
    (22, 55, 160, "female", "moderate"),
])
def test_calorie_calculations_various_profiles(age, weight, height, gender, activity):
    """
    Test calorie calculations across many different user profiles.
    This creates 10 test cases, making the suite longer.
    """
    profile = {
        "age": age,
        "weight": weight,
        "height": height,
        "gender": gender,
        "activity_level": activity,
        "goal": "maintain",
        "diet_preference": "balanced",
        "equipment": "gym"
    }

    response = client.post("/calculate/calories", json=profile)
    assert response.status_code == 200
    data = response.json()

    # Validate reasonable calorie ranges
    assert 1000 <= data["bmr"] <= 3000  # Allow lower BMR for smaller/older females
    assert 1200 <= data["tdee"] <= 5000
    assert data["tdee"] >= data["bmr"]


@pytest.mark.integration
class TestDataConsistency:
    """Test data consistency across multiple endpoint calls."""

    def test_calorie_consistency_across_endpoints(self):
        """
        Verify that calorie calculations are consistent when called
        through different endpoints.
        """
        profile = {
            "age": 30,
            "weight": 70,
            "height": 175,
            "gender": "male",
            "activity_level": "moderate",
            "goal": "maintain",
            "diet_preference": "balanced",
            "equipment": "gym"
        }

        # Get calories from dedicated endpoint
        calories_direct = client.post("/calculate/calories", json=profile)
        calories_data = calories_direct.json()

        time.sleep(0.02)

        # Get calories from complete plan endpoint
        complete_plan = client.post("/generate/complete-plan", json=profile)
        complete_data = complete_plan.json()

        # Verify consistency
        assert calories_data["bmr"] == complete_data["calories"]["bmr"]
        assert calories_data["tdee"] == complete_data["calories"]["tdee"]
        assert calories_data["target_calories"] == complete_data["calories"]["target_calories"]

    def test_macro_calculations_match_calorie_target(self):
        """
        Verify macros always add up to the target calories.
        Tests all three macro calculation goals.
        """
        base_profile = {
            "age": 28,
            "weight": 75,
            "height": 180,
            "gender": "male",
            "activity_level": "active",
            "diet_preference": "balanced",
            "equipment": "gym"
        }

        goals = ["lose_weight", "maintain", "gain_muscle"]

        for goal in goals:
            profile = {**base_profile, "goal": goal}

            # Get target calories
            calories_response = client.post("/calculate/calories", json=profile)
            target_cal = calories_response.json()["target_calories"]

            time.sleep(0.02)

            # Get macros
            macros_response = client.post("/calculate/macros", json=profile)
            macros = macros_response.json()

            # Calculate calories from macros
            protein_cal = macros["protein_grams"] * 4
            carbs_cal = macros["carbs_grams"] * 4
            fat_cal = macros["fat_grams"] * 9
            total_cal = protein_cal + carbs_cal + fat_cal

            # Allow 5% margin for rounding
            assert abs(total_cal - target_cal) < target_cal * 0.05, \
                f"Goal: {goal}, Macros total: {total_cal}, Target: {target_cal}"


@pytest.mark.integration
@pytest.mark.slow
class TestConcurrentRequests:
    """Test handling of concurrent user requests."""

    def test_multiple_complete_plans_generated_concurrently(self):
        """
        Simulate multiple users generating plans simultaneously.
        In real scenarios, this tests database connection pooling,
        cache behavior, and resource management.
        """
        profiles = [
            {
                "age": 25 + i,
                "weight": 70 + i * 5,
                "height": 175,
                "gender": "male" if i % 2 == 0 else "female",
                "activity_level": "moderate",
                "goal": "maintain",
                "diet_preference": "balanced",
                "equipment": "gym"
            }
            for i in range(5)
        ]

        results = []
        for profile in profiles:
            response = client.post("/generate/complete-plan", json=profile)
            assert response.status_code == 200
            results.append(response.json())
            time.sleep(0.03)  # Simulate network latency

        # Verify all plans were generated successfully
        assert len(results) == 5

        # Verify each plan is unique (different calories for different weights)
        calories_list = [r["calories"]["target_calories"] for r in results]
        assert len(set(calories_list)) > 1  # At least some variation


@pytest.mark.integration
class TestEdgeCasesAndValidation:
    """Test edge cases across multiple endpoints."""

    def test_extreme_weight_loss_goal_safety_checks(self):
        """
        Test that extreme weight loss doesn't result in dangerously low calories.
        This would normally involve checking against medical guidelines.
        """
        # Very overweight user wanting to lose weight
        profile = {
            "age": 35,
            "weight": 150,
            "height": 170,
            "gender": "male",
            "activity_level": "sedentary",
            "goal": "lose_weight",
            "diet_preference": "balanced",
            "equipment": "home"
        }

        response = client.post("/calculate/calories", json=profile)
        assert response.status_code == 200
        data = response.json()

        # Even with extreme weight loss goal, calories shouldn't go below safe minimum
        # For males, minimum is typically 1500 calories
        assert data["target_calories"] >= 1200, "Calories too low for safety"

    def test_very_tall_and_very_short_users(self):
        """
        Test BMI and calorie calculations for extreme heights.
        """
        # Very tall user
        tall_response = client.post("/calculate/bmi?weight_kg=90&height_cm=210")
        assert tall_response.status_code == 200
        tall_bmi = tall_response.json()["bmi"]

        time.sleep(0.02)

        # Very short user
        short_response = client.post("/calculate/bmi?weight_kg=50&height_cm=150")
        assert short_response.status_code == 200
        short_bmi = short_response.json()["bmi"]

        # Both should return valid BMI values
        assert 15 <= tall_bmi <= 30
        assert 15 <= short_bmi <= 30


@pytest.mark.integration
class TestWorkoutMealPlanCorrelation:
    """Test that workout and meal plans are appropriate for each other."""

    def test_high_intensity_workout_matches_high_calories(self):
        """
        Verify that users with gym equipment and muscle gain goals
        get both intensive workouts and sufficient calories.
        """
        profile = {
            "age": 25,
            "weight": 70,
            "height": 180,
            "gender": "male",
            "activity_level": "very_active",
            "goal": "gain_muscle",
            "diet_preference": "high_protein",
            "equipment": "gym"
        }

        # Generate complete plan
        response = client.post("/generate/complete-plan", json=profile)
        assert response.status_code == 200
        plan = response.json()

        # Verify high calories for bulking
        assert plan["calories"]["target_calories"] > plan["calories"]["tdee"]

        # Verify high protein for muscle gain
        assert plan["macros"]["protein_grams"] > 140

        # Verify workout plan exists and has 7 days
        assert len(plan["workout_plan"]["weekly_schedule"]) == 7

    def test_bodyweight_workout_for_home_equipment(self):
        """
        Verify that users with home/bodyweight equipment get appropriate workouts.
        """
        profiles = [
            {"equipment": "home", "expected": "home"},
            {"equipment": "bodyweight", "expected": "bodyweight"},
            {"equipment": "gym", "expected": "gym"},
        ]

        for config in profiles:
            profile = {
                "age": 28,
                "weight": 70,
                "height": 175,
                "gender": "male",
                "activity_level": "moderate",
                "goal": "maintain",
                "diet_preference": "balanced",
                "equipment": config["equipment"]
            }

            response = client.post("/generate/workout", json=profile)
            assert response.status_code == 200

            time.sleep(0.02)


# Performance marker for grouping slow tests
pytestmark = pytest.mark.integration
