import time
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from typing import List
import time
import asyncio
import ocr
import utils

class Course(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    author: Optional[str] = None


app = FastAPI()


# @app.get("/")
# def root():
#     return {"message": "Hello World"}

@app.get("/")
async def home():
    tasks = []
    start = time.time()
    for i in range(2):
        tasks.append(asyncio.create_task(func1()))
        tasks.append(asyncio.create_task(func2()))
    response = await asyncio.gather(*tasks)
    end = time.time()
    return {"response": response, "time_taken": (end - start)}


async def func1():
    await asyncio.sleep(2)
    return "Func1() Completed"


async def func2():
    await asyncio.sleep(1)
    return "Func2() Completed"

course_items = [{"course_name": "Python"}, {
    "course_name": "NodeJS"}, {"course_name": "Machine Learning"}]


@app.get("/courses/")
def read_courses(start: int = 0, end: int = 10):
    return course_items[start: start + end]


# @app.get("/courses/{course_name}")
# def read_course(course_name: int):
#     print(type(course_name))
#     return {"course_name": course_name}

@app.post("/courses/")
def create_course(course: Course):
    return course


course_items2 = {1: "Python", 2: "NodeJS", 3: "Machine Learning"}


@app.get("/courses/{course_id}")
def read_courses(course_id: int, q: Optional[str] = None):
    if q is not None:
        return {"course_name": course_items2[course_id], "q": q}
    return {"course_name": course_items2[course_id]}


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


@app.post("/api/v1/extract_text")
async def extract_text(Images: List[UploadFile] = File(...)):
    response = {}
    s = time.time()
    for img in Images:
        print("Images Uploaded: ", img.filename)
        temp_file = utils._save_file_to_server(
            img, path="./", save_as=img.filename)
        text = await ocr.read_image(temp_file)
        response[img.filename] = text
    response["Time Taken"] = round((time.time() - s), 2)

    return response
