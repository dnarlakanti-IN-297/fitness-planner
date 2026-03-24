import pytest
from app.workout_engine import generate_workout_plan
from app.models import Goal, Equipment


def test_generate_workout_plan_weight_loss():
    """Test workout plan generation for weight loss."""
    plan = generate_workout_plan(Goal.LOSE_WEIGHT, Equipment.BODYWEIGHT)
    assert plan.goal == Goal.LOSE_WEIGHT
    assert plan.equipment == Equipment.BODYWEIGHT
    assert len(plan.weekly_schedule) == 7
    assert all(day.day for day in plan.weekly_schedule)
    assert all(day.exercises for day in plan.weekly_schedule)


def test_generate_workout_plan_muscle_gain():
    """Test workout plan generation for muscle gain."""
    plan = generate_workout_plan(Goal.GAIN_MUSCLE, Equipment.GYM)
    assert plan.goal == Goal.GAIN_MUSCLE
    assert plan.equipment == Equipment.GYM
    assert len(plan.weekly_schedule) == 7


def test_generate_workout_plan_endurance():
    """Test workout plan generation for endurance."""
    plan = generate_workout_plan(Goal.IMPROVE_ENDURANCE, Equipment.HOME)
    assert plan.goal == Goal.IMPROVE_ENDURANCE
    assert len(plan.weekly_schedule) == 7


def test_workout_plan_has_rest_days():
    """Test that workout plans include rest days."""
    plan = generate_workout_plan(Goal.MAINTAIN, Equipment.BODYWEIGHT)
    rest_days = [day for day in plan.weekly_schedule if "rest" in day.focus.lower()]
    assert len(rest_days) > 0


def test_exercises_have_required_fields():
    """Test that exercises have proper structure."""
    plan = generate_workout_plan(Goal.LOSE_WEIGHT, Equipment.GYM)
    for day in plan.weekly_schedule:
        for exercise in day.exercises:
            assert exercise.name
            assert exercise.rest is not None
