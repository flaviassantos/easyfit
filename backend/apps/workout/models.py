from typing import Optional
import uuid
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field


class ExerciseModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    completed: bool = False
    date_added: str = Field(default_factory=datetime.utcnow)
    number_sets: int = Field(default=0)
    rep_per_set: int = Field(default=0)
    kg_per_set: Optional[float] = None
    # TODO cal_burned: Optional[float] = None
    # TODO add heart_rate_zones: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True, json_schema_extra={
        "example": {
            "id": "08890203-0905-0907-0879-0a0b3c0d0e0f",
            "name": "Crunches",
            "completed": False,
            "date_added": '2023-09-12T12:05:29.351031',
            "number_sets": 3,
            "rep_per_set": 8,
            "kg_per_set": 2.5
        }
    })


class UpdateExerciseModel(BaseModel):
    name: Optional[str] = None
    completed: Optional[bool] = None
    number_sets: Optional[int] = None
    rep_per_set: Optional[int] = None
    kg_per_set: Optional[float] = None
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Crunches",
            "completed": True,
            "number_sets": 3,
            "rep_per_set": 8,
            "kg_per_set": 2.8
        }
    })
