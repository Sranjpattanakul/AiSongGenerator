from django.shortcuts import render, redirect
from app.models import User


def index(request):
    if not request.session.get('user_email'):
        return redirect('login')
    user_name = request.session.get('user_name', 'User')
    user_id = None
    try:
        user_id = User.objects.get(email=request.session['user_email']).id
    except Exception:
        pass
    return render(request, 'home.html', {
        'user_email': request.session.get('user_email'),
        'user_name': user_name,
        'user_picture': request.session.get('user_picture', ''),
        'user_initial': (user_name or 'U')[0].upper(),
        'active_page': 'home',
        'user_id': user_id,
    })
