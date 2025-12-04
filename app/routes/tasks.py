from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_bd
from app import models, schemas
from app.utils import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

#obtener todas las tareas (protegido)
@router.get("/", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_bd), current_user: models.User= Depends(get_current_user)):
    tasks = db.query(models.Task).all()
    return tasks


#crear una nueva tarea (protegida)
@router.post("/", response_model= schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_bd), current_user: models.User = Depends(get_current_user)):
    new_task= models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#actualizar una tarea (protegida)
@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, 
    update_task: schemas.TaskCreate, 
    db: Session = Depends(get_bd), 
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=400, detail="Tarea no encontrada")
    for key, value in update_task.model_dump().items():
        setattr(task,key,value)
    db.commit()
    db.refresh(task)
    return task

#Eliminar tarea (protegida)
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_bd),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(task)
    db.commit
    return {"message": "Tarea eliminada correctamente"}