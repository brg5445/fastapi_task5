from fastapi import FastAPI
from src.infrastructure.sqlite.models import category_models, comment_models, location_models, post_models
from src.api import users, categories, locations, posts, comments, auth
# from src.infrastructure.sqlite.database import Base, engine
from src.infrastructure.sqlite.models import user_models # noqa

# Base.metadata.create_all(bind=engine) # После добавления alembic выполнение данной строки скорее всего не нужно.

app = FastAPI()


# Добавил роутеры, чтоб не импортировать последовательно один API в другой.
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(auth.router)