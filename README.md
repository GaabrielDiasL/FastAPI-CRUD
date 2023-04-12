FastAPI-CRUD

Introduction

Hello everyone,

I have created this CRUD application using FastAPI. As a developer who frequently uses FastAPI, I thought it would be helpful to have a default FastAPI startup for future projects.

Features

This API includes:

CRUD Routes
Security using Bearer Token
MongoDB connection
More features will be added soon.

Getting Started

To use this application, you need to make a few changes to the src/dbgit.py file. You'll need to update the file name to db.py. This is because I've added my real db connection string to another file, which is not included in this Github repository.

How to Use

Clone this repository to your local machine.
Install the required dependencies using pip install -r requirements.txt.
Update src/dbgit.py to src/db.py.
Run the application using uvicorn main:app --reload.
Navigate to http://localhost:8000/docs to view the Swagger UI.
Conclusion

I hope you find this FastAPI-CRUD application helpful. If you have any questions or suggestions, feel free to open an issue or pull request.
