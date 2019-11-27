from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlog
from .models import Blog
# Create your views here.

def index(request):
    return render(request, 'index.html')

def blogMain(request):
    # models를 import하고 DB에 저장된 객체를 모두 가리키는 객체 blogs 생성
    blogs = Blog.objects.all()
    # 객체 blogs를 blogMain.html에 보내줌
    return render(request, 'blogMain.html', {'blogs': blogs})

def createBlog(request):

    if request.method == 'POST':
        form = CreateBlog(request.POST)

        if form.is_valid():
            form.save()
            # redirect() -> render()와 비슷하지만 템플릿에 값을 전달하는 목적이 아닌 단순히 특정 url혹은 프로젝트내의 문서로 이동시키고 할 때
            return redirect('blogMain')
        else:
            return redirect('index')
    else:
        form = CreateBlog()
        return render(request, 'createBlog.html', {'form' : form})

    # [createBlog.html]에서 [저장]을 누르면 데이터들이 POST식으로 넘어옴
    # 만약 POST방식으로 넘어오지 않았다면 그냥 단순히 글쓰기 버튼을 눌러서 들어온 것이 됨
    # POST방식으로 넘어오면 CreateBlog() 폼에 값을 전달한 상태로 form 객체를 만듬
    # 그 폼 데이터들이 올바른 형식이면 form.is_valid() 데이터베이스에 저장을 함(form.save())
    # 그 후에 블로그 메인 화면으로 이동(redirect('blogMain'))

def detail(request, blog_id):
    # get_object_or_404 -> 모델로부터 객체를 받을 때 겍체가 있으면 받고, 없을 시 404에러 나오게 함
    # 블로그 글 객체를 판별하기 위해 blog_id값을 매개변수로 받고, pk= 값에 대입함, 이는 주키(primary key)를 판별하기 위한 작업
    blog_detail = get_object_or_404(Blog, pk = blog_id)

    return render(request, 'deatil.html', {'blog_detail': blog_detail})