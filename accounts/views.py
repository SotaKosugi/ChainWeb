from os import environ
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms
from .models import StudentImage, StudentStudyLog, StudentVideo
from django.contrib.auth.decorators import login_required
import json
import matplotlib
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
import ffmpeg
import base64
import datetime
import os

#ログイン処理
class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

#ログアウト処理
class MyLogoutView(LogoutView):
    template_name = "accounts/logout.html"

#ホーム画面の処理
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/new_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #
        if StudentStudyLog.objects.filter(userID=self.request.user.userID).exists():
            context["times"] = StudentStudyLog.objects.get(userID=self.request.user.userID)
        else:
            StudentStudyLog.objects.create(userID=self.request.user.userID, username=self.request.user.username)

        context["goal"] = StudentStudyLog.objects.get(userID=self.request.user.userID)

        return context
  

#勉強画面の処理
@login_required
def Study(request):
    return render(request,'accounts/new_study.html')

#未実装
@login_required
def Res1(request):
    
    user_id = request.user.userID
    user_name = request.user.username

    data = request.body.decode('utf-8')
    
    StudentImage.objects.create(image=data.replace('"',''), userID=user_id, username=user_name)
    
    return redirect('/accounts/index')

#未実装
@login_required
def Res2(request):
    
    user_id = request.user.userID
    user_name = request.user.username

    studyTime = request.body.decode('utf-8')


    #累計の勉強時間を更新  
    now_sum_studyTime = StudentStudyLog.objects.get(userID=user_id)
    sumStudyTime = now_sum_studyTime.sum_study_time + int(studyTime)

    StudentStudyLog.objects.update_or_create(
        userID=user_id, 
                
        defaults={
            "userID":user_id,
            "username":user_name,
            "study_time":studyTime,
            "sum_study_time":sumStudyTime
            } 
    )

    return redirect('/accounts/index')


@login_required
def get_datetime():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) # 日本時刻
    #print(now.strftime('%Y%m%d%H%M%S'))  # yyyyMMddHHmmss形式で出力
    return now.strftime('%Y%m%d%H%M%S')

#勉強動画アップロード時ののポスト
@login_required
def Upload(request):
    if request.method == 'POST' :
        
        #アップロード日時を取得してファイル名に設定する
        print("THIS!!",flush=True)
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) # 日本時刻
        nowtime = now.strftime('%Y_%m_%d_%H_%M_%S')
        InputDirectory = "./media/videos/" + str(request.user.userID) + "_input/" 
        InputUserPath = "./media/videos/" + str(request.user.userID) + "_input/" + "in_" + str(request.user.userID) + "_" + nowtime + ".webm"
        if not os.path.exists(InputDirectory):
            # inputディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(InputDirectory)

        # base64のテキストをbase64のbytes型に変換後、通常のbytes型に変換して保存
        b64video = request.body.decode('utf-8')
       
        webm0 = base64.b64decode((b64video.replace('"','')).encode())
        with open(InputUserPath, 'bw') as f3:
            f3.write(webm0)

        #タイムラプス動画に変換する処理
        OutputDirectory = "./media/videos/" + str(request.user.userID) + "_output/" 
        OutputUserPath = "./media/videos/" + str(request.user.userID) + "_output/" + "out_" + str(request.user.userID) + "_" + nowtime + ".webm"
        VideoPath = "../." + OutputUserPath
        if not os.path.exists(OutputDirectory):
            # outputディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(OutputDirectory)
    
        #タイムラプス動画に変換
        ffmpeg.input(InputUserPath,r=30).output(OutputUserPath).run()

        print("SUCCESS!!",flush=True)
        print(OutputUserPath.lstrip())
       
        #StudentVideoモデルにタイムラプス動画のパスを格納
        StudentVideo.objects.create(videoPath=VideoPath, userID=request.user.userID, username=request.user.username)
        
    return redirect('/accounts/index')

@login_required
def videocheck(request):
    video = {
        "b64video":StudentImage.objects.filter(userID=request.user.userID).latest('published_date')
    }
    return render(request, 'accounts/upload.html',video)


#アップロードした動画を保存して圧縮
def handle_uploaded_file(file_obj):
   
    file_path =  MEDIA_ROOT + '/videos/' + file_obj.name 
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    #タイムラプス動画に変換  
    ffmpeg.input(file_path,r=30).output(MEDIA_ROOT + '/videos/output3.webm').run()
        

#目標設定のポストに対するレスポンス
@login_required
def GoalConfig(request):

    #モデルが存在していなかったら作る
    if not StudentStudyLog.objects.filter(userID=request.user.userID).exists():
        StudentStudyLog.objects.create(userID=request.user.userID,username=request.user.username)

    if request.method == 'POST':

        user_id = request.user.userID
        user_name = request.user.username

        goals_json = request.body.decode('utf-8')

        goals = json.loads(goals_json)

        print(goals,flush=True)
        print(type(goals_json),flush=True)
        print(type(goals),flush=True)
        
        StudentStudyLog.objects.update_or_create(
            userID=user_id, 
            
            defaults={
                "userID":user_id,
                "username":user_name,
                "goal_start":goals['start'],
                "goal_end":goals['end'],
                "study_time":goals['time']
            } 
        )   


@login_required
def Config(request):
    return render(request,'accounts/config.html')    



class StudyLogView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/new_studylog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #
        
        context["videoPath"] = StudentVideo.objects.filter(userID=self.request.user.userID).order_by('-published_date')[:3]
        
        context["goal"] = StudentStudyLog.objects.get(userID=self.request.user.userID)

        return context

class ImageLogView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/image_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #
        
        context["student_images"] = StudentImage.objects.all()

        temp = StudentStudyLog.objects.get(userID=self.request.user.userID)

        data = {
            'jsonTimes':temp.study_time
        }
        
        sent_json = json.dumps(data)
        context["json_times"] = sent_json

        return context


#グラフ作成
def setPlt():
    x = ["5/31~", "6/7~", "6/14~", "6/21~", "6/28~", "7/5~", "7/12~"]
    y = [32, 51, 18, 25, 36, 20, 43]
    fig = plt.figure(figsize=(6, 4), dpi=72,
                 facecolor='white', linewidth=10, edgecolor='skyblue')
    ax = fig.add_subplot(111, title='WeeklyStudyTime', xlabel='Week', ylabel='Time(h)')

    for i in range(len(x)): 
        ax.text(i, y[i], y[i], horizontalalignment='center') 
  
    ax.bar(x,y)


# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

# 実行するビュー関数
def get_svg(request):
    setPlt()  
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response