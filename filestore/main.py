from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from filestore.routes import file


def app_factory():
    """
    returns FastAPI object 
    """

    app = FastAPI()

    origins = [
        "http://localhost:3000",
        "localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(file.router)
    # Includes routes to the app.
    # app.include_router(users_route.router)
    # app.include_router(posts_route.router)

    return app


app = app_factory()