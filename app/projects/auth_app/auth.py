from authlib.integrations.starlette_client import OAuth, OAuthError
from .config import CLIENT_ID, CLIENT_SECRET
from fastapi import APIRouter,Form
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request,HTTPException
from fastapi.responses import HTMLResponse



oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile'

    }
)

templates = Jinja2Templates(directory="projects/auth_app/templates")
router = APIRouter()

@router.get("/")
def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('welcome')

    return templates.TemplateResponse(
        name="login.html",
        context={"request": request}
    )


@router.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return templates.TemplateResponse(
        name='home.html',
        context={'request': request, 'user': user}
    )


@router.get("/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/auth_app/auth"
    # redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request': request, 'error': e.error}
        )
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse('welcome')


@router.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    return RedirectResponse('/auth_app')


fake_db = {}

@router.get('/view_profile', response_class=HTMLResponse, name='view_profile')
def get_view_profile(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')

    email = user['email']

    if email not in fake_db:
        fake_db[email] = {
            'name': user['name'],
            'email': email,
            'picture': user['picture'],
            'family_name': user.get('family_name', 'N/A'),
            'bio': user.get('bio', 'N/A'),
            'phone': user.get('phone', 'N/A')
        }

    return templates.TemplateResponse(
        name='profile.html',
        context={'request': request, 'user': fake_db[email]}
    )


@router.post('/update_profile', name='update_profile')
def post_update_profile(request: Request,picture: str=Form(...), bio: str = Form(...), phone: str = Form(...)):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    email = user['email']

    if email not in fake_db:
        raise HTTPException(status_code=404, detail="User not found in fake_db")
    fake_db[email]['picture']=picture
    fake_db[email]['bio'] = bio
    fake_db[email]['phone'] = phone
    return {"message": "User details updated successfully"}

@router.get('/edit_profile', response_class=HTMLResponse)
def edit_profile(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    email = user['email']
    return templates.TemplateResponse(
        name='edit_profile.html',
        context={'request': request, 'user': fake_db[email]}
    )

