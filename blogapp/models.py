from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# import된 models.Model을 매개변수로 받고 클래스안에 제목,날짜,내용으로 구성
class Blog(models.Model):
    # CharField -> 문자로 구성되어 있는 항목
    title = models.CharField(max_length = 100)
    # auto_now_add = True를 지정해주어 따로 작성자가 값을 입력하지 않아도 현재 시간에 맞춰서 입력됨
    pub_date = models.DateTimeField(auto_now_add = True)
    # 장고에서 User모델을 기본적으로 제공함
    # ForeignKey는 외래키라는 뜻으로 새로 import한 User 객체를 지정해줌
    # DB는 테이블마다 주키(Primary Key)가 있는데 author 항목처럼 User 외래키를 설정하면 User 테이블의 주키를 참조하게 됨
    # 즉, admin page에서 Users에 들어가면 우리가 설정한 관리자 계쩡이 등록되어 있는데, 우리는 이 계정 정보를 가져오고 이 값을 바탕으로 하여 author 항목을 설정
    # 나머지 인자들은 User 테이블에서 값이 삭제되면 author 항목도 영향을 받아 삭제가 됨
    # 기본값을 본인의 관리자 계정으로 설정
    author = models.ForeignKey(User, on_delete = True, null = True, default = 1)
    body = models.TextField()