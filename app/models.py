from pydantic import BaseModel, Field
from typing import Literal, Optional, List
from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Goal(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    GAIN_MUSCLE = "gain_muscle"
    MAINTAIN = "maintain"
    IMPROVE_ENDURANCE = "improve_endurance"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"          # Little to no exercise
    LIGHT = "light"                  # Light exercise 1-3 days/week
    MODERATE = "moderate"            # Moderate exercise 3-5 days/week
    ACTIVE = "active"                # Hard exercise 6-7 days/week
    VERY_ACTIVE = "very_active"      # Very hard exercise & physical job


class DietPreference(str, Enum):
    BALANCED = "balanced"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    KETO = "keto"
    HIGH_PROTEIN = "high_protein"


class Equipment(str, Enum):
    GYM = "gym"
    HOME = "home"
    BODYWEIGHT = "bodyweight"


class UserProfile(BaseModel):
    age: int = Field(gt=0, le=120)
    weight: float = Field(gt=0, description="Weight in kg")
    height: float = Field(gt=0, description="Height in cm")
    gender: Gender
    activity_level: ActivityLevel
    goal: Goal
    diet_preference: DietPreference
    equipment: Equipment


class BMIResult(BaseModel):
    bmi: float
    category: str
    healthy_weight_range: dict


class CalorieResult(BaseModel):
    bmr: float
    tdee: float
    target_calories: float
    description: str


class MacroResult(BaseModel):
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    protein_calories: float
    carbs_calories: float
    fat_calories: float


class Exercise(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[str] = None
    duration: Optional[str] = None
    rest: str


class WorkoutDay(BaseModel):
    day: str
    focus: str
    exercises: List[Exercise]


class WorkoutPlan(BaseModel):
    goal: Goal
    equipment: Equipment
    weekly_schedule: List[WorkoutDay]
    notes: str


class Meal(BaseModel):
    name: str
    calories: int
    protein: float
    carbs: float
    fat: float


class DailyMealPlan(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snacks: List[Meal]
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fat: float


class FitnessResponse(BaseModel):
    profile: UserProfile
    bmi: BMIResult
    calories: CalorieResult
    macros: MacroResult
    workout_plan: WorkoutPlan
    meal_plan: DailyMealPlan
