# from fastapi import FastAPI
# from pydantic import BaseModel
# from scripts.scheduler import create_shift_scheduling_model, solve_shift_scheduling
# from sqlalchemy import JSON, create_engine, Column, Integer, String, ForeignKey, Enum
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# import uvicorn



# # Database setup
# DATABASE_URL = 'mysql+mysqlconnector://root:password@mysql-db/employee_info_db'
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# # Define Employee model (based on the table you created)
# class Employee(Base):
#     __tablename__ = "employee_info_tb"
#     employee_id = Column(Integer, primary_key=True, index=True)
#     employee_name = Column(String(250), nullable=False)
#     employee_email = Column(String(200), unique=True, nullable=False)
#     employee_phone = Column(String(20))
#     employment_type = Column(Enum('Part-time', 'Full-time'), nullable=False)
#     employee_availability = Column(JSON)
#     employee_role_id = Column(Integer)

# # API SET UP 
# app = FastAPI()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # python -m uvicorn main:app --reload   
# # Define the Pydantic model to accept the input JSON
# class ShiftScheduleInput(BaseModel):
#     num_employees: int
#     shifts_per_day: int
#     total_days: int
#     employee_types: list[str]  # List of employee types ('full_time' or 'part_time')

# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Employee Shift Scheduler is up!"}

# # Scheduler endpoint
# @app.post("/api/v1/scheduler")
# def scheduler(data: ShiftScheduleInput):
#     # Create the model based on the input data
#     model, shifts = create_shift_scheduling_model(
#         data.num_employees,
#         data.shifts_per_day,
#         data.total_days,
#         data.employee_types
#     )

#     # Solve the model and return the results
#     results = solve_shift_scheduling(
#         model, shifts, data.num_employees, data.shifts_per_day, data.total_days
#     )

#     # Example: Store the schedule in the database
#     for day, day_schedule in enumerate(results):
#         for shift in day_schedule["Day"]:
#             employee_id = shift["employee"]
#             new_schedule = scheduler(
#                 employee_id=employee_id,
#                 day=day + 1,
#                 shift=shift["shift"]
#             )
#             db.add(new_schedule)

#     db.commit()
#     return {"schedules": results}


# if __name__ == "__main__":
#     uvicorn.run(app="app:app", host="0.0.0.0", port=5000, reload=True)





# from fastapi import FastAPI, Depends  # Import Depends for dependency injection
# from pydantic import BaseModel
# from scripts.scheduler import create_shift_scheduling_model, solve_shift_scheduling
# from sqlalchemy import JSON, create_engine, Column, Integer, String, ForeignKey, Enum
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship, Session
# import uvicorn 
# from app.scripts.scheduler import create_shift_scheduling_model, solve_shift_scheduling
# from typing import List

# # Database setup
# DATABASE_URL = 'mysql+mysqlconnector://root:password@localhost:3306/employee_info_db'

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Define Employee model (based on the table you created)
# class Employee(Base):
#     __tablename__ = "employee_info_tb"
#     employee_id = Column(Integer, primary_key=True, index=True)
#     employee_name = Column(String(250), nullable=False)
#     employee_email = Column(String(200), unique=True, nullable=False)
#     employee_phone = Column(String(20))
#     employment_type = Column(Enum('Part-time', 'Full-time'), nullable=False)
#     employee_availability = Column(JSON)  # Storing availability as a list of shifts (morning, evening, closing)
#     employee_role_id = Column(Integer)


# # Define Schedule model
# class Schedule(Base):
#     __tablename__ = "schedule_tb"
#     id = Column(Integer, primary_key=True, index=True)
#     employee_id = Column(Integer, ForeignKey('employee_info_tb.employee_id'))
#     day = Column(Integer, nullable=False)
#     shift = Column(Integer, nullable=False)
#     employee = relationship("Employee")

# # Create tables if they do not exist
# Base.metadata.create_all(bind=engine)

# # API SET UP 
# app = FastAPI()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Define the Pydantic model to accept the input JSON
# class ShiftScheduleInput(BaseModel):
#     num_employees: int
#     shifts_per_day: int
#     total_days: int
#     employee_types: list[str]  # List of employee types ('full_time' or 'part_time')

# # Define the Pydantic model to add new employee 
# class EmployeeCreate(BaseModel):
#     employee_name: str
#     employee_email: str
#     employee_phone: str
#     employment_type: str
#     employee_availability: list[str]
#     employee_role_id: int

# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Employee List is up!"}

# # Scheduler endpoint
# @app.post("/api/v1/scheduler")
# def scheduler(data: ShiftScheduleInput, db: Session = Depends(get_db)):
#     # Create the model based on the input data
#     model, shifts = create_shift_scheduling_model(
#         data.num_employees,
#         data.shifts_per_day,
#         data.total_days,
#         data.employee_types
#     )

#     # Solve the model and return the results
#     results = solve_shift_scheduling(
#         model, shifts, data.num_employees, data.shifts_per_day, data.total_days
#     )

#     # Store the schedule in the database
#     for day, day_schedule in enumerate(results):
#         for shift in day_schedule[f"Day {day + 1}"]:
#             employee_id = shift["employee"]
#             new_schedule = Schedule(
#                 employee_id=employee_id,
#                 day=day + 1,
#                 shift=shift["shift"]
#             )
#             db.add(new_schedule)

#     db.commit()
#     return {"schedules": results}

# # GET endpoint to fetch all employees, returns a list of all employees in the database
# #  response_model=List[EmployeeCreate] ensures that only the necessary fields are exposed in the response
# @app.get("/api/v1/employees", response_model=List[EmployeeCreate])
# def get_employees(db: Session = Depends(get_db)):
#     employees = db.query(Employee).all()
#     return employees

# # POST endpoint to add a new employee to the database
# @app.post("/api/v1/employees", response_model=EmployeeCreate)
# def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
#     new_employee = Employee(
#         employee_name=employee.employee_name,
#         employee_email=employee.employee_email,
#         employee_phone=employee.employee_phone,
#         employment_type=employee.employment_type,
#         employee_availability=employee.employee_availability,
#         employee_role_id=employee.employee_role_id
#     )
#     db.add(new_employee)
#     db.commit()
#     db.refresh(new_employee)
#     return new_employee


# if __name__ == "__main__":
#     uvicorn.run(app="app:app", host="0.0.0.0", port=5000, reload=True)





from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import JSON, create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from typing import List
import uvicorn


from app.scripts.scheduler import create_shift_scheduling_model, solve_shift_scheduling

# Database setup
DATABASE_URL = 'mysql+mysqlconnector://root:password@localhost:3306/employee_info_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Employee model (based on the table you created)
class Employee(Base):
    __tablename__ = "employee_info_tb"
    employee_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String(250), nullable=False)
    employee_email = Column(String(200), unique=True, nullable=False)
    employee_phone = Column(String(20))
    employment_type = Column(Enum('Part-time', 'Full-time'), nullable=False)
    employee_availability = Column(JSON)
    employee_role_id = Column(Integer)

# Define Schedule model
class Schedule(Base):
    __tablename__ = "schedule_tb"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employee_info_tb.employee_id'))
    day = Column(Integer, nullable=False)
    shift = Column(Integer, nullable=False)
    employee = relationship("Employee")

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# API SET UP
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the Pydantic models
class ShiftScheduleInput(BaseModel):
    num_employees: int
    shifts_per_day: int
    total_days: int
    employee_types: list[str]

class EmployeeCreate(BaseModel):
    employee_name: str
    employee_email: str
    employee_phone: str
    employment_type: str
    employee_availability: list[str]
    employee_role_id: int

class ScheduleRead(BaseModel):
    id: int
    employee_id: int
    day: int
    shift: int

    class Config:
        orm_mode = True

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Employee List is up!"}

# Scheduler endpoint
@app.post("/api/v1/scheduler")
def scheduler(data: ShiftScheduleInput, db: Session = Depends(get_db)):
    # Create the model based on the input data
    model, shifts = create_shift_scheduling_model(
        data.num_employees,
        data.shifts_per_day,
        data.total_days,
        data.employee_types
    )

    # Solve the model and return the results
    results = solve_shift_scheduling(
        model, shifts, data.num_employees, data.shifts_per_day, data.total_days
    )

    # Store the schedule in the database
    for day, day_schedule in enumerate(results):
        for shift in day_schedule[f"Day {day + 1}"]:
            employee_id = shift["employee"]
            new_schedule = Schedule(
                employee_id=employee_id,
                day=day + 1,
                shift=shift["shift"]
            )
            db.add(new_schedule)

    db.commit()
    return {"schedules": results}

# GET endpoint to fetch all employees
@app.get("/api/v1/employees", response_model=List[EmployeeCreate])
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees

# POST endpoint to add a new employee
@app.post("/api/v1/employees", response_model=EmployeeCreate)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(
        employee_name=employee.employee_name,
        employee_email=employee.employee_email,
        employee_phone=employee.employee_phone,
        employment_type=employee.employment_type,
        employee_availability=employee.employee_availability,
        employee_role_id=employee.employee_role_id
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee



# GET endpoint to fetch a specific employee by ID
@app.get("/api/v1/employees/{employee_id}", response_model=EmployeeCreate)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# GET endpoint to fetch all schedules
@app.get("/api/v1/schedules", response_model=List[ScheduleRead])
def get_schedules(db: Session = Depends(get_db)):
    schedules = db.query(Schedule).all()
    return schedules




if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=5000, reload=True)
