
# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.
from app.models import Jobs
from django.template import loader
from django.db.models import Q
import json
from app.zhilianzhaopin_echarts import views
import pymongo



client = pymongo.MongoClient('localhost',port=27017)
db = client.jonfenlei
coll = db.content
# 课程列表首页
from django.views import View
def zhilianzhaopin_show(req):
    msg = req.POST.get('kw', '')
    return render(req,'list.html',{'msg':msg})

class ListView(View):
    def search_city(self,city,jobs):
        if city=='全国':
            jobs = jobs
        else:
            jobs = jobs.filter(
                Q(address__icontains=city)
            )
        return jobs

    def search_job(self,job,jobs):
        # print(job)
        if job == '不限':
            jobs = jobs
        elif job == 'web开发':
            job_in = 'python ' + job

        else:
            if job == 'web开发':
                job_in = 'python ' + job
            else:
                job_in = 'python' + job
            lt = []
            res = coll.find({'category':job_in})
            # print(type(res))
            for i in res:
                lt.append(i["_id"])
            # print(lt)
            jobs = jobs.filter(Q(id__in = lt))
        return jobs


    def search_wage(self,wage,jobs):
        print(wage)
        if wage == '不限':
            jobs = jobs
        elif wage=='7k以下':
            jobs = jobs.filter(
                Q(pay_b__lt=7)
            )
        elif wage == '20k以上':

            jobs = jobs.filter(
                Q(pay_a__gt=20)
            )
        else:
            wage_low = wage.split('-')[0].strip('k')
            wage_high = wage.split('-')[1].strip('k')
            jobs = jobs.filter((Q(pay_a__gt=wage_low)&Q(pay_b__lt=wage_high)))
        return jobs

    def search_exp(self,exp,jobs):
        if exp == '工作经验':
            jobs = jobs
        else:
            jobs = jobs.filter(Q(job_term__icontains=exp))
        return jobs

    def search_edu(self,edu,jobs):
        if edu == '学历要求':
            jobs = jobs
        else:
            jobs = jobs.filter(Q(job_term__icontains=edu))
        return jobs

    def search_keywords(self,search_keywords,jobs):
        if search_keywords.strip() == '':
            jobs = jobs
        else:
            jobs = jobs.filter(Q(position__icontains=search_keywords)|Q(job_des__icontains=search_keywords))
        return jobs


    def post(self, request, p):
        city = request.POST.get('city', '').strip()
        wage = request.POST.get('wage', '').strip()
        edu = request.POST.get('edu', '').strip()
        exp = request.POST.get('exs', '').strip()
        job = request.POST.get('job','').strip()
        search_keywords = request.POST.get('kw', '').strip()
        p = request.POST.get('page', '')
        # print(p)
        jobs = Jobs.objects.all()
        jobs = self.search_city(city, jobs)
        jobs = self.search_keywords(search_keywords, jobs)
        jobs = self.search_edu(edu, jobs)
        jobs = self.search_exp(exp, jobs)
        jobs = self.search_wage(wage, jobs)
        jobs = self.search_job(job,jobs)
        paginator = Paginator(jobs, 20)
        page_jobs = paginator.page(p)
        result_list = []
        for i in page_jobs:
            if i.pay_a == -1:
                wage = '薪资面议'
            else:
                wage = str(i.pay_a) + 'k-' + str(i.pay_b) + 'k'
            s = {'id':i.id,'job_title': i.position,'wage':wage, 'location': i.address, 'work_experience': i.job_term,
                 'education': i.job_term, 'company_name': i.company}
            result_list.append(json.dumps(s))
        return JsonResponse({"msg": result_list, 'num_page': paginator.num_pages, 'page': int(p)})

def mian(request):
    return render(request, 'zhuye.html')

def left_show(request):
    return render(request, 'lift.html')

def top_show(request):
    return render(request, 'top.html')

REMOTE_HOST = "https://pyecharts.github.io/assets/js"
view = views()

def index(request):
    template = loader.get_template('index.html')
    x = view.work_experience()

    context = dict(
        myechart=x.render_embed(),
        host=REMOTE_HOST,
        script_list=x.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def index1(request):
    template = loader.get_template('index.html')
    x = view.location()

    context = dict(
        myechart=x.render_embed(),
        host=REMOTE_HOST,
        script_list=x.get_js_dependencies()
    )
    return HttpResponse(template.render(context, request))

def index2(request):
    return render(request,'wordcloud.html')


def work_detail(req,n):
    job = Jobs.objects.get(id=n)
    if job.pay_a == -1:
        job.pay_a = '薪资面议'
    else:
        job.pay_a = str(job.pay_a)+'k-'+str(job.pay_b)+'k'

    job.job_des = job.job_des.split('工作地址')[0]
    return render(req,'job_detail.html',context={'msg':job})