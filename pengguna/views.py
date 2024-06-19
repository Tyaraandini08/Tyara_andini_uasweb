from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from pengguna.forms import ( UserEditFormDB, )
from pengguna.models import Biodata

# Create your views here.
def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False
    

@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def pengguna_list(request):
    template_name = "dashboard/snippets/pengguna/pengguna_list.html"
    users = User.objects.all()

    user = request.user
    try:
        biodata = Biodata.objects.get(user=user)
    except Biodata.DoesNotExist:
        biodata = None

    context = {
        'title' : 'Selamat Datang Di Web Saya',
        'users' : users,
        'biodata': biodata,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def pengguna_edit(request, id_user):
    template_name = "dashboard/snippets/pengguna/pengguna_edit.html"

    users = request.user
    try:
        biodata = Biodata.objects.get(user=users)
    except Biodata.DoesNotExist:
        biodata = None

    user = User.objects.get(id=id_user)
    if request.method == 'POST':
        form = UserEditFormDB(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()  # To save the groups
            return redirect('pengguna_list')
    else:
        form = UserEditFormDB(instance=user)

        context = {
        'title': 'Edit User',
        'form': form,
        'biodata': biodata,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def pengguna_delete(request, id_user):
    try:
        user = User.objects.get(id=id_user)
        if request.user.groups.filter(name='Operator'):
            pass
        else:
            if user.author != request.user:
                return redirect ('home')
        user.delete()
    except:
        pass
    return redirect(pengguna_list)