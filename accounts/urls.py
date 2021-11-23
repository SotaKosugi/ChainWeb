from django.urls import path
from . import views

#app_name='accounts'

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('index/',views.IndexView.as_view(), name="index"),
    path('study/',views.Study,name='study'),
    path('res1/',views.Res1,name='res1'),
    path('res2/',views.Res2,name='res2'),
    path('upload/', views.Upload, name='upload'),
    path('imagelog/',views.ImageLogView.as_view(),name='imagelog'),
    #path('home/',views.Home,name='home'),
    path('goalconfig/',views.GoalConfig,name='goalconfig'),
    path('config/',views.Config,name='config'),
    path('studylog/',views.StudyLogView.as_view(),name='studylog'),
    path('plot/', views.get_svg, name='plot'),
    #path('videocheck/', views.videocheck, name='videocheck'),
]