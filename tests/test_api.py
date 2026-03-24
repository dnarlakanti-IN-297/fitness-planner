import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_calculate_bmi():
    """Test BMI calculation endpoint."""
    response = client.post("/calculate/bmi?weight_kg=70&height_cm=175")
    assert response.status_code == 200
    data = response.json()
    assert "bmi" in data
    assert "category" in data


def test_calculate_calories():
    """Test calorie calculation endpoint."""
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
    response = client.post("/calculate/calories", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert "bmr" in data
    assert "tdee" in data
    assert "target_calories" in data


def test_calculate_macros():
    """Test macro calculation endpoint."""
    profile = {
        "age": 25,
        "weight": 65,
        "height": 165,
        "gender": "female",
        "activity_level": "active",
        "goal": "lose_weight",
        "diet_preference": "high_protein",
        "equipment": "home"
    }
    response = client.post("/calculate/macros", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert "protein_grams" in data
    assert "carbs_grams" in data
    assert "fat_grams" in data


def test_generate_workout():
    """Test workout generation endpoint."""
    profile = {
        "age": 28,
        "weight": 75,
        "height": 180,
        "gender": "male",
        "activity_level": "moderate",
        "goal": "gain_muscle",
        "diet_preference": "balanced",
        "equipment": "gym"
    }
    response = client.post("/generate/workout", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert "weekly_schedule" in data
    assert len(data["weekly_schedule"]) == 7


def test_generate_meal_plan():
    """Test meal plan generation endpoint."""
    profile = {
        "age": 30,
        "weight": 70,
        "height": 175,
        "gender": "male",
        "activity_level": "moderate",
        "goal": "maintain",
        "diet_preference": "vegan",
        "equipment": "bodyweight"
    }
    response = client.post("/generate/meal-plan", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert "breakfast" in data
    assert "lunch" in data
    assert "dinner" in data
    assert "snacks" in data


def test_generate_complete_plan():
    """Test complete plan generation endpoint."""
    profile = {
        "age": 35,
        "weight": 80,
        "height": 178,
        "gender": "male",
        "activity_level": "active",
        "goal": "lose_weight",
        "diet_preference": "balanced",
        "equipment": "gym"
    }
    response = client.post("/generate/complete-plan", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert "profile" in data
    assert "bmi" in data
    assert "calories" in data
    assert "macros" in data
    assert "workout_plan" in data
    assert "meal_plan" in data


def test_invalid_profile_age():
    """Test validation for invalid age."""
    profile = {
        "age": -5,
        "weight": 70,
        "height": 175,
        "gender": "male",
        "activity_level": "moderate",
        "goal": "maintain",
        "diet_preference": "balanced",
        "equipment": "gym"
    }
    response = client.post("/calculate/calories", json=profile)
    assert response.status_code == 422  # Validation error
