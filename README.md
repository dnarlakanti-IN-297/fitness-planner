# Fitness & Diet Planner API

A FastAPI application that generates personalized workout and diet plans based on user fitness goals.

## Overview

The Fitness Planner API is a REST service built with Python and FastAPI that provides:
- BMI calculations and health metrics
- Personalized calorie and macro nutrient recommendations
- Custom workout plans based on goals and equipment availability
- Daily meal plans tailored to dietary preferences
- Complete fitness planning in a single API call

**Technology Stack:**
- **Backend:** Python 3.11 with FastAPI
- **Testing:** pytest with coverage reporting
- **Containerization:** Docker
- **CI/CD:** CloudBees Unify with Kaniko

---

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
uvicorn app.main:app --reload
```

3. **Access API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run Tests

```bash
pytest tests/ -v
```

### Docker

```bash
docker build -t fitness-planner .
docker run -p 8000:8000 fitness-planner
```

---

## API Endpoints

### Health & Info
- `GET /` - API information and available endpoints
- `GET /health` - Health check

### Calculations
- `POST /calculate/bmi` - Calculate Body Mass Index
- `POST /calculate/calories` - Calculate BMR, TDEE, and target calories
- `POST /calculate/macros` - Calculate protein/carbs/fat splits

### Plan Generation
- `POST /generate/workout` - Generate weekly workout plan
- `POST /generate/meal-plan` - Generate daily meal plan
- `POST /generate/complete-plan` - Generate complete fitness plan (all-in-one)

### Example Request

```python
import requests

profile = {
    "age": 30,
    "weight": 75,          # kg
    "height": 180,         # cm
    "gender": "male",
    "activity_level": "moderate",
    "goal": "gain_muscle",
    "diet_preference": "high_protein",
    "equipment": "gym"
}

response = requests.post(
    "http://localhost:8000/generate/complete-plan",
    json=profile
)

plan = response.json()
```

---

## CI/CD Pipeline - CloudBees Unify

This project uses **CloudBees Unify** for continuous integration and deployment with a complete automated pipeline.

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CI/CD Pipeline                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Trigger (Push to main/develop OR Manual)                  │
│                    ↓                                        │
│  ┌──────────────────────────────────────────────────┐      │
│  │  JOB 1: TEST                                     │      │
│  ├──────────────────────────────────────────────────┤      │
│  │  1. Checkout code                                │      │
│  │  2. Install dependencies & run pytest            │      │
│  │  3. Publish test results (JUNIT)                 │      │
│  │  4. Extract test summary                         │      │
│  │  5. Publish test evidence (component)            │      │
│  └──────────────────────────────────────────────────┘      │
│                    ↓ (only if tests pass)                   │
│  ┌──────────────────────────────────────────────────┐      │
│  │  JOB 2: BUILD                                    │      │
│  ├──────────────────────────────────────────────────┤      │
│  │  Calls: build-reusable.yml                       │      │
│  │    1. Checkout code                              │      │
│  │    2. Configure Docker Hub credentials           │      │
│  │    3. Build image with Kaniko                    │      │
│  │    4. Push to Docker Hub (SHA + latest tags)     │      │
│  │    5. Publish build evidence                     │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Pipeline Components

#### 1. Main CI Workflow (`.cloudbees/workflows/ci.yml`)

**Purpose:** Orchestrates the entire CI/CD process

**Triggers:**
- **Automatic:** Push to `main` or `develop` branches
- **Manual:** workflow_dispatch (can be triggered manually from UI)

**Jobs:**

##### **Test Job**
Runs comprehensive testing and publishes results:

**Steps:**
1. **Checkout code** - Uses `cloudbees-io/checkout@v1`
2. **Install & Test** - Runs in Python 3.11 Docker container:
   ```bash
   pip install -r requirements.txt
   pytest tests/ -v --junitxml=test-results.xml --cov=app
   ```
3. **Publish Test Results** - Uses `cloudbees-io/publish-test-results@v2`
   - Format: JUNIT XML
   - Creates test dashboard in CloudBees UI
4. **Extract Test Summary** - Parses test-results.xml to extract:
   - Total test cases
   - Passed tests
   - Failed tests
5. **Publish Test Evidence** - Calls custom component
   - Uses: `./.cloudbees/components/publish-test-evidence`
   - Creates audit trail with test metrics, run ID, commit SHA

##### **Build Job**
Builds and pushes Docker image (runs only after test success):

**Steps:**
1. **Calls Reusable Workflow** - `./.cloudbees/workflows/build-reusable.yml`
2. **Passes Inputs:**
   - `image-name: fitness-planner`
   - `dockerfile-path: ./Dockerfile`
   - `context: .`
3. **Passes Secrets:**
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

---

#### 2. Reusable Build Workflow (`.cloudbees/workflows/build-reusable.yml`)

**Purpose:** Reusable workflow for building and pushing Docker images with Kaniko

**Trigger:** `workflow_call` (called by other workflows)

**Inputs:**
- `image-name` (required) - Name of the Docker image
- `dockerfile-path` (optional, default: `./Dockerfile`)
- `context` (optional, default: `.`)

**Secrets:**
- `DOCKERHUB_USERNAME` (required)
- `DOCKERHUB_TOKEN` (required)

**Steps:**
1. **Checkout code** - `cloudbees-io/checkout@v1`
2. **Configure Docker Hub credentials** - `cloudbees-io/configure-oci-credentials@v1`
   - Registry: `docker.io`
   - Authenticates with Docker Hub
3. **Build & Push with Kaniko** - `cloudbees-io/kaniko@v1`
   - **Why Kaniko?** Builds images without Docker daemon (more secure)
   - **Tags created:**
     - `docker.io/<username>/<image>:<commit-sha>` (specific version)
     - `docker.io/<username>/<image>:latest` (latest version)
4. **Publish Build Evidence** - Documents:
   - Run ID, branch, commit SHA
   - Docker image location
   - Build status

---

#### 3. Publish Test Evidence Component (`.cloudbees/components/publish-test-evidence/`)

**Purpose:** Reusable component for publishing test execution evidence

**Type:** Custom CloudBees Unify component (kind: action)

**Inputs:**
- `total-tests` - Total number of test cases
- `passed-tests` - Number of passed tests
- `failed-tests` - Number of failed tests

**What it does:**
- Creates a formatted Markdown evidence document
- Publishes using `cloudbees-io/publish-evidence-item@v1`
- Includes:
  - Test summary (total/passed/failed)
  - Workflow metadata (run ID, branch, commit)
  - Test details (framework, type, results file)

**Why use a component?**
- Eliminates code duplication
- Evidence format defined in ONE place
- Reusable across multiple workflows
- Easy to maintain and update

---

### Key Features

#### ✅ **Test Results Publishing**
- **Action:** `cloudbees-io/publish-test-results@v2`
- **Format:** JUNIT XML
- **Purpose:** Displays detailed test execution in CloudBees UI
- **Shows:** Individual test names, pass/fail status, execution times

#### ✅ **Test Evidence Publishing**
- **Action:** `cloudbees-io/publish-evidence-item@v1` (via component)
- **Format:** Markdown document
- **Purpose:** Compliance, audit trail, traceability
- **Shows:** Summary metrics, workflow info, test metadata

#### ✅ **Kaniko Build**
- **Why Kaniko?**
  - No Docker daemon required (runs in userspace)
  - More secure for CI/CD pipelines
  - Works in containerized environments
- **Multi-tag Strategy:**
  - SHA tag for version tracking
  - Latest tag for convenience

#### ✅ **Workflow Composition**
- **Reusable Workflow:** `build-reusable.yml` can be called from any workflow
- **Custom Component:** `publish-test-evidence` can be used in any job
- **No Code Duplication:** Logic defined once, used everywhere

#### ✅ **Quality Gates**
- Build job only runs if tests pass
- Failed tests block deployment
- Test results and evidence published for every run

---

### Required Configuration

#### CloudBees Unify Secrets

Add these secrets in CloudBees Unify platform:

1. **DOCKERHUB_USERNAME**
   - Your Docker Hub username
   - Used for authentication

2. **DOCKERHUB_TOKEN**
   - Docker Hub access token (NOT password)
   - Create at: Docker Hub → Account Settings → Security → New Access Token

#### Permissions

The workflows require these CloudBees permissions:
```yaml
permissions:
  scm-token-own: read
  scm-token-org: read
  id-token: read
```

---

### Directory Structure

```
fitness-planner/
├── .cloudbees/
│   ├── components/
│   │   └── publish-test-evidence/
│   │       └── action.yml              # Custom evidence component
│   └── workflows/
│       ├── ci.yml                      # Main CI workflow
│       └── build-reusable.yml          # Reusable build workflow
├── app/
│   ├── main.py                         # FastAPI application
│   ├── models.py                       # Pydantic models
│   ├── calculators.py                  # BMI, calorie, macro calculators
│   ├── workout_engine.py               # Workout plan generation
│   └── diet_engine.py                  # Meal plan generation
├── tests/
│   ├── test_api.py                     # API endpoint tests
│   ├── test_calculators.py             # Calculator tests
│   ├── test_workout_engine.py          # Workout generation tests
│   └── test_diet_engine.py             # Diet plan tests
├── Dockerfile                          # Container definition
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

### Pipeline Execution Flow

1. **Developer pushes code** to main or develop branch
2. **CloudBees Unify detects push** and triggers ci.yml workflow
3. **Test Job starts:**
   - Code is checked out
   - Python dependencies installed
   - pytest runs all tests with coverage
   - Test results published to CloudBees UI
   - Test summary extracted (total/passed/failed)
   - Evidence component called to publish audit trail
4. **Test Job completes** - If successful, build job starts
5. **Build Job starts:**
   - Calls build-reusable.yml workflow
   - Code checked out again
   - Docker Hub credentials configured
   - Kaniko builds Docker image
   - Image pushed with two tags (commit SHA + latest)
   - Build evidence published
6. **Pipeline completes** - Both test and build evidence available in CloudBees

---

### Manual Trigger

You can manually trigger the workflow from CloudBees Unify UI:
1. Navigate to the repository in CloudBees Unify
2. Go to Workflows
3. Select "CI Workflow"
4. Click "Run Workflow"
5. Choose the branch to run against

---

## Application Features

### Supported Goals
- `lose_weight` - 500 calorie deficit
- `gain_muscle` - 300 calorie surplus
- `maintain` - Maintenance calories
- `improve_endurance` - Slight surplus for training

### Diet Preferences
- `balanced` - Well-rounded nutrition
- `vegetarian` - No meat
- `vegan` - Plant-based only
- `keto` - Low-carb, high-fat
- `high_protein` - Protein-focused

### Equipment Options
- `bodyweight` - No equipment needed
- `home` - Dumbbells and basic equipment
- `gym` - Full gym access

---

## Development

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

### Code Structure

- **app/main.py** - FastAPI app initialization and endpoint definitions
- **app/models.py** - Pydantic models for request/response validation
- **app/calculators.py** - BMI, BMR, TDEE, calorie, macro calculations
- **app/workout_engine.py** - Workout plan generation logic
- **app/diet_engine.py** - Meal plan generation logic

---

## License

This project is for demonstration purposes.
