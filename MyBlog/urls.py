"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import blogapp.views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blogapp.views.index, name='index'),
    path('blogMain/', blogapp.views.blogMain, name='blogMain'),
    path('blogMain/createBlog/', blogapp.views.createBlog, name='createBlog'),
    # ckeditor가 url을 참조할 수 있도록 설정
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # int:blog_id -> views.detail 함수에 넘길 블로그 글 번호
    # blogMain/detail/1 은 블로그 글 1번에 대한 detail 페이지가 나오게 됨
    path('blogMain/detail/<int:blog_id>', blogapp.views.detail, name='detail'),
    path('oauth/', blogapp.views.oauth, name='oauth'),
]
# MEDIA 경로를 참조하기 위함
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)