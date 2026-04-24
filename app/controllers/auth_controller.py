import secrets
from urllib.parse import urlencode

import requests as http_requests
from django.conf import settings
from django.shortcuts import redirect

from app.models import User, Library

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
REDIRECT_URI = 'http://localhost:8000/auth/callback/'


def google_auth(request):
    state = secrets.token_urlsafe(16)
    request.session['oauth_state'] = state

    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'online',
        'prompt': 'select_account',
    }
    return redirect(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


def google_callback(request):
    if request.GET.get('error'):
        return redirect('/login/')

    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code or state != request.session.get('oauth_state'):
        return redirect('/login/')

    token_resp = http_requests.post(GOOGLE_TOKEN_URL, data={
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    })

    if not token_resp.ok:
        return redirect('/login/')

    access_token = token_resp.json().get('access_token')

    userinfo_resp = http_requests.get(
        GOOGLE_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    if not userinfo_resp.ok:
        return redirect('/login/')

    info = userinfo_resp.json()
    email = info.get('email', '')
    name = info.get('name', email.split('@')[0])
    google_id = info.get('sub', '')
    picture = info.get('picture', '')

    if not email:
        return redirect('/login/')

    user, _ = User.objects.get_or_create(
        email=email,
        defaults={
            'display_name': name,
            'google_id': google_id,
        },
    )
    Library.objects.get_or_create(user=user)

    request.session['user_email'] = user.email
    request.session['user_name'] = user.display_name
    request.session['user_picture'] = picture

    return redirect('/')


def demo_login(request):
    if request.method != 'POST':
        return redirect('login')

    email = request.POST.get('email', '').strip()
    name = request.POST.get('name', '').strip()

    if not email:
        return redirect('login')

    user, _ = User.objects.get_or_create(
        email=email,
        defaults={
            'display_name': name or email.split('@')[0],
            'google_id': f'demo-{email}',
        },
    )
    Library.objects.get_or_create(user=user)

    request.session['user_email'] = user.email
    request.session['user_name'] = user.display_name
    request.session['user_picture'] = ''

    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('login')
