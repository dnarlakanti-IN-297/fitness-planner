from app.models import Goal, Equipment, WorkoutPlan, WorkoutDay, Exercise
from typing import List


# Exercise database
EXERCISES = {
    "bodyweight": {
        "upper": ["Push-ups", "Diamond Push-ups", "Pike Push-ups", "Pull-ups", "Chin-ups", "Dips"],
        "lower": ["Squats", "Lunges", "Bulgarian Split Squats", "Jump Squats", "Calf Raises"],
        "core": ["Plank", "Side Plank", "Mountain Climbers", "Bicycle Crunches", "Leg Raises"],
        "cardio": ["Burpees", "High Knees", "Jumping Jacks", "Mountain Climbers", "Jump Rope"]
    },
    "home": {
        "upper": ["Dumbbell Press", "Dumbbell Rows", "Dumbbell Curls", "Tricep Extensions", "Lateral Raises"],
        "lower": ["Goblet Squats", "Romanian Deadlifts", "Dumbbell Lunges", "Step-ups", "Calf Raises"],
        "core": ["Weighted Crunches", "Russian Twists", "Plank", "Dead Bug", "Bird Dog"],
        "cardio": ["Jump Rope", "Burpees", "Mountain Climbers", "High Knees"]
    },
    "gym": {
        "upper": ["Bench Press", "Barbell Rows", "Overhead Press", "Lat Pulldown", "Dumbbell Flyes"],
        "lower": ["Barbell Squats", "Deadlifts", "Leg Press", "Leg Curls", "Leg Extensions"],
        "core": ["Cable Crunches", "Hanging Leg Raises", "Ab Wheel", "Pallof Press", "Russian Twists"],
        "cardio": ["Treadmill", "Rowing Machine", "Stationary Bike", "Stair Climber"]
    }
}

# Premium exercise database (advanced/specialized exercises)
PREMIUM_EXERCISES = {
    "bodyweight": {
        "upper": ["Archer Push-ups", "One-Arm Push-ups", "Muscle-ups", "Front Lever Progressions", "Handstand Push-ups", "Ring Dips"],
        "lower": ["Pistol Squats", "Nordic Curls", "Single-Leg Box Jumps", "Dragon Flags", "Shrimp Squats"],
        "core": ["Dragon Flags", "L-Sits", "Human Flag Progressions", "Hanging Windshield Wipers", "Hollow Body Holds"],
        "cardio": ["Sprint Intervals", "Tabata Burpees", "Box Jump HIIT", "Battle Ropes", "Assault Bike Sprints"]
    },
    "home": {
        "upper": ["Single-Arm Dumbbell Press", "Renegade Rows", "Incline/Decline Dumbbell Press", "Zottman Curls", "Arnold Press"],
        "lower": ["Bulgarian Split Squat (Elevated)", "Single-Leg RDLs", "Dumbbell Thrusters", "Goblet Squat Pulses", "Tempo Squats"],
        "core": ["Turkish Get-ups", "Dumbbell Windmills", "Loaded Carries", "Overhead Carries", "Suitcase Carries"],
        "cardio": ["EMOM Burpees", "Dumbbell Complexes", "Metabolic Conditioning", "Tabata Training"]
    },
    "gym": {
        "upper": ["Incline Bench Press", "Pendlay Rows", "Close-Grip Bench", "Face Pulls", "Cable Flyes", "Weighted Dips"],
        "lower": ["Front Squats", "Sumo Deadlifts", "Hack Squats", "Walking Lunges", "Bulgarian Split Squats", "Hip Thrusts"],
        "core": ["Weighted Planks", "Anti-Rotation Press", "TRX Fallouts", "Landmine Rotations", "GHD Sit-ups"],
        "cardio": ["Assault Bike", "Sled Push/Pull", "Battle Ropes", "Rowing Intervals", "Ski Erg"]
    }
}


def generate_workout_plan(goal: Goal, equipment: Equipment, premium: bool = False) -> WorkoutPlan:
    """Generate a weekly workout plan based on goal and equipment."""
    equipment_key = equipment.value

    if goal == Goal.LOSE_WEIGHT:
        plan = _generate_weight_loss_plan(equipment_key, premium)
    elif goal == Goal.GAIN_MUSCLE:
        plan = _generate_muscle_gain_plan(equipment_key, premium)
    elif goal == Goal.MAINTAIN:
        plan = _generate_maintenance_plan(equipment_key, premium)
    else:  # IMPROVE_ENDURANCE
        plan = _generate_endurance_plan(equipment_key, premium)

    notes = "Rest for 48 hours between working the same muscle group. Stay hydrated and listen to your body."
    if premium:
        notes += " 🌟 Premium plan with advanced exercises - ensure proper form and consider working with a trainer."

    return WorkoutPlan(
        goal=goal,
        equipment=equipment,
        weekly_schedule=plan,
        notes=notes
    )


def _generate_weight_loss_plan(equipment: str, premium: bool = False) -> List[WorkoutDay]:
    """Weight loss focuses on cardio with strength training."""
    exercises = PREMIUM_EXERCISES[equipment] if premium else EXERCISES[equipment]

    return [
        WorkoutDay(
            day="Monday",
            focus="Full Body + Cardio",
            exercises=[
                Exercise(name=exercises["upper"][0], sets=3, reps="12-15", rest="60s"),
                Exercise(name=exercises["lower"][0], sets=3, reps="15-20", rest="60s"),
                Exercise(name=exercises["core"][0], sets=3, duration="45s", rest="30s"),
                Exercise(name=exercises["cardio"][0], duration="20 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Tuesday",
            focus="Cardio & Core",
            exercises=[
                Exercise(name=exercises["cardio"][1], duration="30 minutes", rest=""),
                Exercise(name=exercises["core"][1], sets=3, duration="30s each side", rest="30s"),
                Exercise(name=exercises["core"][2], sets=3, reps="15-20", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Wednesday",
            focus="Rest or Light Activity",
            exercises=[
                Exercise(name="Walking or Stretching", duration="30 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Thursday",
            focus="Full Body + Cardio",
            exercises=[
                Exercise(name=exercises["upper"][1], sets=3, reps="12-15", rest="60s"),
                Exercise(name=exercises["lower"][1], sets=3, reps="12-15 each leg", rest="60s"),
                Exercise(name=exercises["core"][3], sets=3, reps="20", rest="30s"),
                Exercise(name=exercises["cardio"][2], duration="20 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Friday",
            focus="HIIT Cardio",
            exercises=[
                Exercise(name=exercises["cardio"][0], duration="30s", rest="30s", sets=8, reps="rounds"),
                Exercise(name=exercises["cardio"][1], duration="30s", rest="30s", sets=8, reps="rounds"),
                Exercise(name=exercises["core"][4], sets=3, reps="12-15", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Saturday",
            focus="Active Recovery",
            exercises=[
                Exercise(name="Yoga or Swimming", duration="30-45 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Sunday",
            focus="Rest",
            exercises=[
                Exercise(name="Complete rest day", duration="", rest="")
            ]
        )
    ]


def _generate_muscle_gain_plan(equipment: str, premium: bool = False) -> List[WorkoutDay]:
    """Muscle gain focuses on strength training with progressive overload."""
    exercises = PREMIUM_EXERCISES[equipment] if premium else EXERCISES[equipment]

    return [
        WorkoutDay(
            day="Monday",
            focus="Upper Body - Push",
            exercises=[
                Exercise(name=exercises["upper"][0], sets=4, reps="8-12", rest="90s"),
                Exercise(name=exercises["upper"][2], sets=4, reps="8-12", rest="90s"),
                Exercise(name=exercises["upper"][4], sets=3, reps="10-15", rest="60s"),
                Exercise(name=exercises["core"][0], sets=3, duration="45s", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Tuesday",
            focus="Lower Body",
            exercises=[
                Exercise(name=exercises["lower"][0], sets=4, reps="8-12", rest="2min"),
                Exercise(name=exercises["lower"][1], sets=4, reps="10-12", rest="90s"),
                Exercise(name=exercises["lower"][2], sets=3, reps="12-15 each leg", rest="60s"),
                Exercise(name=exercises["lower"][4], sets=4, reps="15-20", rest="60s")
            ]
        ),
        WorkoutDay(
            day="Wednesday",
            focus="Rest or Light Cardio",
            exercises=[
                Exercise(name="Walking or Light Cycling", duration="20-30 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Thursday",
            focus="Upper Body - Pull",
            exercises=[
                Exercise(name=exercises["upper"][1], sets=4, reps="8-12", rest="90s"),
                Exercise(name=exercises["upper"][3], sets=4, reps="8-12", rest="90s"),
                Exercise(name=exercises["upper"][5] if len(exercises["upper"]) > 5 else exercises["upper"][1], sets=3, reps="10-15", rest="60s"),
                Exercise(name=exercises["core"][1], sets=3, duration="30s each side", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Friday",
            focus="Lower Body",
            exercises=[
                Exercise(name=exercises["lower"][1], sets=4, reps="8-12", rest="2min"),
                Exercise(name=exercises["lower"][3], sets=4, reps="10-12", rest="90s"),
                Exercise(name=exercises["lower"][0], sets=3, reps="12-15", rest="60s"),
                Exercise(name=exercises["core"][2], sets=3, reps="15", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Saturday",
            focus="Active Recovery",
            exercises=[
                Exercise(name="Stretching or Yoga", duration="30 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Sunday",
            focus="Rest",
            exercises=[
                Exercise(name="Complete rest day", duration="", rest="")
            ]
        )
    ]


def _generate_maintenance_plan(equipment: str, premium: bool = False) -> List[WorkoutDay]:
    """Maintenance plan balances strength and cardio."""
    exercises = PREMIUM_EXERCISES[equipment] if premium else EXERCISES[equipment]

    return [
        WorkoutDay(
            day="Monday",
            focus="Upper Body",
            exercises=[
                Exercise(name=exercises["upper"][0], sets=3, reps="10-12", rest="60s"),
                Exercise(name=exercises["upper"][1], sets=3, reps="10-12", rest="60s"),
                Exercise(name=exercises["core"][0], sets=3, duration="45s", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Tuesday",
            focus="Cardio",
            exercises=[
                Exercise(name=exercises["cardio"][0], duration="30 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Wednesday",
            focus="Lower Body",
            exercises=[
                Exercise(name=exercises["lower"][0], sets=3, reps="12-15", rest="90s"),
                Exercise(name=exercises["lower"][1], sets=3, reps="10-12 each leg", rest="60s"),
                Exercise(name=exercises["core"][1], sets=3, duration="30s each side", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Thursday",
            focus="Rest or Light Activity",
            exercises=[
                Exercise(name="Walking or Stretching", duration="20-30 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Friday",
            focus="Full Body",
            exercises=[
                Exercise(name=exercises["upper"][2], sets=3, reps="10-12", rest="60s"),
                Exercise(name=exercises["lower"][2], sets=3, reps="12 each leg", rest="60s"),
                Exercise(name=exercises["core"][2], sets=3, reps="15", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Saturday",
            focus="Cardio",
            exercises=[
                Exercise(name=exercises["cardio"][1], duration="25 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Sunday",
            focus="Rest",
            exercises=[
                Exercise(name="Complete rest day", duration="", rest="")
            ]
        )
    ]


def _generate_endurance_plan(equipment: str, premium: bool = False) -> List[WorkoutDay]:
    """Endurance plan focuses on cardio and stamina building."""
    exercises = PREMIUM_EXERCISES[equipment] if premium else EXERCISES[equipment]

    return [
        WorkoutDay(
            day="Monday",
            focus="Long Steady Cardio",
            exercises=[
                Exercise(name=exercises["cardio"][0], duration="45 minutes", rest="")
            ]
        ),
        WorkoutDay(
            day="Tuesday",
            focus="Strength Circuit",
            exercises=[
                Exercise(name=exercises["upper"][0], sets=3, reps="15-20", rest="30s"),
                Exercise(name=exercises["lower"][0], sets=3, reps="20", rest="30s"),
                Exercise(name=exercises["core"][0], sets=3, duration="60s", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Wednesday",
            focus="Interval Training",
            exercises=[
                Exercise(name=exercises["cardio"][1], duration="1min", rest="1min", sets=10, reps="intervals")
            ]
        ),
        WorkoutDay(
            day="Thursday",
            focus="Recovery Run/Cardio",
            exercises=[
                Exercise(name=exercises["cardio"][2], duration="30 minutes easy pace", rest="")
            ]
        ),
        WorkoutDay(
            day="Friday",
            focus="Tempo Cardio",
            exercises=[
                Exercise(name=exercises["cardio"][0], duration="40 minutes moderate pace", rest="")
            ]
        ),
        WorkoutDay(
            day="Saturday",
            focus="Long Endurance Session",
            exercises=[
                Exercise(name=exercises["cardio"][3], duration="60 minutes", rest=""),
                Exercise(name=exercises["core"][1], sets=3, duration="45s each side", rest="30s")
            ]
        ),
        WorkoutDay(
            day="Sunday",
            focus="Rest",
            exercises=[
                Exercise(name="Complete rest day or gentle yoga", duration="", rest="")
            ]
        )
    ]
