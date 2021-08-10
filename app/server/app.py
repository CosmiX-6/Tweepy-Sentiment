from fastapi import FastAPI, Request
from app.server.routes.gettweets import router as TweetRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates('app/server/templates')

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/server/static"), name="static")

app.include_router(TweetRouter, tags=["TweepySentiment"]) # , prefix="/sentiment")

@app.get('/',tags=["Root"], include_in_schema=False)
async def read_root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})
