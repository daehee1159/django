from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlog
from .models import Blog
from .models import Comment
from .forms import BlogCommentForm
# requests 패키지 설치 후 import
import requests
# json 형태로 변환하는 작업을 위한
import json
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
            redirect_uri = 'http://127.0.0.1:8000/oauth'

            login_request_url += 'client_id=' + client_id
            login_request_url += '&redirect_uri=' + redirect_uri
            # 나에게 보내기 동적동의 부분 + &scope=talk_message 추가됨
            login_request_url += '&response_type=code&scope=talk_message'
            # client_id와 redirect_uri 값을 세션으로 보냄
            request.session['client_id'] = client_id
            request.session['redirect_uri'] = redirect_uri

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
    # client_id와 redirect_uri 값을 세션으로 보냈으니 oauth()에서 그 세션 값을 받아옴
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    # code값을 추가하여  access_token을 얻을 수 있느 최종 uri
    access_token_request_uri = 'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&'

    access_token_request_uri += 'client_id=' + client_id
    access_token_request_uri += '&redirect_uri=' + redirect_uri
    access_token_request_uri += '&code=' + code

    print(access_token_request_uri)

    # requests패키지를 이용하여 access_token json 데이터 파싱
    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    print('access_token = ' + access_token)
    # requests패키지를 이용하여 user_profile json 데이터 파싱
    user_profile_info_uri = "https://kapi.kakao.com/v1/api/talk/profile?access_token="
    user_profile_info_uri += str(access_token)

    user_profile_info_uri_data = requests.get(user_profile_info_uri)
    user_json_data = user_profile_info_uri_data.json()
    nickName = user_json_data['nickName']
    profileImageURL = user_json_data['profileImageURL']
    thumbnailURL = user_json_data['thumbnailURL']

    print("nickName = " + str(nickName))
    print("profileImageURL = " + str(profileImageURL))
    print("thumbnailURL = " + str(thumbnailURL))

    # 기본 템플릿 보내기 -> 피드템플릿 보내기 request
    # 해당 데이터를 요청하기 위해 requests 패키지의 request() 함수를 이용
    # request()함수는 method, uri, 기타인자를 요구함
    # request(method, uri, kwargs)
    template_dict_data = str({
        "object_type": "feed",
        "content": {
            "title": "디저트 사진",
            "description": "아메리카노, 빵, 케익",
            "image_url": "http://mud-kage.kakao.co.kr/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        },
        "social": {
            "like_count": 100,
            "comment_count": 200,
            "shared_count": 300,
            "view_count": 400,
            "subscriber_count": 500
        },
        "buttons": [
            {
                "title": "웹으로 이동",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            }
        ]
    })
    # print(template_dict_data)

    # 요청할 uri 변수 생성
    kakao_to_me_uri = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'

    # header 구성, 위에서 얻은 access_token과 함께 구성
    # Content-Type은 여러 종류가 있지만 지금은 template_object= 와 같이 키 = 값 의 형태로 전달해야함
    # POST로 전송하므로 application/x-www-form-urlencoded 타입을 사용
    # POST로 데이터를 전송할 때 multipart/form-data 의 경우 파일의 형태가 포함될 경우에 사용
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + access_token,
    }

    # json.dumps() 함수를 사용하면 딕셔너리를 JSON 데이터 형태로 변환해줌
    # template_object 변수와 함께 보내야 되므로 문자열로 구성
    template_json_data = "template_object=" + str(json.dumps(template_dict_data))
    # print(template_json_data)

    # template_json_data는 print()로 출력해보면 ""로 감싸고 있으므로 이를 없애줌
    template_json_data = template_json_data.replace("\"", "")
    # template_json_data를  JSON 형태로 인식하기 위한 작업
    # JSON 데이터는 키 값이 ''로 감싸고 있는 것이 아니라 ""로 감싸고 있기 때문
    template_json_data = template_json_data.replace("'", "\"")

    response = requests.request(method="POST", url=kakao_to_me_uri, data=template_json_data, headers=headers)
    print(template_json_data)
    print(response.json())

    return redirect('blogMain')