from django import forms
from .models import Blog, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# 장고에서 기본적으로 지원하는 forms
# 블로그를 생성할 것
class CreateBlog(forms.ModelForm):
    # 장고에서 Meta클래스는 내부 클래스로 활용되며, 이는 기본 필드의 값을 재정의할 때 사용
    class Meta:
        # Blog로부터 모델을 가져오고 그 중 title,pub_date,body를 가져옴
        model = Blog
        # pub_date는 자동입력되게 하여 삭제함
        fields = ['title', 'author', 'body']

        widgets = {
            'title' : forms.TextInput (
                # attrs = 속성, 폼에 적용되는 css의 class 지정
                attrs={'class': 'form-control', 'style': 'width: 100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'author': forms.Select (
                attrs={'class': 'custom-select'},
            ),
            'body': forms.CharField(widget=CKEditorUploadingWidget()),
        }

# 댓글 폼 작성
class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 내용을 입력할 것이기 때문에 comment_textfield 필드만 가져옴
        fields = ['comment_textfield']
        widgets = {
            # 댓글 입력 폼은 html에서 Textarea 형태의 폼이기 때문에 rows와 cols를 지정하였고, 부트스트랩의 css클래스인 form-control을 활용함
            'comment_textfield': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40})
        }