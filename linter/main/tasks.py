from pylint import epylint as lint
from .models import Syntax
from celery import shared_task
from datetime import datetime
from celery import app
import os


@app.shared_task()
def syntax_test(file_path, prog_id, version):
    try:
        report_items = {}
        syntax_err = []
        (pylint_stdout, pylint_stderr) = lint.py_run(command_options=file_path, return_std=True)
        lints = pylint_stdout.getvalue().split('\n')[1:]
        for l in lints:
            if 'warning' in l:
                err = l.split(':')
                syntax_err.append(f'line({err[2]}) : {err[3]} ')
            if 'rated' in l:
                report_items['code_score'] = l.split('(')[0]
            else:
                continue
        report_items['syntax_count'] = str(len(syntax_err))
        report_items['syntax_errors'] = '\n'.join(syntax_err)
        report_items['time'] = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
        print(report_items)
        test_s = Syntax(time=report_items['time'],
                        version=version,
                        prog_id=prog_id,
                        err_text=report_items['syntax_errors'],
                        count=report_items['syntax_count'],
                        score=report_items['code_score'],
                        )
        test_s.save()
        return 'okkkkkk'
    except:
        return -1


def syntax_test_2(file_path, prog_id, version):
    try:
        for dirname, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                if '.py' in filename and '.pyc' not in filename and '__init__' not in filename:
                    if 'venv' not in dirname:
                        cur_file=os.path.join(dirname, filename)
                        report_items = {}
                        syntax_err = []
                        (pylint_stdout, pylint_stderr) = lint.py_run(command_options=cur_file, return_std=True)
                        lints = pylint_stdout.getvalue().split('\n')[1:]
                        for l in lints:
                            if 'warning' in l:
                                err = l.split(':')
                                syntax_err.append(f'line({err[2]}) : {err[3]} ')
                            if 'rated' in l:
                                report_items['code_score'] = l.split('(')[0]
                            else:
                                continue
                        report_items['syntax_count'] = str(len(syntax_err))
                        report_items['syntax_errors'] = '\n'.join(syntax_err)
                        report_items['time'] = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
                        print(report_items)
                        test_s = Syntax(time=report_items['time'],
                                        version=version,
                                        prog_id=prog_id,
                                        err_text=report_items['syntax_errors'],
                                        count=report_items['syntax_count'],
                                        score=report_items['code_score'],
                                        )
                        test_s.save()
                    else:
                        continue
                else:
                    continue
    except:
        print('Syntax_analyse_error')
