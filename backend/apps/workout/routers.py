from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import ExerciseModel, UpdateExerciseModel

router = APIRouter()


@router.post("/", response_description="Add new exercise")
async def create_exercise(request: Request, exercise: ExerciseModel = Body(...)):
    exercise = jsonable_encoder(exercise)
    new_exercise = await request.app.mongodb["exercises"].insert_one(exercise)
    created_exercise = await request.app.mongodb["exercises"].find_one(
        {"_id": new_exercise.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=created_exercise)


@router.get("/", response_description="List all exercises")
async def list_exercises(request: Request):
    exercises = []
    for doc in await request.app.mongodb["exercises"].find().to_list(length=100):
        exercises.append(doc)
    return exercises


@router.get("/{id}", response_description="Get a single exercise")
async def show_exercise(id: str, request: Request):
    if (exercise := await request.app.mongodb["exercises"].find_one({"_id": id})) is not None:
        return exercise

    raise HTTPException(status_code=404, detail=f"Exercise {id} not found")


@router.put("/{id}", response_description="Update a exercise")
async def update_exercise(id: str, request: Request, exercise: UpdateExerciseModel = Body(...)):
    exercise = {k: v for k, v in exercise.dict().items() if v is not None}

    if len(exercise) >= 1:
        update_result = await request.app.mongodb["exercises"].update_one(
            {"_id": id}, {"$set": exercise}
        )

        if update_result.modified_count == 1:
            if (
                updated_exercise := await request.app.mongodb["exercises"].find_one({"_id": id})
            ) is not None:
                return updated_exercise

    if (
        existing_exercise := await request.app.mongodb["exercises"].find_one({"_id": id})
    ) is not None:
        return existing_exercise

    raise HTTPException(status_code=404, detail=f"Exercise {id} not found")


@router.delete("/{id}", response_description="Delete Exercise")
async def delete_exercise(id: str, request: Request):
    delete_result = await request.app.mongodb["exercises"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Exercise {id} not found")
