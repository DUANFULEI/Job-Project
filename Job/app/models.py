

# Create your models here.
from django.db import models

# Create your models here.
class Jobs(models.Model):

    position = models.CharField('职位',max_length=20)
    company = models.CharField('公司',max_length=20)
    pay_a = models.IntegerField('最低薪资')
    pay_b = models.IntegerField('最高薪资')
    address = models.CharField('公司地址',max_length=20)
    job_term = models.TextField('入职要求')
    job_des = models.TextField('描述信息')

    def __str__(self):
        return self.position