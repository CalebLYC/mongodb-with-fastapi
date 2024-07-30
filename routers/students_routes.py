from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Response, status
from pymongo import ReturnDocument

from models.student import StudentCollection, StudentModel, UpdateStudentModel
from config.database import db
from repositories import students_repository


router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)
student_collection = db.get_collection("students")

@router.post(
    "/",
    response_description="Add new student",
    response_model=StudentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_student(student: StudentModel = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    return await students_repository.create_student(student=student, student_collection=student_collection)


@router.get(
    "/",
    response_description="List all students",
    response_model=StudentCollection,
    response_model_by_alias=False,
)
async def list_students():
    """
    List all of the student data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return await students_repository.list_students(student_collection=student_collection)


@router.get(
    "/{id}",
    response_description="Get a single student",
    response_model=StudentModel,
    response_model_by_alias=False,
)
async def show_student(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    student = await students_repository.get_student(student_collection=student_collection, id=id)
    if student is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.put(
    "/{id}",
    response_description="Update a student",
    response_model=StudentModel,
    response_model_by_alias=False,
)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    return await students_repository.update_student(id=id, student=student, student_collection=student_collection)


@router.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    """
    Remove a single student record from the database.
    """
    return await students_repository.delete_student(id=id, student_collection=student_collection)