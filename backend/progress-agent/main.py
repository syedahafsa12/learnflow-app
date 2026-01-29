from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from typing import Dict, Any, List
import datetime
import uuid
from enum import Enum

# Initialize FastAPI app
app = FastAPI(title="Progress Agent", description="Tracks student mastery and progress", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Topic(str, Enum):
    VARIABLES = "variables"
    LOOPS = "loops"
    FUNCTIONS = "functions"
    DATA_STRUCTURES = "data_structures"
    CLASSES = "classes"
    FILES = "files"
    ERRORS = "errors"
    LIBRARIES = "libraries"

class MasteryLevel(str, Enum):
    BEGINNER_LEVEL = "beginner"  # 0-40%
    LEARNING = "learning"  # 41-70%
    PROFICIENT = "proficient"  # 71-90%
    MASTERED = "mastered"  # 91-100%

class ProgressEvent(BaseModel):
    user_id: str
    topic: Topic
    event_type: str  # exercise_completed, quiz_taken, code_submitted, concept_learned
    score: float = None  # 0.0 to 1.0
    timestamp: datetime.datetime = datetime.datetime.now()
    metadata: Dict[str, Any] = {}

class ProgressUpdate(BaseModel):
    user_id: str
    topic: Topic
    mastery_percentage: float  # 0.0 to 1.0
    exercises_completed: int
    quizzes_taken: int
    code_quality_score: float  # 0.0 to 1.0
    consistency_streak: int  # Number of consecutive days active

class StudentProgress(BaseModel):
    user_id: str
    overall_mastery: float
    topic_mastery: Dict[Topic, float]
    exercises_completed: int
    quizzes_taken: int
    code_quality_average: float
    consistency_streak: int
    last_active: datetime.datetime
    mastery_levels: Dict[Topic, MasteryLevel]

class ProgressResponse(BaseModel):
    message: str
    progress: StudentProgress

# In-memory storage for progress data (would be replaced by database in production)
student_progress_db: Dict[str, StudentProgress] = {}

def calculate_mastery_score(progress: ProgressUpdate) -> float:
    """
    Calculate overall mastery based on the formula:
    Topic Mastery = weighted average of:
    - Exercise completion: 40%
    - Quiz scores: 30%
    - Code quality ratings: 20%
    - Consistency (streak): 10%
    """
    # Normalize inputs to 0-1 scale
    exercise_factor = min(progress.exercises_completed / 10.0, 1.0)  # Assuming 10 exercises = full credit
    quiz_factor = min(progress.quizzes_taken / 5.0, 1.0)  # Assuming 5 quizzes = full credit
    code_quality_factor = progress.code_quality_score
    consistency_factor = min(progress.consistency_streak / 7.0, 1.0)  # Assuming 7-day streak = full credit

    # Apply weights
    mastery_score = (
        exercise_factor * 0.4 +
        quiz_factor * 0.3 +
        code_quality_factor * 0.2 +
        consistency_factor * 0.1
    )

    return min(mastery_score, 1.0)  # Cap at 1.0

def get_mastery_level(score: float) -> MasteryLevel:
    """Convert numerical score to mastery level"""
    if 0.0 <= score <= 0.40:
        return MasteryLevel.BEGINNER_LEVEL
    elif 0.41 <= score <= 0.70:
        return MasteryLevel.LEARNING
    elif 0.71 <= score <= 0.90:
        return MasteryLevel.PROFICIENT
    elif 0.91 <= score <= 1.0:
        return MasteryLevel.MASTERED
    else:
        return MasteryLevel.BEGINNER_LEVEL  # Default fallback

def initialize_student_progress(user_id: str) -> StudentProgress:
    """Initialize progress data for a new student"""
    return StudentProgress(
        user_id=user_id,
        overall_mastery=0.0,
        topic_mastery={
            Topic.VARIABLES: 0.0,
            Topic.LOOPS: 0.0,
            Topic.FUNCTIONS: 0.0,
            Topic.DATA_STRUCTURES: 0.0,
            Topic.CLASSES: 0.0,
            Topic.FILES: 0.0,
            Topic.ERRORS: 0.0,
            Topic.LIBRARIES: 0.0
        },
        exercises_completed=0,
        quizzes_taken=0,
        code_quality_average=0.0,
        consistency_streak=0,
        last_active=datetime.datetime.now(),
        mastery_levels={
            Topic.VARIABLES: MasteryLevel.BEGINNER_LEVEL,
            Topic.LOOPS: MasteryLevel.BEGINNER_LEVEL,
            Topic.FUNCTIONS: MasteryLevel.BEGINNER_LEVEL,
            Topic.DATA_STRUCTURES: MasteryLevel.BEGINNER_LEVEL,
            Topic.CLASSES: MasteryLevel.BEGINNER_LEVEL,
            Topic.FILES: MasteryLevel.BEGINNER_LEVEL,
            Topic.ERRORS: MasteryLevel.BEGINNER_LEVEL,
            Topic.LIBRARIES: MasteryLevel.BEGINNER_LEVEL
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "progress-agent"}

@app.post("/event")
async def record_progress_event(event: ProgressEvent):
    """Record a progress event and update student's progress"""
    logger.info(f"Recording event for user {event.user_id}: {event.event_type}")

    # Get or initialize student progress
    if event.user_id not in student_progress_db:
        student_progress_db[event.user_id] = initialize_student_progress(event.user_id)

    progress = student_progress_db[event.user_id]

    # Update progress based on event type
    if event.event_type == "exercise_completed":
        if event.score is not None:
            progress.exercises_completed += 1
            # Update topic-specific mastery if score provided
            if event.topic:
                prev_score = progress.topic_mastery[event.topic]
                # Weighted average: new score contributes to topic mastery
                new_score = (prev_score * (progress.exercises_completed - 1) + event.score) / progress.exercises_completed
                progress.topic_mastery[event.topic] = new_score
    elif event.event_type == "quiz_taken":
        if event.score is not None:
            progress.quizzes_taken += 1
            # Update code quality average if score is related to code quality
            if "quality" in event.metadata:
                prev_avg = progress.code_quality_average
                new_avg = (prev_avg * (progress.quizzes_taken - 1) + event.score) / progress.quizzes_taken
                progress.code_quality_average = new_avg
    elif event.event_type == "code_submitted":
        if event.score is not None:
            # Update code quality score
            total_submissions = progress.quizzes_taken + 1  # Simplified calculation
            prev_avg = progress.code_quality_average
            new_avg = (prev_avg * (total_submissions - 1) + event.score) / total_submissions
            progress.code_quality_average = new_avg
    elif event.event_type == "struggle_detected":
        # Decrease consistency streak if struggling
        if progress.consistency_streak > 0:
            progress.consistency_streak = max(0, progress.consistency_streak - 1)

    # Update last active timestamp
    progress.last_active = event.timestamp

    # Calculate overall mastery
    progress.overall_mastery = calculate_mastery_score(
        ProgressUpdate(
            user_id=event.user_id,
            topic=event.topic if event.topic else Topic.VARIABLES,
            mastery_percentage=0.0,  # Will be calculated from other fields
            exercises_completed=progress.exercises_completed,
            quizzes_taken=progress.quizzes_taken,
            code_quality_score=progress.code_quality_average,
            consistency_streak=progress.consistency_streak
        )
    )

    # Update mastery levels for each topic
    for topic in Topic:
        progress.mastery_levels[topic] = get_mastery_level(progress.topic_mastery[topic])

    # Update overall mastery level based on overall mastery score
    overall_mastery_level = get_mastery_level(progress.overall_mastery)
    # Store in the first topic as a general indicator (in a real system, we'd have a separate field)

    return {"message": f"Event recorded successfully for user {event.user_id}", "event_id": str(uuid.uuid4())}

@app.get("/progress/{user_id}", response_model=StudentProgress)
async def get_student_progress(user_id: str):
    """Get progress information for a specific student"""
    logger.info(f"Retrieving progress for user {user_id}")

    if user_id not in student_progress_db:
        # Initialize if not exists
        student_progress_db[user_id] = initialize_student_progress(user_id)

    progress = student_progress_db[user_id]

    # Update consistency streak if it's been more than a day since last activity
    time_since_last_active = datetime.datetime.now() - progress.last_active
    if time_since_last_active.days > 1:
        # Reset streak if inactive for more than a day
        progress.consistency_streak = 0
    elif time_since_last_active.days == 1:
        # Increment streak if active yesterday
        progress.consistency_streak += 1

    return progress

@app.get("/mastery/{user_id}/{topic}", response_model=dict)
async def get_topic_mastery(user_id: str, topic: Topic):
    """Get mastery information for a specific topic"""
    logger.info(f"Retrieving {topic} mastery for user {user_id}")

    if user_id not in student_progress_db:
        student_progress_db[user_id] = initialize_student_progress(user_id)

    progress = student_progress_db[user_id]

    mastery_percentage = progress.topic_mastery[topic]
    mastery_level = progress.mastery_levels[topic]

    # Calculate progress toward next level
    next_level_thresholds = {
        MasteryLevel.BEGINNER_LEVEL: 0.40,
        MasteryLevel.LEARNING: 0.70,
        MasteryLevel.PROFICIENT: 0.90,
        MasteryLevel.MASTERED: 1.0
    }

    current_threshold = 0.0
    if mastery_level == MasteryLevel.BEGINNER_LEVEL:
        current_threshold = 0.0
    elif mastery_level == MasteryLevel.LEARNING:
        current_threshold = 0.41
    elif mastery_level == MasteryLevel.PROFICIENT:
        current_threshold = 0.71
    elif mastery_level == MasteryLevel.MASTERED:
        current_threshold = 0.91

    progress_to_next = ((mastery_percentage - current_threshold) /
                       (next_level_thresholds[mastery_level] - current_threshold)) if next_level_thresholds[mastery_level] > current_threshold else 0.0

    return {
        "user_id": user_id,
        "topic": topic,
        "mastery_percentage": mastery_percentage,
        "mastery_level": mastery_level,
        "progress_to_next_level": progress_to_next,
        "exercises_completed_in_topic": progress.exercises_completed,  # Simplified
        "recommendations": get_recommendations_for_topic(topic, mastery_level)
    }

def get_recommendations_for_topic(topic: Topic, mastery_level: MasteryLevel) -> List[str]:
    """Provide recommendations based on topic and mastery level"""
    recommendations = []

    if mastery_level in [MasteryLevel.BEGINNER_LEVEL, MasteryLevel.LEARNING]:
        recommendations.append(f"Focus on foundational concepts in {topic.value}")
        recommendations.append("Complete more exercises to build understanding")
        recommendations.append("Review examples and documentation")
    elif mastery_level == MasteryLevel.PROFICIENT:
        recommendations.append(f"You're proficient in {topic.value}. Try more challenging exercises")
        recommendations.append("Apply concepts in real-world scenarios")
        recommendations.append("Help others to reinforce your knowledge")
    elif mastery_level == MasteryLevel.MASTERED:
        recommendations.append(f"Congratulations! You've mastered {topic.value}")
        recommendations.append("Consider mentoring others")
        recommendations.append("Move on to advanced topics or projects")

    return recommendations

@app.get("/leaderboard")
async def get_leaderboard():
    """Get top students based on overall mastery"""
    if not student_progress_db:
        return {"leaderboard": []}

    # Sort students by overall mastery
    sorted_students = sorted(
        student_progress_db.items(),
        key=lambda x: x[1].overall_mastery,
        reverse=True
    )

    leaderboard = []
    for i, (user_id, progress) in enumerate(sorted_students[:10]):  # Top 10
        leaderboard.append({
            "rank": i + 1,
            "user_id": user_id,
            "overall_mastery": progress.overall_mastery,
            "exercises_completed": progress.exercises_completed,
            "consistency_streak": progress.consistency_streak
        })

    return {"leaderboard": leaderboard}

@app.post("/reset/{user_id}")
async def reset_student_progress(user_id: str):
    """Reset a student's progress (for testing purposes)"""
    if user_id in student_progress_db:
        del student_progress_db[user_id]
        return {"message": f"Progress for user {user_id} has been reset"}
    else:
        # Initialize with default values
        student_progress_db[user_id] = initialize_student_progress(user_id)
        return {"message": f"Initialized progress for user {user_id}"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8003))
    uvicorn.run(app, host="0.0.0.0", port=port)