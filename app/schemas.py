from pydantic import BaseModel, EmailStr

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass 

class Task(TaskBase):
    id:int 

class config:
    orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class config:
        orm_mode: True
