import os


def file_listing(path):
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if '.py' in filename and '.pyc' not in filename and '__init__' not in filename:
                if 'venv' not in dirname:
                    print(os.path.join(dirname, filename))
                else:
                    continue
            else:
                continue


def git_clone():
    return os.system('GIT_TERMINAL_PROMPT=0 git clone https://github.com/Yaroher2442/tetrika_test.git')


git_rezult = git_clone()
if git_rezult != 0:
    print(git_rezult)
else:
    print('ok')
