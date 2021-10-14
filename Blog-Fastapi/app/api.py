from fastapi import Body, Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.model import PostSchema, UserLoginSchema, UserSchema

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum"
    }
]

users = []

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["root"])
async def read_root(request: Request) -> dict:
    return templates.TemplateResponse("blogpage.html", {
        "request": request
    })

# get all posts in the blog
@app.get("/posts", tags=["posts"])
async def get_posts() -> dict:
    return {"data": posts}

# get single post by id
@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with that ID"
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }

# add new post into blog
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "Post added!"
    }

# user registration route
@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)
    
# check if a user exists
def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

# define login route
@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Incorrect login details"
    }

