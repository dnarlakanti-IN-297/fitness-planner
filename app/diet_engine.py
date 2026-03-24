from app.models import DietPreference, Meal, DailyMealPlan


# Food database with macros
MEALS = {
    "balanced": {
        "breakfast": [
            Meal(name="Oatmeal with berries and nuts", calories=350, protein=12, carbs=55, fat=10),
            Meal(name="Scrambled eggs with whole wheat toast", calories=400, protein=25, carbs=35, fat=18),
            Meal(name="Greek yogurt with granola and banana", calories=380, protein=20, carbs=52, fat=11)
        ],
        "lunch": [
            Meal(name="Grilled chicken salad with quinoa", calories=450, protein=35, carbs=40, fat=15),
            Meal(name="Turkey sandwich with avocado and veggies", calories=480, protein=30, carbs=45, fat=18),
            Meal(name="Salmon with brown rice and steamed broccoli", calories=520, protein=38, carbs=48, fat=18)
        ],
        "dinner": [
            Meal(name="Lean beef stir-fry with vegetables", calories=500, protein=40, carbs=45, fat=16),
            Meal(name="Baked chicken with sweet potato and green beans", calories=480, protein=42, carbs=50, fat=12),
            Meal(name="Shrimp pasta with marinara sauce", calories=520, protein=35, carbs=60, fat=14)
        ],
        "snacks": [
            Meal(name="Apple with almond butter", calories=200, protein=5, carbs=25, fat=10),
            Meal(name="Protein shake", calories=180, protein=25, carbs=15, fat=3),
            Meal(name="Mixed nuts (1 oz)", calories=170, protein=6, carbs=6, fat=15),
            Meal(name="Hummus with carrot sticks", calories=150, protein=5, carbs=18, fat=7)
        ]
    },
    "vegetarian": {
        "breakfast": [
            Meal(name="Vegetable omelet with toast", calories=380, protein=22, carbs=38, fat=16),
            Meal(name="Smoothie bowl with granola", calories=420, protein=15, carbs=65, fat=12),
            Meal(name="Whole grain pancakes with fruit", calories=400, protein=12, carbs=70, fat=8)
        ],
        "lunch": [
            Meal(name="Veggie burger with sweet potato fries", calories=480, protein=20, carbs=65, fat=16),
            Meal(name="Lentil soup with whole grain bread", calories=420, protein=22, carbs=58, fat=10),
            Meal(name="Chickpea curry with brown rice", calories=500, protein=18, carbs=75, fat=14)
        ],
        "dinner": [
            Meal(name="Vegetable stir-fry with tofu and quinoa", calories=480, protein=25, carbs=55, fat=16),
            Meal(name="Eggplant parmesan with side salad", calories=520, protein=20, carbs=60, fat=22),
            Meal(name="Black bean tacos with guacamole", calories=500, protein=18, carbs=65, fat=18)
        ],
        "snacks": [
            Meal(name="Greek yogurt with honey", calories=180, protein=15, carbs=25, fat=3),
            Meal(name="Trail mix", calories=200, protein=6, carbs=20, fat=12),
            Meal(name="Cheese and crackers", calories=190, protein=8, carbs=18, fat=10),
            Meal(name="Edamame", calories=120, protein=11, carbs=10, fat=5)
        ]
    },
    "vegan": {
        "breakfast": [
            Meal(name="Overnight oats with chia seeds and berries", calories=380, protein=12, carbs=60, fat=10),
            Meal(name="Tofu scramble with vegetables", calories=350, protein=20, carbs=30, fat=16),
            Meal(name="Acai bowl with granola", calories=420, protein=10, carbs=70, fat=12)
        ],
        "lunch": [
            Meal(name="Buddha bowl with tempeh", calories=500, protein=22, carbs=65, fat=16),
            Meal(name="Lentil and vegetable curry", calories=450, protein=18, carbs=70, fat=12),
            Meal(name="Quinoa salad with chickpeas", calories=480, protein=20, carbs=68, fat=14)
        ],
        "dinner": [
            Meal(name="Vegan chili with cornbread", calories=520, protein=20, carbs=78, fat=14),
            Meal(name="Pasta primavera with nutritional yeast", calories=500, protein=18, carbs=80, fat=12),
            Meal(name="Stir-fried tofu with vegetables and rice", calories=480, protein=24, carbs=65, fat=14)
        ],
        "snacks": [
            Meal(name="Banana with peanut butter", calories=220, protein=6, carbs=32, fat=10),
            Meal(name="Roasted chickpeas", calories=150, protein=8, carbs=22, fat=4),
            Meal(name="Fruit smoothie with plant protein", calories=200, protein=15, carbs=30, fat=3),
            Meal(name="Vegetable sticks with hummus", calories=140, protein=5, carbs=16, fat=7)
        ]
    },
    "keto": {
        "breakfast": [
            Meal(name="Eggs and bacon with avocado", calories=520, protein=30, carbs=8, fat=42),
            Meal(name="Keto smoothie with MCT oil", calories=400, protein=25, carbs=10, fat=30),
            Meal(name="Cheese omelet with spinach", calories=450, protein=28, carbs=6, fat=36)
        ],
        "lunch": [
            Meal(name="Grilled salmon with asparagus", calories=500, protein=40, carbs=8, fat=36),
            Meal(name="Chicken Caesar salad (no croutons)", calories=480, protein=38, carbs=10, fat=34),
            Meal(name="Bunless burger with cheese and side salad", calories=520, protein=35, carbs=12, fat=38)
        ],
        "dinner": [
            Meal(name="Ribeye steak with butter-roasted broccoli", calories=600, protein=45, carbs=10, fat=44),
            Meal(name="Pork chops with cauliflower mash", calories=550, protein=42, carbs=12, fat=38),
            Meal(name="Baked chicken thighs with zucchini noodles", calories=520, protein=40, carbs=10, fat=36)
        ],
        "snacks": [
            Meal(name="Cheese cubes", calories=150, protein=10, carbs=2, fat=12),
            Meal(name="Macadamia nuts", calories=200, protein=2, carbs=4, fat=22),
            Meal(name="Celery with cream cheese", calories=120, protein=3, carbs=3, fat=11),
            Meal(name="Hard-boiled eggs", calories=140, protein=12, carbs=2, fat=10)
        ]
    },
    "high_protein": {
        "breakfast": [
            Meal(name="Protein pancakes with Greek yogurt", calories=450, protein=40, carbs=45, fat=12),
            Meal(name="Egg white omelet with turkey bacon", calories=380, protein=45, carbs=20, fat=12),
            Meal(name="Protein shake with oats and banana", calories=420, protein=38, carbs=50, fat=8)
        ],
        "lunch": [
            Meal(name="Grilled chicken breast with quinoa", calories=520, protein=50, carbs=45, fat=12),
            Meal(name="Tuna salad with whole grain crackers", calories=480, protein=45, carbs=40, fat=14),
            Meal(name="Turkey meatballs with whole wheat pasta", calories=550, protein=48, carbs=52, fat=15)
        ],
        "dinner": [
            Meal(name="Grilled steak with sweet potato", calories=580, protein=52, carbs=48, fat=16),
            Meal(name="Baked cod with wild rice and vegetables", calories=500, protein=48, carbs=50, fat=10),
            Meal(name="Chicken stir-fry with brown rice", calories=540, protein=50, carbs=55, fat=12)
        ],
        "snacks": [
            Meal(name="Protein bar", calories=200, protein=20, carbs=22, fat=6),
            Meal(name="Cottage cheese with berries", calories=180, protein=22, carbs=18, fat=3),
            Meal(name="Turkey jerky", calories=120, protein=18, carbs=6, fat=3),
            Meal(name="Protein shake", calories=160, protein=25, carbs=10, fat=2)
        ]
    }
}


def generate_meal_plan(target_calories: float, diet_preference: DietPreference) -> DailyMealPlan:
    """Generate a daily meal plan based on calorie target and diet preference."""
    preference_key = diet_preference.value
    meals = MEALS[preference_key]

    # Simple selection - pick first option from each category
    breakfast = meals["breakfast"][0]
    lunch = meals["lunch"][0]
    dinner = meals["dinner"][0]

    # Calculate remaining calories for snacks
    main_meals_calories = breakfast.calories + lunch.calories + dinner.calories
    remaining_calories = target_calories - main_meals_calories

    # Select snacks to fill remaining calories
    selected_snacks = []
    snack_calories = 0

    for snack in meals["snacks"]:
        if snack_calories + snack.calories <= remaining_calories + 100:  # Allow 100 cal buffer
            selected_snacks.append(snack)
            snack_calories += snack.calories
            if len(selected_snacks) >= 2:  # Max 2 snacks
                break

    if not selected_snacks:  # If no snacks fit, add one anyway
        selected_snacks = [meals["snacks"][0]]
        snack_calories = meals["snacks"][0].calories

    # Calculate totals
    total_calories = breakfast.calories + lunch.calories + dinner.calories + snack_calories
    total_protein = breakfast.protein + lunch.protein + dinner.protein + sum(s.protein for s in selected_snacks)
    total_carbs = breakfast.carbs + lunch.carbs + dinner.carbs + sum(s.carbs for s in selected_snacks)
    total_fat = breakfast.fat + lunch.fat + dinner.fat + sum(s.fat for s in selected_snacks)

    return DailyMealPlan(
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        snacks=selected_snacks,
        total_calories=total_calories,
        total_protein=round(total_protein, 1),
        total_carbs=round(total_carbs, 1),
        total_fat=round(total_fat, 1)
    )
