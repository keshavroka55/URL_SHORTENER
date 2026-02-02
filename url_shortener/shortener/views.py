from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
import qrcode
from io import BytesIO

from .models import ShortURL
from .utils import encode_base62


@login_required
def dashboard(request):
    urls = ShortURL.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'urls': urls})


@login_required
def create_url(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        custom_key = request.POST.get('custom_key')
        expires_at = request.POST.get('expires_at')

        if custom_key:
            if ShortURL.objects.filter(short_key=custom_key).exists():
                return HttpResponse("Custom key already exists")
            short_key = custom_key
            obj = ShortURL.objects.create(
                user=request.user,
                original_url=original_url,
                short_key=short_key,
                expires_at=expires_at or None
            )
        else:
            obj = ShortURL.objects.create(
                user=request.user,
                original_url=original_url
            )
            obj.short_key = encode_base62(obj.id)
            obj.expires_at = expires_at or None
            obj.save()

        return redirect('dashboard')

    return render(request, 'create.html')


@login_required
def edit_url(request, id):
    url = get_object_or_404(ShortURL, id=id, user=request.user)

    if request.method == 'POST':
        url.original_url = request.POST['original_url']
        url.save()
        return redirect('dashboard')

    return render(request, 'edit.html', {'url': url})


@login_required
def delete_url(request, id):
    url = get_object_or_404(ShortURL, id=id, user=request.user)
    url.delete()
    return redirect('dashboard')


def redirect_url(request, short_key):
    url = get_object_or_404(ShortURL, short_key=short_key, is_active=True)

    if url.is_expired():
        return HttpResponse("This link has expired")

    url.click_count += 1
    url.save()

    return redirect(url.original_url)


@login_required
def qr_code(request, short_key):
    url = get_object_or_404(ShortURL, short_key=short_key, user=request.user)

    qr = qrcode.make(request.build_absolute_uri(f'/{short_key}'))
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")
