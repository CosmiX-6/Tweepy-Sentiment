from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.server.sentiment import sentiment_analyzer
from app.server.models.models import ErrorResponseModel

templates = Jinja2Templates('app/server/templates')

router = APIRouter()

# Loads the search page
@router.get("/search_tweet", include_in_schema=False)
def search_tweet(request: Request):
    result = "Enter search query..."
    return templates.TemplateResponse('sentiment.html', context={'request': request, 'result': result})

# Process the search query
@router.post("/search_tweet", include_in_schema=False)
def search_tweet(request: Request, search_txt: str = Form(...)):
    try:
        output = sentiment_analyzer.predict(search_txt)
        if output == False:
            return templates.TemplateResponse('error.html', context={'request': request, 'code': 429, 'message': 'Free Api Rate Limit (Try again after 15min)'})
        elif output == None:
            return templates.TemplateResponse('error.html', context={'request': request, 'code': 404, 'message': 'Not Found'})
        return templates.TemplateResponse('processed.html', context={'request': request, 'query': search_txt, 'result': output})
    except:
        return templates.TemplateResponse('error.html', context={'request': request, 'code': 503, 'message': 'Server Overload'})
        
@router.post("/search_tweets")
def search_tweet(request: Request, search_txt: str = Form(...)):
    try:
        output = sentiment_analyzer.predict(search_txt)
        if output == None:
            return ErrorResponseModel("An error occurred", 404, "No data found for entered query.")
        elif output == False:
            return ErrorResponseModel("An error occurred", 429, "Free Api Rate Limit (Try again after 15min.)")
        return {'query': search_txt, 'result': output}
    except:
        return ErrorResponseModel("An error occurred", 503, "Server Overload.")