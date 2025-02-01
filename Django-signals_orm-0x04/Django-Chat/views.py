from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # This triggers the post_delete signal
        return redirect('home')  # Redirect to a home or logout page after deletion
    return render(request, 'Django-Chat/delete_user.html')
  
