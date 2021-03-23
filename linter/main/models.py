from django.db import models

class Progs(models.Model):
    filename = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default="not_runned")
    version = models.IntegerField(default=0)
    def get_status(self):
        return self.status

    def get_version(self):
        return self.version

class Syntax(models.Model):
    prog = models.ForeignKey(Progs, on_delete=models.CASCADE)
    time = models.CharField(max_length=200, default='')
    version = models.IntegerField(default=0)
    err_text = models.CharField(max_length=1000)
    score = models.CharField(max_length=200)
    count = models.IntegerField()

    def get_dict(self):
        return {'version': self.version,
                'err_text': self.err_text,
                'score': self.score,
                'count': self.count
                }

