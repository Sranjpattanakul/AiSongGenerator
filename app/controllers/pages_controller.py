from django.shortcuts import render, redirect
from app.models import User, Library, Song, Draft


def _ctx(request, active_page):
    user_name = request.session.get('user_name', 'User')
    return {
        'user_email': request.session.get('user_email'),
        'user_name': user_name,
        'user_picture': request.session.get('user_picture', ''),
        'user_initial': (user_name or 'U')[0].upper(),
        'active_page': active_page,
    }


def library_page(request):
    if not request.session.get('user_email'):
        return redirect('login')
    user_id = None
    songs = []
    drafts = []
    try:
        user = User.objects.get(email=request.session['user_email'])
        user_id = user.id
        library = Library.objects.get(user=user)
        songs = Song.objects.filter(library=library).order_by('-created_at')
        drafts = Draft.objects.filter(library=library).select_related('prompt').order_by('-last_modified_at')
    except Exception:
        drafts = []
    ctx = _ctx(request, 'library')
    ctx['songs'] = songs
    ctx['drafts'] = drafts
    ctx['user_id'] = user_id
    return render(request, 'library.html', ctx)


def browse_page(request):
    if not request.session.get('user_email'):
        return redirect('login')
    songs = Song.objects.filter(status='SUCCESS').select_related('library__user').order_by('-created_at')[:48]
    ctx = _ctx(request, 'browse')
    ctx['songs'] = songs
    return render(request, 'browse.html', ctx)
