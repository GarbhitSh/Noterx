from django.shortcuts import render, redirect
from .models import Note
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
 
 
# create editor page
@login_required(login_url='/login/')
def editor(request):
    docid = int(request.GET.get('docid', 0))
    notes = Note.objects.all()
 
    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')
 
        if docid > 0:
            note = Note.objects.get(pk=docid)
            note.title = title
            note.content = content
            note.save()
 
            return redirect('/?docid=%i' % docid)
        else:
            note = Note.objects.create(title=title, content=content)
 
            return redirect('/?docid=%i' % note.id)
 
    if docid > 0:
        note = Note.objects.get(pk=docid)
    else:
        note = ''
 
    context = {
        'docid': docid,
        'notes': notes,
        'note': note
    }
 
    return render(request, 'editor.html', context)
 
# create delete notes page
 
 
@login_required(login_url='/login/')
def delete_note(request, docid):
    note = Note.objects.get(pk=docid)
    note.delete()
 
    return redirect('/?docid=0')
 
 
# login page for user
def login_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.error(request, "Username not found")
                return redirect('/login/')
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('editor')
            messages.error(request, "Wrong Password")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register/')
    return render(request, "login.html")
 
 
# register page for user
def register_page(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is taken")
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account created")
            return redirect('/login')
        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('/register')
    return render(request, "register.html")
 
 
# logout function
def custom_logout(request):
    logout(request)
    return redirect('login')
