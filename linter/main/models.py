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
    test_passed=models.BooleanField(default=False)
    file = models.CharField(max_length=200, default='')
    time = models.CharField(max_length=200, default='')
    version = models.IntegerField(default=0)
    err_text = models.CharField(max_length=1000)
    score = models.CharField(max_length=200)
    count = models.IntegerField()

