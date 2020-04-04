
from django.urls import path,include

urlpatterns = [
    path("call/",include('study.urls')),
    path("student/",include('stud.urls')),
    path("faculty/",include('faculty.urls'))
]
