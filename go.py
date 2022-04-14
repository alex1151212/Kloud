
from starlette.config import Config

from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
import uvicorn
from fastapi import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from starlette.responses import HTMLResponse

from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
# OAuth settings
SECRET_KEY = 'CKFGkJEnJJwLICiXy17uPoFggzz39-f4RUIPVaaj'
GOOGLE_CLIENT_ID = '816065165801-fgbh2n77386m8733nii1nkocc7da0l9u.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/')

@app.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


if __name__ == '__main__':
    uvicorn.run("go:app",host='0.0.0.0',port=8000,reload=True,debug=True)
