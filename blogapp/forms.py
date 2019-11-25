from django import forms
from .models import Blog

# 장고에서 기본적으로 지원하는 forms
# 블로그를 생성할 것
class CreateBlog(forms.ModelForm):
    # 장고에서 Meta클래스는 내부 클래스로 활용되며, 이는 기본 필드의 값을 재정의할 때 사용
    class Meta:
        # Blog로부터 모델을 가져오고 그 중 title,pub_date,body를 가져옴
        model = Blog
        # pub_date는 자동입력되게 하여 삭제함
        fields = ['title', 'author', 'body']