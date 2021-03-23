import os
import shutil

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .form import UploadFileForm, Register, Git_form
from .models import Progs, Syntax
from .tasks import syntax_test,syntax_test_2


@csrf_exempt
def logining(request):
    if request.method == 'POST':
        print(request.POST.dict())
        # username = request.POST.dict()
        user = authenticate(request, **request.POST.dict())
        print(user)
        if user is not None:
            login(request, user)
            direct_dir = os.path.join(os.getcwd(), 'main', 'user_files')
            if user.username not in os.listdir(direct_dir):
                os.mkdir(os.path.join(direct_dir, user.get_username()))
            else:
                pass
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/register')
    else:
        context = {}
        return render(request, 'main/helpers/login.html', context)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
        return HttpResponseRedirect('/login')
    else:
        context = {'form': Register()}
        return render(request, 'main/helpers/register.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def index(request):
    user_name = request.user.username
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    context = {'prg_names': valids_progs(user_name),
               'page_flag': '',
               'prg_data': '',
               'dataset': {},
               'status': ''}
    return render(request, 'main/index.html', context)


def how_use(request):
    context = {}
    return render(request, 'main/how_use.html', context)


def valids_progs(user_name):
    progs_dir = os.listdir(os.path.join(os.getcwd(), 'main', 'user_files', user_name))
    return progs_dir


@login_required(login_url='/login')
@csrf_exempt
def prog(request, prg_name):
    print(request.user.username)
    user_name = request.user.username
    cur_prg = Progs.objects.get(filename=prg_name)
    p_id = cur_prg.id
    status = cur_prg.get_status()
    version = cur_prg.get_version()
    color_dict = {'not_runned': 'darkgray', 'syntax_errors': 'yellow', 'passed': 'green'}
    synt = Syntax.objects.filter(prog_id=p_id)
    dataset = []
    for s in synt:
        up_data = s.get_dict()
        up_data['time'] = s.time
        dataset.append(up_data)
    context = {'prg_names': valids_progs(user_name),
               'title': prg_name,
               'status': status.replace('_', ' '),
               'status_colour': color_dict[status],
               'version': version,
               'dataset': dataset,
               'user_name': user_name
               }
    return render(request, 'main/prog.html', context)


def process_syntax(request, prg_name):
    user_name = request.user.username
    analys_path = os.path.join(os.getcwd(), 'main', 'user_files', prg_name, prg_name + '.py')
    cur_prg = Progs.objects.get(filename=prg_name)
    prog_id = cur_prg.id
    version = cur_prg.version
    # syntax_test(analys_path, prog_id, version)
    cell_dir=os.path.join(os.getcwd(), 'main', 'user_files',user_name, prg_name)
    syntax_test_2(cell_dir,prog_id,version)
    return HttpResponseRedirect(f'/prog/{prg_name}')


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        user_name = request.user.username
        form = UploadFileForm(request.POST, request.FILES)
        git = Git_form(request.POST)
        if git.is_valid():
            def git_clone(href, path):
                return os.system(
                    f'GIT_TERMINAL_PROMPT=0 git clone {href} {path}')

            def git_error():
                context = {'prg_names': valids_progs(user_name),
                           'form': UploadFileForm(),
                           'git': Git_form(),
                           'user_name': user_name,
                           'git_error': 'Dwnload failed, try again'
                           }
                return render(request, 'main/upload.html', context)

            link = git.cleaned_data['git_link']
            direct_dir = os.path.join(os.getcwd(), 'main', 'user_files', user_name)
            if '/' not in link or link.count('/') < 4:
                return git_error()
            else:
                prj_name = link.split('/')[-1]
            if prj_name in os.listdir(direct_dir):
                cell_dir = os.path.join(direct_dir, prj_name)
                shutil.rmtree(cell_dir, ignore_errors=True)
                os.mkdir(cell_dir)
                if git_clone(link, cell_dir) != 0:
                    return git_error()
                prg = Progs.objects.get(filename=prj_name)
                prg.version += 1
                prg.save()
            else:
                cell_dir = os.path.join(direct_dir, prj_name)
                os.mkdir(cell_dir)
                if git_clone(link, cell_dir) != 0:
                    return git_error()
                new_p = Progs()
                new_p.filename = prj_name
                new_p.status = 'not_runned'
                new_p.save_base()
            return HttpResponseRedirect(f'''/prog/{prj_name}''')
        if form.is_valid():
            f_name = request.FILES['file'].name

            witout_py = f_name.replace('.py', '')
            direct_dir = os.path.join(os.getcwd(), 'main', 'user_files', user_name, witout_py)

            def write_file(f):
                path = default_storage.save(
                    os.path.join(direct_dir, f_name), ContentFile(f.read()))

            if witout_py in os.listdir(os.path.join(os.getcwd(), 'main', 'user_files', user_name)):
                os.remove(os.path.join(direct_dir, f_name))
                prg = Progs.objects.get(filename=witout_py)
                prg.version += 1
                prg.save()
                f = request.FILES['file']
                write_file(f)
            else:
                os.mkdir(os.path.join(direct_dir))
                f = request.FILES['file']
                write_file(f)
                new_p = Progs()
                new_p.filename = witout_py
                new_p.status = 'not_runned'
                new_p.save_base()
            return HttpResponseRedirect(f'''/prog/{witout_py}''')
    else:
        user_name = request.user.username
        context = {'prg_names': valids_progs(user_name),
                   'form': UploadFileForm(),
                   'git': Git_form(),
                   'user_name': user_name
                   }
        return render(request, 'main/upload.html', context)


def delite(request, p_name):
    user_name = request.user.username
    cur_prg = Progs.objects.get(filename=p_name)
    print('qwr')
    shutil.rmtree(os.path.join(os.getcwd(), 'main', 'user_files', user_name, p_name), ignore_errors=True)
    print('qwr_2')
    for ob in Syntax.objects.filter(prog_id=cur_prg.id):
        ob.delete()
    cur_prg.delete()
    return HttpResponseRedirect('/')
