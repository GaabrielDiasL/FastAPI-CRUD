from fastapi import FastAPI
from routes.router import router
import routes.token

app = FastAPI(
    title="Gabriel's simple CRUD Example API",
    version="1.0.0",
    contact={
        "name": "Gabriel Dias Luz",
        "email": "gabrieldiasluz97@gmail.com",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.include_router(router)