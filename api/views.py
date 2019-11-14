from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import re
import json

import requests

def getToken():
    t = requests.get('https://www.shiyanlou.com')

    if t.text:
        # (?# print(re.findall(r'token:"(.*?)"', t.text)[0]))
        return re.findall(r'token:"(.*?)"', t.text)[0]
    else:
        print('No Token')
        return ''

token = ''

baseUrl = "https://www.shiyanlou.com/api/v2/"

# 这里一开始没有预留接口，做一个覆盖方式的header重写。

post = requests.post
get = requests.get

def addTokenHeader(methods='GET'):
    # 装饰器
    def inner(*args, **kwargs):
        global token
        if not kwargs.get('headers'):
            kwargs['headers'] = {}

        # 实验楼添加了一个token，目前不知道如何生成，直接抓取的生成好的。
        # 生效时间未知。
        # 限制条件未知。
        kwargs['headers']['x-syl-client-token'] = token
        
        if methods == 'GET':
            result = get(*args, **kwargs)
        elif methods == 'POST':
            result = post(*args, **kwargs)

        try:
            if result.json()['client_authentication_failed']:
                # 验证token失败，重新尝试请求token
                token = getToken()
                kwargs['headers']['x-syl-client-token'] = token                
                if methods == 'GET':
                    result = get(*args, **kwargs)
                elif methods == 'POST':
                    result = post(*args, **kwargs)

        except:
            pass

        return result

    return inner

requests.post = addTokenHeader(methods='POST')
requests.get = addTokenHeader(methods='GET')


# 一些额外的东西
@csrf_exempt
def getQiniuToken(request):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())
    
    # data = json.loads(request.body.decode())
    # data.pop('session')

    content = requests.post(f'{baseUrl}services/qiniu/token/', data=request.body, cookies=request.COOKIES, headers={
        'Content-Type': 'application/json;charset=UTF-8'
        })
    return JsonResponse(content.json(), safe=False)


# 课程部分
def courseUserStatus(request):
    # courses/userstatus/?course_ids=1
    # 需要cookies.
    content = requests.get(f"{baseUrl}courses/userstatus/", params=request.GET, cookies=request.COOKIES)

    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def follow(request, courseId):
    # PUT 方式提交的会关注某一课程
    # DELETE 则是取消关注
    # courses/1/follow/
    # 需要cookies.
    if request.method == "PUT":
        response = requests.put(f"{baseUrl}courses/{courseId}/follow", cookies=request.COOKIES)
    else:
        response = requests.delete(f"{baseUrl}courses/{courseId}/follow", cookies=request.COOKIES)

    if int(response.status_code) == 200 or int(response.status_code) == 204:
        return HttpResponse()
    return HttpResponse(status_code=500)

# 进行实验部分.
# 这一部分未计划接入.
# 就当前来说join有用，其他的暂且不用。
@csrf_exempt
def join(request, courseId):
    # courses/1/join
    # 需要用POST提交.
    # 需要cookies.
    # 无返回数据，200应该就是加入成功了。
    content = requests.post(f"{baseUrl}courses/{courseId}/join/", cookies=request.COOKIES)    
    # return JsonResponse(content.json(), safe=False)
    if int(content.status_code) == 200 or int(content.status_code) == 204:
        return HttpResponse()
    return HttpResponse(status_code=500)

def labtask(request):
    # /labtask
    # 需要cookies.
    # 返回当前正在试验中的数据。
    pass

# 关于用户的数据,包括仅登录后能用的和只需要userId就可以使用的。
@csrf_exempt
def userInfo(request):
    # user/
    # 仅需cookies, cookies 也是必须的。
    if request.method == 'GET':
        content = requests.get(f"{baseUrl}user/", cookies=request.COOKIES)
        return JsonResponse(content.json(), safe=False)
    elif request.method == 'PATCH':
        content = requests.patch(f"{baseUrl}user/", data=request.body, cookies=request.COOKIES, headers={
            'Content-Type': 'application/json'
            })
        if int(content.status_code) == 200:
            return JsonResponse(content.json(), safe=False)
        else:
            return HttpResponse(content.status_code)

def userInfoWithoutCookies(request, userId):
    content = requests.get(f"{baseUrl}users/{userId}/")

    return JsonResponse(content.json(), safe=False)   

def userStudiedCourses(request, userId):
    # users/1146797/courses/?page_size=5&type=studied
    # 这个无需 cookies.
    content = requests.get(f"{baseUrl}users/{userId}/courses", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def userFollowCourses(request):
    # users/1146797/courses/?userId=1146797&type=followed
    # 无需 cookies.
    pass

def userBoughtCourses(request):
    # users/1146797/courses/?userId=1146797&type=bought
    # 无需 cookies.
    pass

def userPaths(request, userId):
    # users/1146797/paths/
    # 无需 cookies.
    content = requests.get(f"{baseUrl}users/{userId}/paths/")
    return JsonResponse(content.json(), safe=False)

def userLabreports(request, userId):
    # users/1146797/labreports/
    # 无需 cookies.
    content = requests.get(f"{baseUrl}users/{userId}/labreports/")
    return JsonResponse(content.json(), safe=False)

def userQuestion(request):
    # users/1146797/questions/?type=answered
    # 无需 cookies.
    pass

def userQuestionsForOneCourse(request, userId):
    content = requests.get(f"{baseUrl}users/{userId}/questions/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def checkin(request):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    if request.method == 'POST':
        content = requests.post(f"{baseUrl}user/checkin/", cookies=request.COOKIES)
    elif request.method == 'GET':
        content = requests.get(f"{baseUrl}user/checkin/", cookies=request.COOKIES)
    
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def changeEmail(request):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    # data = json.loads(request.body.decode())
    # data.pop('session')

    content = requests.post(f"{baseUrl}user/change-email/", data=request.body, cookies=request.COOKIES, headers={
            'Content-Type': 'application/json'
            })
    try:
        return JsonResponse(content.json(), safe=False)
    except:
        return HttpResponse(200)

@csrf_exempt
def changePassword(request):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    # data = json.loads(request.body.decode())
    # data.pop('session')

    content = requests.post(f"{baseUrl}user/change-password/", data=request.body, cookies=request.COOKIES, headers={
            'Content-Type': 'application/json'
            })

    try:
        return JsonResponse(content.json(), safe=False)
    except:
        return HttpResponse(200)

@csrf_exempt
def changePassword(request):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    # data = json.loads(request.body.decode())
    # data.pop('session')

    content = requests.post(f"{baseUrl}user/change-password/", data=request.body, cookies=request.COOKIES, headers={
            'Content-Type': 'application/json'
            })

    try:
        return JsonResponse(content.json(), safe=False)
    except:
        return HttpResponse(200)

@csrf_exempt
def mailSettings(request):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    if request.method == 'GET':
        content = requests.get(f"{baseUrl}user/mail-settings/", cookies=request.COOKIES)
        # return JsonResponse(content.json(), safe=False)

    elif request.method == 'PUT':
        content = requests.put(f"{baseUrl}user/mail-settings/", data=request.body, cookies=request.COOKIES, headers={
            'Content-Type': 'application/json'
            })

    return JsonResponse(content.json(), safe=False)

# 教程和比赛,暂未加入计划。
# users/1146797/contests/?page_size=15
# users/1146797/books/?userId=1146797&type=marked
# ===

# auth
@csrf_exempt
def login(request):
    content = requests.post(f"{baseUrl}auth/login/", data=request.body, headers={
        'Content-Type': 'application/json'
        })
    response = JsonResponse(content.json(), safe=False)
    # 登陆失败
    if not content.json().get('comet_token'):
        return response
    # 登录成功, 设置cookies.

    # response['Access-Control-Allow-Credentials'] = True
    # response['Access-Control-Allow-Origin'] = "http://localhost:8080"
    # for cookieName, cookieValue in content.cookies:
    # response.set_cookie('session', content.cookies['session'])
    # 似乎chrome不允许设置带有端口号的cookies. 直接把 session 用Json传了吧...
    # 用Js设置。
    with_session = content.json()
    with_session['session'] = content.cookies['session']
    return JsonResponse(with_session, safe=False)

# comment
@csrf_exempt
def comment(request):
    # 以 GET 提交。
    if request.method == 'GET':
        content = requests.get(f"{baseUrl}comments/", params=request.GET)
        return JsonResponse(content.json(), safe=False)
    # 以 POST 提交 需要 cookies.
    elif request.method == 'POST':
        # content: "o"
        # topic_id: 1
        # topic_type: "course"
        # cookies = getSessionFromGetOrPost(request.GET)
        # if not cookies.get('session'):
        #     cookies = getSessionFromGetOrPost(request.body.decode())

        # data = request.body.decode()
        content = requests.post(f"{baseUrl}comments/", data=request.body, cookies=request.COOKIES, headers={'Content-Type': 'application/json;charset=UTF-8'})
        return JsonResponse(content.json(), safe=False) 

def commentsUserstatus(request):
    # 需要cookies。
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    content = requests.get(f"{baseUrl}comments/userstatus/", params={'comment_ids': request.GET.get('comment_ids')}, cookies=request.COOKIES)
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def deleteComment(request, commentId):
    # cookies = getSessionFromGetOrPost(request.GET)
    # if not cookies.get('session'):
    #     cookies = getSessionFromGetOrPost(request.body.decode())

    response = requests.delete(f"{baseUrl}comments/{commentId}/", cookies=request.COOKIES)

    if int(response.status_code) == 200 or int(response.status_code) == 204:
        return HttpResponse()
    return HttpResponse(status_code=500)

# path
def stages(request, pathId):
    content = requests.get(f"{baseUrl}paths/{pathId}/stages")
    return JsonResponse(content.json(), safe=False)

def path(request, pathId):
    content = requests.get(f"{baseUrl}paths/{pathId}")
    return JsonResponse(content.json(), safe=False)

def paths(request):
    content = requests.get(f"{baseUrl}paths")
    return JsonResponse(content.json(), safe=False)

def pathUserstatus(request):
    content = requests.get(f"{baseUrl}paths/userstatus/", params=request.GET, cookies=request.COOKIES)
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def pathJoin(request, pathId):
    if request.method == 'POST':
        content = requests.post(f"{baseUrl}paths/{pathId}/join/", cookies=request.COOKIES)
    elif request.method == 'DELETE':
        content = requests.delete(f"{baseUrl}paths/{pathId}/join/", cookies=request.COOKIES)
    
    if int(content.status_code) < 299:
        return HttpResponse(content.status_code)

    return JsonResponse(content.json(), safe=False)

# qa
def relatedQuestions(request, questionId):
    content = requests.get(f"{baseUrl}questions/{questionId}/related-questions/")
    return JsonResponse(content.json(), safe=False)

def question(request, questionId):
    content = requests.get(f"{baseUrl}questions/{questionId}")
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def questionAnswers(request, questionId):
    if request.method == "GET":
        content = requests.get(f"{baseUrl}questions/{questionId}/answers/", params=request.GET)
        return JsonResponse(content.json(), safe=False)
    else:
        # cookies = getSessionFromGetOrPost(request.GET)
        # if not cookies.get('session'):
        #     cookies = getSessionFromGetOrPost(request.body.decode())

        response = requests.post(f"{baseUrl}questions/{questionId}/answers/", data=request.body, cookies=request.COOKIES, headers={'Content-Type': 'application/json;charset=UTF-8'})

        return JsonResponse(response.json(), safe=False)        


def recentLouplus(request):
    content = requests.get(f"{baseUrl}fringe/recent-louplus-courses/")
    return JsonResponse(content.json(), safe=False)

def recentActivities(request):
    content = requests.get(f"{baseUrl}fringe/recent-activities/")
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def questions(request):
    if request.method == "GET":
        content = requests.get(f"{baseUrl}questions/", params=request.GET)
        return JsonResponse(content.json(), safe=False)
    elif request.method == 'POST':
        content = requests.post(f"{baseUrl}questions/", data=request.body, cookies=request.COOKIES, headers={'Content-Type': 'application/json;charset=UTF-8'})
        return JsonResponse(content.json(), safe=False)


# home
def indexPaths(request):
    content = requests.get(f"{baseUrl}index/paths")
    return JsonResponse(content.json(), safe=False)

def indexBootcamps(request):
    content = requests.get(f"{baseUrl}index/bootcamps")
    return JsonResponse(content.json(), safe=False)

def classficationCourses(request):
    content = requests.get(f"{baseUrl}index/classfication-courses/")
    return JsonResponse(content.json(), safe=False)

def louplus(request):
    content = requests.get(f"{baseUrl}index/louplus/")
    return JsonResponse(content.json(), safe=False)

def indexBanner(request):
    content = requests.get(f"{baseUrl}index/banner-pictures/")
    return JsonResponse(content.json(), safe=False)

def indexCategories(request):
    content = requests.get("http://www.shiyanlou.com/api/v2/index/categories/")
    return JsonResponse(content.json(), safe=False)

# courses 
def courseLabs(request, courseId):
    content = requests.get(f"{baseUrl}courses/{courseId}/labs")
    return JsonResponse(content.json(), safe=False)

def course(request, courseId):
    content = requests.get(f"{baseUrl}courses/{courseId}")
    return JsonResponse(content.json(), safe=False)

def categories(request):
    content = requests.get("http://www.shiyanlou.com/api/v2/courses/categories/")
    return JsonResponse(content.json(), safe=False)

def courses(request):
    content = requests.get("http://www.shiyanlou.com/api/v2/courses/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# reports
def labreports(request):
    content = requests.get(f"{baseUrl}labreports/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def labreport(request, reportId):
    content = requests.get(f"{baseUrl}labreports/{reportId}/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def labreportLearnData(request, reportId):
    content = requests.get(f"{baseUrl}labreports/{reportId}/learn-data/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def labreportRelated(request, reportId):
    content = requests.get(f"{baseUrl}labreports/{reportId}/related/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# library
def library(request):
    content = requests.get(f"{baseUrl}library/")
    return JsonResponse(content.json(), safe=False)

def libraryBooks(request):
    content = requests.get(f"{baseUrl}library/books/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# search
def search(request):
    content = requests.get(f"{baseUrl}search/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# live
def liveCourses(request):
    content = requests.get(f"{baseUrl}live-courses/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# contests
def contests(request):
    content = requests.get(f"{baseUrl}contests/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def contestRank(request, contestName):
    content = requests.get(f"{baseUrl}contests/{contestName}/rank/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def contestsRank(request):
    content = requests.get(f"{baseUrl}contests/rank/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

# challenges
def challenges(request):
    content = requests.get(f"{baseUrl}challenges/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def challengesTags(request):
    content = requests.get(f"{baseUrl}challenges/tags/")
    return JsonResponse(content.json(), safe=False)

def challengesUserStatus(request):
    content = request.get(f"{baseUrl}challenges/userstatus/", params=request.GET)
    return JsonResponse(content.json(), safe=False)
