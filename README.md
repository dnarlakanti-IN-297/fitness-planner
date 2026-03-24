# Fitness & Diet Planner API

A FastAPI application that generates personalized workout and diet plans based on user fitness goals.

## Features

- **BMI Calculator**: Calculate Body Mass Index and healthy weight range
- **Calorie Calculator**: Calculate BMR, TDEE, and target calories based on goals
- **Macro Calculator**: Get personalized protein/carbs/fat splits
- **Workout Plans**: Weekly workout schedules based on goals and equipment
- **Diet Plans**: Daily meal plans based on dietary preferences and calorie needs
- **Complete Plans**: All-in-one endpoint for full fitness planning

## Quick Start

### Local Development

1. Install dependencies:
```bash
cd fitness-planner
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

3. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run Tests

```bash
pytest tests/ -v
```

### Docker

Build and run with Docker:

```bash
docker build -t fitness-planner .
docker run -p 8000:8000 fitness-planner
```

## CI/CD Setup

This project includes a complete CI/CD pipeline with:

### Components

1. **Custom Test Action** (`.github/actions/test-and-publish/`)
   - Runs pytest tests
   - Publishes test results

2. **Reusable Build Workflow** (`.github/workflows/build-reusable.yml`)
   - Uses Kaniko for container builds
   - Pushes images to Docker Hub

3. **Main CI Workflow** (`.github/workflows/ci.yml`)
   - Test job: Uses custom action
   - Build job: Calls reusable workflow
   - Triggers: Push to main/develop and manual dispatch

### Required Secrets

Add these secrets to your GitHub repository:

- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token

To create a Docker Hub token:
1. Log in to Docker Hub
2. Go to Account Settings → Security
3. Click "New Access Token"
4. Copy the token and add it to GitHub secrets

## API Usage Example

```python
import requests

# User profile
profile = {
    "age": 30,
    "weight": 70,
    "height": 175,
    "gender": "male",
    "activity_level": "moderate",
    "goal": "lose_weight",
    "diet_preference": "balanced",
    "equipment": "gym"
}

# Generate complete plan
response = requests.post(
    "http://localhost:8000/generate/complete-plan",
    json=profile
)

plan = response.json()
print(f"BMI: {plan['bmi']['bmi']}")
print(f"Target Calories: {plan['calories']['target_calories']}")
print(f"Workout Days: {len(plan['workout_plan']['weekly_schedule'])}")
```

## Project Structure

```
fitness-planner/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── calculators.py       # BMI, calorie, macro calculators
│   ├── workout_engine.py    # Workout plan generation
│   └── diet_engine.py       # Meal plan generation
├── tests/
│   ├── test_api.py
│   ├── test_calculators.py
│   ├── test_workout_engine.py
│   └── test_diet_engine.py
├── .github/
│   ├── actions/
│   │   └── test-and-publish/
│   │       └── action.yml   # Custom test action
│   └── workflows/
│       ├── ci.yml           # Main CI workflow
│       └── build-reusable.yml  # Reusable build workflow
├── Dockerfile
└── requirements.txt
```

## Goals Supported

- `lose_weight`: 500 calorie deficit
- `gain_muscle`: 300 calorie surplus
- `maintain`: Maintenance calories
- `improve_endurance`: Slight surplus for training

## Diet Preferences

- `balanced`: Well-rounded nutrition
- `vegetarian`: No meat
- `vegan`: Plant-based only
- `keto`: Low-carb, high-fat
- `high_protein`: Protein-focused

## Equipment Options

- `bodyweight`: No equipment needed
- `home`: Dumbbells/basic equipment
- `gym`: Full gym access
