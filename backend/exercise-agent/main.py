from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Dict, Any, List
import random
import json
import re

# Initialize FastAPI app
app = FastAPI(title="Exercise Agent", description="Generates and auto-grades coding challenges", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExerciseRequest(BaseModel):
    topic: str
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    user_context: Dict[str, Any] = {}

class ExerciseSubmission(BaseModel):
    exercise_id: str
    user_solution: str
    user_context: Dict[str, Any] = {}

class Exercise(BaseModel):
    id: str
    title: str
    description: str
    starter_code: str
    difficulty: str
    topic: str
    hints: List[str]
    test_cases: List[Dict[str, Any]]

class GradeResult(BaseModel):
    exercise_id: str
    passed: bool
    score: float
    feedback: str
    detailed_feedback: List[str]

class ExerciseResponse(BaseModel):
    exercise: Exercise
    message: str = "Exercise generated successfully"

# Sample exercise database
EXERCISE_DATABASE = {
    "variables": [
        {
            "id": "var-001",
            "title": "Variable Assignment Practice",
            "description": "Create variables to store your name, age, and favorite color. Print a sentence using these variables.",
            "starter_code": "# TODO: Create variables for name, age, and favorite_color\n# Then print a sentence using these variables\n",
            "difficulty": "beginner",
            "topic": "variables",
            "hints": [
                "Use meaningful variable names",
                "Remember to use quotes for string values",
                "Use f-strings for printing variables in sentences"
            ],
            "test_cases": [
                {"input": "", "expected_output_pattern": r".*Alice.*25.*blue.*"},
                {"input": "", "expected_output_pattern": r".*[Nn]ame|[Aa]ge|[Cc]olor.*"}
            ]
        },
        {
            "id": "var-002",
            "title": "Swap Two Variables",
            "description": "Write a function that swaps the values of two variables without using a temporary variable.",
            "starter_code": "def swap_variables(a, b):\n    # TODO: Swap a and b without using a temporary variable\n    pass\n",
            "difficulty": "intermediate",
            "topic": "variables",
            "hints": [
                "Consider using tuple unpacking",
                "Python allows multiple assignment in one line"
            ],
            "test_cases": [
                {"input": "(5, 10)", "expected_output": [10, 5]},
                {"input": "('hello', 'world')", "expected_output": ['world', 'hello']}
            ]
        }
    ],
    "loops": [
        {
            "id": "loop-001",
            "title": "Simple For Loop",
            "description": "Write a for loop that prints the numbers 1 through 10.",
            "starter_code": "# TODO: Write a for loop to print numbers 1 through 10\n",
            "difficulty": "beginner",
            "topic": "loops",
            "hints": [
                "Use the range() function",
                "Remember that range is exclusive of the end value"
            ],
            "test_cases": [
                {"expected_output_pattern": r"1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n?"},
                {"expected_output_pattern": r"(1.*2.*3.*4.*5.*6.*7.*8.*9.*10)"}
            ]
        },
        {
            "id": "loop-002",
            "title": "Sum of Numbers",
            "description": "Write a function that calculates the sum of all numbers in a list using a loop.",
            "starter_code": "def sum_numbers(numbers):\n    # TODO: Calculate the sum of numbers in the list using a loop\n    total = 0\n    # Your code here\n    return total\n",
            "difficulty": "intermediate",
            "topic": "loops",
            "hints": [
                "Initialize a variable to store the running total",
                "Iterate through each number in the list",
                "Add each number to the running total"
            ],
            "test_cases": [
                {"input": "[1, 2, 3, 4, 5]", "expected_output": 15},
                {"input": "[10, -5, 3]", "expected_output": 8},
                {"input": "[]", "expected_output": 0}
            ]
        }
    ],
    "functions": [
        {
            "id": "func-001",
            "title": "Temperature Converter",
            "description": "Write a function that converts Celsius to Fahrenheit.",
            "starter_code": "def celsius_to_fahrenheit(celsius):\n    # TODO: Convert Celsius to Fahrenheit\n    # Formula: (celsius * 9/5) + 32\n    pass\n",
            "difficulty": "beginner",
            "topic": "functions",
            "hints": [
                "Use the formula: (celsius * 9/5) + 32",
                "Remember operator precedence"
            ],
            "test_cases": [
                {"input": 0, "expected_output": 32},
                {"input": 100, "expected_output": 212},
                {"input": -40, "expected_output": -40}
            ]
        },
        {
            "id": "func-002",
            "title": "Palindrome Checker",
            "description": "Write a function that checks if a string is a palindrome (reads the same forwards and backwards).",
            "starter_code": "def is_palindrome(text):\n    # TODO: Check if text is a palindrome\n    # Ignore spaces, punctuation, and case\n    pass\n",
            "difficulty": "intermediate",
            "topic": "functions",
            "hints": [
                "First clean the string: remove non-alphanumeric characters and convert to lowercase",
                "Compare the string with its reverse",
                "You can reverse a string with slicing: text[::-1]"
            ],
            "test_cases": [
                {"input": "'racecar'", "expected_output": True},
                {"input": "'A man a plan a canal Panama'", "expected_output": True},
                {"input": "'hello'", "expected_output": False}
            ]
        }
    ]
}

def execute_user_code(code: str, function_name: str, test_input) -> Any:
    """Execute user code safely and return the result"""
    try:
        # Create a local namespace to execute the code
        local_namespace = {}

        # Execute the user code
        exec(code, {}, local_namespace)

        # Get the function from the local namespace
        if function_name in local_namespace:
            func = local_namespace[function_name]

            # Call the function with the test input
            if isinstance(test_input, tuple):
                return func(*test_input)
            else:
                return func(test_input)
        else:
            raise Exception(f"Function '{function_name}' not found in submitted code")
    except Exception as e:
        raise Exception(f"Execution error: {str(e)}")

def grade_exercise_solution(exercise_id: str, user_solution: str) -> GradeResult:
    """Grade a user's exercise solution"""
    # Find the exercise
    exercise = None
    for topic, exercises in EXERCISE_DATABASE.items():
        for ex in exercises:
            if ex["id"] == exercise_id:
                exercise = ex
                break
        if exercise:
            break

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Extract function name from the exercise ID to determine which function to call
    function_name = ""
    if "swap_variables" in user_solution:
        function_name = "swap_variables"
    elif "sum_numbers" in user_solution:
        function_name = "sum_numbers"
    elif "celsius_to_fahrenheit" in user_solution:
        function_name = "celsius_to_fahrenheit"
    elif "is_palindrome" in user_solution:
        function_name = "is_palindrome"
    elif "temperature" in exercise_id.lower():
        function_name = "celsius_to_fahrenheit"
    elif "palindrome" in exercise_id.lower():
        function_name = "is_palindrome"
    elif "sum" in exercise_id.lower():
        function_name = "sum_numbers"
    elif "swap" in exercise_id.lower():
        function_name = "swap_variables"

    feedback_messages = []
    passed_tests = 0
    total_tests = len(exercise["test_cases"])

    for i, test_case in enumerate(exercise["test_cases"]):
        try:
            expected = test_case.get("expected_output")
            expected_pattern = test_case.get("expected_output_pattern")
            test_input = test_case.get("input")

            # Execute the user's solution
            result = execute_user_code(user_solution, function_name, test_input)

            # Check result against expected value or pattern
            test_passed = False
            if expected is not None:
                test_passed = result == expected
            elif expected_pattern:
                import re
                test_passed = bool(re.search(expected_pattern, str(result)))

            if test_passed:
                passed_tests += 1
            else:
                feedback_messages.append(f"Test {i+1} failed: Expected {expected or expected_pattern}, got {result}")

        except Exception as e:
            feedback_messages.append(f"Test {i+1} caused an error: {str(e)}")

    # Calculate score
    score = passed_tests / total_tests if total_tests > 0 else 0

    # Overall feedback
    if score == 1.0:
        feedback = "Excellent! All test cases passed."
    elif score >= 0.7:
        feedback = f"Well done! {passed_tests}/{total_tests} tests passed."
    elif score > 0:
        feedback = f"Good effort! {passed_tests}/{total_tests} tests passed. Check the feedback below."
    else:
        feedback = f"Keep trying! {passed_tests}/{total_tests} tests passed. Review the feedback."

    return GradeResult(
        exercise_id=exercise_id,
        passed=score == 1.0,
        score=score,
        feedback=feedback,
        detailed_feedback=feedback_messages
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "exercise-agent"}

@app.post("/generate", response_model=ExerciseResponse)
async def generate_exercise(request: ExerciseRequest):
    """
    Generate a coding exercise based on topic and difficulty
    """
    topic = request.topic.lower()
    difficulty = request.difficulty.lower()

    logger.info(f"Generating exercise for topic: {topic}, difficulty: {difficulty}")

    # Find exercises matching the topic
    topic_exercises = EXERCISE_DATABASE.get(topic, [])

    if not topic_exercises:
        # If no exercises for the specific topic, pick a random one
        all_exercises = []
        for exercises in EXERCISE_DATABASE.values():
            all_exercises.extend(exercises)

        if all_exercises:
            selected_exercise = random.choice(all_exercises)
        else:
            # If no exercises at all, return a default one
            default_exercise = Exercise(
                id="default-001",
                title="Introduction to Python",
                description="Write a simple program that prints 'Hello, World!'",
                starter_code="print('')  # Replace with your code\n",
                difficulty="beginner",
                topic="introduction",
                hints=["Use the print() function", "Remember to put text in quotes"],
                test_cases=[{"expected_output_pattern": r"Hello,? World!?!"}]
            )
            return ExerciseResponse(
                exercise=default_exercise,
                message="No exercises available for this topic. Here's a basic one to start."
            )
    else:
        # Filter by difficulty if specified
        if difficulty != "any":
            difficulty_exercises = [ex for ex in topic_exercises if ex["difficulty"] == difficulty]
            if difficulty_exercises:
                selected_exercise = random.choice(difficulty_exercises)
            else:
                # If no exercises of requested difficulty, pick from all available for topic
                selected_exercise = random.choice(topic_exercises)
        else:
            selected_exercise = random.choice(topic_exercises)

    # Convert dict to Exercise model
    exercise = Exercise(**selected_exercise)

    logger.info(f"Generated exercise: {exercise.id}")

    return ExerciseResponse(
        exercise=exercise,
        message=f"Exercise generated for {topic} at {difficulty} level"
    )

@app.post("/grade", response_model=GradeResult)
async def grade_exercise(submission: ExerciseSubmission):
    """
    Grade a user's exercise submission
    """
    logger.info(f"Grading submission for exercise: {submission.exercise_id}")

    try:
        result = grade_exercise_solution(submission.exercise_id, submission.user_solution)
        logger.info(f"Grading completed with score: {result.score}")
        return result
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Grading error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")

@app.get("/topics")
async def list_topics():
    """List all available exercise topics"""
    return {"topics": list(EXERCISE_DATABASE.keys())}

@app.get("/exercises/{topic}")
async def list_exercises_by_topic(topic: str):
    """List all exercises for a specific topic"""
    if topic not in EXERCISE_DATABASE:
        raise HTTPException(status_code=404, detail="Topic not found")

    exercises = EXERCISE_DATABASE[topic]
    return {"topic": topic, "exercises": exercises, "count": len(exercises)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)