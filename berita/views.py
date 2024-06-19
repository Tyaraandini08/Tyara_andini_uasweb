from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from berita.models import Kategori, Artikel
from berita.forms import ArtikelForm

# Create your views here.
def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False

@login_required
def dashboard(request):
    template_name = "dashboard/index.html"
    total_users = User.objects.count()
    total_kategori = Kategori.objects.count()
    total_artikel = Artikel.objects.count()

    context = {
        'title' : 'Selamat Datang Di Dashboard',
        'total': total_users,
        'total_kategori': total_kategori,
        'total_artikel': total_artikel,
    }
    return render(request, template_name, context)

##################################################Kategori#####################################################
@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def kategori_list(request):
    template_name = "dashboard/snippets/kategori/kategori_list.html"
    kategori_ambil = Kategori.objects.all()
    print(kategori_ambil)
    context = {
        'title' : 'Halaman Kategori',
        'kategori': kategori_ambil
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def kategori_add(request):
    template_name = "dashboard/snippets/kategori/kategori_add.html"
    if request.method == "POST":
        nama_input = request.POST.get('nama_kategori')
        Kategori.objects.create(
            nama = nama_input
        )
        return redirect(kategori_list)
    
    context = {
        'title' : 'Tambah Kategori',
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def kategori_update(request, id_kategori ):
    template_name = "dashboard/snippets/kategori/kategori_update.html"
    try:
        kategori = Kategori.objects.get(id=id_kategori)
    except:
        return redirect(kategori_list)
    if request.method == "POST":
        nama_input = request.POST.get('nama_kategori')
        kategori.nama = nama_input
        kategori.save()
        return redirect(kategori_list)
    context ={
        'titel' : 'Update Kategori',
        'kategori' : kategori,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator, login_url='/authentikasi/logout')
def kategori_delete(request, id_kategori):
    try:
        Kategori.objects.get(id=id_kategori).delete()
    except:
        pass
    return redirect(kategori_list)

##################################################Kategori#####################################################

##################################################Artikel######################################################
@login_required
def artikel(request):
    template_name = "dashboard/artikel.html"
    context = {
        'title' : 'Halaman Artikel'
    }
    return render(request, template_name, context)

@login_required
def artikel_list(request):
    template_name = "dashboard/snippets/artikel/artikel_list.html"
    if request.user.groups.filter(name='Operator'):
        artikel = Artikel.objects.all()
    else:
        artikel = Artikel.objects.filter(author=request.user)
    context = {
        'title' : 'Daftar Artikel',
        'artikel' : artikel,
    }
    return render(request, template_name, context)

@login_required
def artikel_add(request):
    template_name = "dashboard/snippets/artikel/artikel_forms.html"
    if request.method == "POST":
        forms = ArtikelForm(request.POST, request.FILES)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.author = request.user
            pub.save()
            return redirect(artikel_list)
        else:
            print(forms.error_class)
    forms = ArtikelForm
    context = {
        'titel' : 'Tambah Atikel',
        'forms' : forms
    }
    return render(request, template_name, context)

@login_required
def artikel_detail(request, id_artikel):
    template_name = "dashboard/snippets/artikel/artikel_detail.html"
    artikel = Artikel.objects.get(id=id_artikel)
    context = {
        'titel' : 'Tambah Atikel',
        'artikel' : artikel, 
    }
    return render(request, template_name, context)

@login_required
def artikel_update(request, id_artikel):
    template_name = "dashboard/snippets/artikel/artikel_forms.html"
    artikel = Artikel.objects.get(id=id_artikel)
    try:
        artikel = Artikel.objects.get(id=id_artikel)
    except Artikel.DoesNotExist:
        return redirect(artikel_list)
    
    # Lakukan pengecekan operator dan penulis artikel
    if request.user.groups.filter(name='Operator').exists() or artikel.author == request.user:
        forms = ArtikelForm(instance=artikel)
        
        if request.method == "POST":
            forms = ArtikelForm(request.POST, request.FILES, instance=artikel)
            if forms.is_valid():
                pub = forms.save(commit=False)
                pub.author = request.user
                pub.save()
                return redirect(artikel_list)
        
        context = {
            'title': 'Update Artikel',
            'forms': forms
        }
        return render(request, template_name, context)
    else:
        return redirect('home')

@login_required
def artikel_delete(request, id_artikel):
    try:
        artikel = Artikel.objects.get(id=id_artikel)
        if request.user.groups.filter(name='Operator'):
            pass
        else:
            if artikel.author != request.user:
                return redirect ('home')
        artikel.delete()
    except:
        pass
    return redirect(artikel_list)
