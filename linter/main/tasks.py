from pylint import epylint as lint
from .models import Syntax
from datetime import datetime
import os

def validation_path(file_path):
    py_count = 0
    for dirname, dirnames, filenames in os.walk(file_path):
        for filename in filenames:
            if '.py' in filename:
                py_count += 1
    if py_count == 0:
        return False
    else:
        return True


def syntax_test_2(file_path, prog_id, version):
    try:
        if validation_path(file_path) == False:
            return -2
        else:
            returns_count = 0
            files_count = 0
            for dirname, dirnames, filenames in os.walk(file_path):
                for filename in filenames:
                    if '.py' in filename and '.pyc' not in filename and '__init__' not in filename:
                        if 'venv' not in dirname:
                            cur_file = os.path.join(dirname, filename)
                            report_items = {}
                            syntax_err = []
                            (pylint_stdout, pylint_stderr) = lint.py_run(command_options=cur_file, return_std=True)
                            lints = pylint_stdout.getvalue().split('\n')[1:]
                            for l in lints:
                                if 'warning' in l:
                                    err = l.split(':')
                                    syntax_err.append(f'line({err[1]}) : {err[2]} ')
                                if 'rated' in l:
                                    report_items['code_score'] = l.split('(')[0]
                                else:
                                    continue
                            report_items['syntax_count'] = str(len(syntax_err))
                            report_items['syntax_errors'] = '\n'.join(syntax_err)
                            report_items['time'] = datetime.now().strftime("%d.%m.%Y-%H:%M:%S")
                            returns_count += int(report_items['syntax_count'])
                            test_s = Syntax(time=report_items['time'],
                                            file=filename,
                                            version=version,
                                            prog_id=prog_id,
                                            err_text=report_items['syntax_errors'],
                                            count=report_items['syntax_count'],
                                            score=report_items['code_score'],
                                            )
                            test_s.save()
                            files_count += 1
                        else:
                            continue
                    else:
                        continue
            return returns_count / files_count
    except:
        return -1
