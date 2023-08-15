from fastapi import FastAPI, Request, Form
from app.routers import blog, comment, reply, user

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from app.models.blog import Blog
from app.controllers.blog_controller import create_blog, get_all_blogs, get_blog, update_blog, delete_blog, get_all_blogs_all, get_blog, get_all_blogs




app = FastAPI()

app.include_router(blog.router)
app.include_router(comment.router)
app.include_router(reply.router)
app.include_router(user.router)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    blogs = get_all_blogs()
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs})


@app.get("/blog/{blog_id}", response_class=HTMLResponse)
async def read_blog(request: Request, blog_id: str):
    blog = get_blog(blog_id)
    return templates.TemplateResponse("blog.html", {"request": request, "blog": blog})

@app.get("/blog/{blog_id}/edit", response_class=HTMLResponse)
async def edit_blog(request: Request, blog_id: str):
    blog = get_blog(blog_id)
    return templates.TemplateResponse("edit_blog.html", {"request": request, "blog": blog})

# @app.get("/blog/add", response_class=HTMLResponse)
# async def add_blog(request: Request):
#     return templates.TemplateResponse("add.html", {"request": request})

@app.post("/blog/", response_class=HTMLResponse)
async def create_blog_endpoint(request: Request, text: str = Form(...)):
    blog = {"text": text}
    created_blog = create_blog(blog)
    return RedirectResponse(url="/")


@app.post("/blog/{blog_id}", response_class=HTMLResponse)
async def update_blog_endpoint(request: Request, blog_id: str, text: str = Form(...)):
    updated_blog = {"text": text}
    updated_blog = update_blog(blog_id, updated_blog)

    # Use RedirectResponse to redirect to the blog's detail page
    return RedirectResponse(url="/")


@app.post("/blog/{blog_id}/delete", response_class=HTMLResponse)
async def delete_blog_endpoint(request: Request, blog_id: str):
    delete_blog(blog_id)
    return RedirectResponse(url="/")


@app.get("/all", response_class=HTMLResponse)
async def read_all(request: Request):
    blogs = get_all_blogs_all()
    return templates.TemplateResponse("all.html", {"request": request, "blogs": blogs})

