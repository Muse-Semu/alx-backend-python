from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.sender and request.user != message.receiver:
        return render(request, 'messaging/error.html', {'error': 'You do not have permission to view this history.'})
    
    history = message.history.all()
    return render(request, 'messaging/history.html', {'message': message, 'history': history})

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # Redirect to homepage after deletion
    return render(request, 'messaging/delete_user.html')