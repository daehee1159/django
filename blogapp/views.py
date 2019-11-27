from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlog
from .models import Blog
from .models import Comment
from .forms import BlogCommentForm
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
    comments = Comment.objects.filter(blog_id = blog_id)

    # 댓글 폼에서 데이터가 POST로 보낸다고 가정
    # 해당 데이터가 POST이면 사용자가 무언가 댓글을 작성하고 데이터를 보낸다는 의미
    # 그게 아니라면 단지 블로그 세부 내용을 확인하기 위함
    # 블로그 세부 내용 확인을 위해 페이지를 열었다면 댓글 폼 객체의 형태만을 생성하여 사용자게에 보여주면 되기 때문에 comment_form 이라는 객체로 받고 context에 추가
    # 이후 context를 보내면 detail.html은 댓글 폼이 추가된 상태로 보여지게 됨
    # 만약 POST로 보내졌다면, 사용자가 제출 버튼을 눌러 데이터를 보냈다는 것이기 때문에 BlogCommentForm 객체의 인자에 POST 데이터를 받음
    # 또한 댓글 폼의 입력 형식이 올바른지 확인하고 clean_data[]형태를 통하여 실제 댓글 폼에 입력된 데이터(comment_textfiled)에 해당되는 것을 받아옴
    # 일련의 작업이 끝나면 터미널에서 내용이 정상적으로 전달되는지 확인하기 위해 print()함

    if request.method == 'POST':
        comment_form = BlogCommentForm(request.POST)

        if comment_form.is_valid():
            content = comment_form.cleaned_data['comment_textfield']

            print(content)

            login_request_url = 'https://kauth.kakao.com/oauth/authorize?'
            client_id = 'cc1c5a4a3f565e37c1a4765025219f73'
            redirect_url = 'http://127.0.0.1:8000/oauth'

            login_request_url += 'client_id=' + client_id
            login_request_url += '&redirect_url=' + redirect_url
            login_request_url += '&response_type=code'

            return redirect(login_request_url)
        else:
            return redirect('blogMain')

    else:
        comment_form = BlogCommentForm()

        context = {
            'blog_detail': blog_detail,
            'comments': comments,
            'comment_form': comment_form
        }

        return render(request, 'detail.html', context)

    # 초기 댓글 버전
    # context = {
    #     'blog_detail': blog_detail,
    #     'comments': comments
    # }
    # return render(request, 'detail.html', context)
    # # return render(request, 'detail.html', {'blog_detail': blog_detail})

def oauth(request):
    code = request.GET['code']
    print('code = ' + str(code))
    return redirect('blogMain')