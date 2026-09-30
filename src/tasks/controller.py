from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.user.models import UserModel



def create_task(body: TaskSchema, db : Session, user:UserModel):
    data = body.model_dump()

    new_task = TaskModel(title = data["title"], 
                         description = data["description"], 
                         is_completed = data["is_completed"], 
                         user_id = user.id)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
 

    return new_task

#controller for all tasks
def get_tasks (db:Session, user:UserModel) :
    tasks = db. query (TaskModel).filter(TaskModel.user_id == user.id ).all()
    return tasks


def get_one_task(task_id:int, db:Session):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="task id not found or invalid")

    return one_task
 

#first we define everything here in the controller and then we call call and import 
# it in the router block which is then called in the main.py file. 
# This is done to keep the code clean and organized.



#updating task controller
def update_task(body:TaskSchema, task_id:int, db: Session, user:UserModel) :
    one_task:TaskModel = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task Id is Incorrect")

    if one_task.user_id != user.id:
         raise HTTPException(401, detail="You are not allowed to make changes")
        
   

    body = body.model_dump()
    for field, value in body.items():   #for handling multiple fileds in the task one by one
        setattr(one_task, field, value)

    db.add (one_task)
    db.commit()
    db.refresh(one_task)
    return one_task


#deleting task controller

def delete_task(task_id:int, db:Session, user:UserModel):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
       raise HTTPException(404, detail="Task Id is Incorrect")

    if one_task.user_id != user.id:
        raise HTTPException(401, detail="You are not allowed to delete the task")

    db.delete(one_task)
    db.commit()
    return None
     
         

 