from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

baseUrl = "https://www.shiyanlou.com/api/v2/"

# localhost 不能携带cookies, 不重写 requests.get/post 强行携带cookies 了。
# 只按需给某些需要cookies的链接带上cookies吧。
# 当然用cookies不能传递,还是需要带在POST/GET参数中。

# === 里面是登录后解锁的内容。

# 这样有安全性问题.
# localhost下也没法传递cookies.
def getSessionFromGetOrPost(data):

    try:
        data.get('session')
    except:
        data = json.loads(data)

    if data:
        return {'session': data.get('session')}
    
    return {'session': ''}


# 课程部分
def courseUserStatus(request):
    # courses/userstatus/?course_ids=1
    # 需要cookies.
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        params = {'user_id': request.GET.get('user_id'), 'course_ids': request.GET.get('course_ids')}
    else:
        params = {'course_ids': request.GET.get('course_ids')}

    content = requests.get(f"{baseUrl}courses/userstatus/", params=params, cookies=cookies)

    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def follow(request, courseId):
    # PUT 方式提交的会关注某一课程
    # DELETE 则是取消关注
    # courses/1/follow/
    # 需要cookies.
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    if request.method == "PUT":
        response = requests.put(f"{baseUrl}courses/{courseId}/follow", cookies=cookies)
    else:
        response = requests.delete(f"{baseUrl}courses/{courseId}/follow", cookies=cookies)

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
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    content = requests.post(f"{baseUrl}courses/{courseId}/join/", cookies=cookies)    
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
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    if request.method == 'GET':
        content = requests.get(f"{baseUrl}user/", cookies=cookies)
        return JsonResponse(content.json(), safe=False)
    elif request.method == 'PATCH':
        data = request.body.decode()
        data = json.loads(data)
        data.pop('session')
        # print(data)
        content = requests.patch(f"{baseUrl}user/", data=json.dumps(data), cookies=cookies, headers={
            'Content-Type': 'application/json'
            })
        # print(content.text)
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
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    if request.method == 'POST':
        content = requests.post(f"{baseUrl}user/checkin/", cookies=cookies)
    elif request.method == 'GET':
        content = requests.get(f"{baseUrl}user/checkin/", cookies=cookies)
    
    return JsonResponse(content.json(), safe=False)


@csrf_exempt
def changeEmail(request):
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    data = json.loads(request.body.decode())
    data.pop('session')

    content = requests.post(f"{baseUrl}user/change-email/", data=json.dumps(data), cookies=cookies, headers={
            'Content-Type': 'application/json'
            })
    try:
        return JsonResponse(content.json(), safe=False)
    except:
        return HttpResponse(200)

@csrf_exempt
def changePassword(request):
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    data = json.loads(request.body.decode())
    data.pop('session')

    content = requests.post(f"{baseUrl}user/change-password/", data=json.dumps(data), cookies=cookies, headers={
            'Content-Type': 'application/json'
            })

    try:
        return JsonResponse(content.json(), safe=False)
    except:
        return HttpResponse(200)

@csrf_exempt
def changePassword(request):
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    data = json.loads(request.body.decode())
    data.pop('session')

    content = requests.post(f"{baseUrl}user/change-password/", data=json.dumps(data), cookies=cookies, headers={
            'Content-Type': 'application/json'
            })

    try:
        return JsonResponse(content.json(), safe=False)
    except:
        return HttpResponse(200)

@csrf_exempt
def mailSettings(request):
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    if request.method == 'GET':
        content = requests.get(f"{baseUrl}user/mail-settings/", cookies=cookies)
        # return JsonResponse(content.json(), safe=False)

    elif request.method == 'PUT':
        data = json.loads(request.body.decode())
        data.pop('session')
        content = requests.put(f"{baseUrl}user/mail-settings/", data=json.dumps(data), cookies=cookies, headers={
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
    content = requests.post(f"{baseUrl}auth/login/", data=request.body.decode(), headers={
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
        cookies = getSessionFromGetOrPost(request.GET)
        if not cookies.get('session'):
            cookies = getSessionFromGetOrPost(request.body.decode())

        # data = request.body.decode()
        content = requests.post(f"{baseUrl}comments/", data=request.body.decode(), cookies=cookies, headers={'Content-Type': 'application/json;charset=UTF-8'})
        return JsonResponse(content.json(), safe=False) 

def commentsUserstatus(request):
    # 需要cookies。
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    content = requests.get(f"{baseUrl}comments/userstatus/", params={'comment_ids': request.GET.get('comment_ids')}, cookies=cookies)
    return JsonResponse(content.json(), safe=False)

@csrf_exempt
def deleteComment(request, commentId):
    cookies = getSessionFromGetOrPost(request.GET)
    if not cookies.get('session'):
        cookies = getSessionFromGetOrPost(request.body.decode())

    response = requests.delete(f"{baseUrl}comments/{commentId}/", cookies=cookies)

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
        cookies = getSessionFromGetOrPost(request.GET)
        if not cookies.get('session'):
            cookies = getSessionFromGetOrPost(request.body.decode())

        response = requests.post(f"{baseUrl}questions/{questionId}/answers/", data=request.body.decode(), cookies=cookies, headers={'Content-Type': 'application/json;charset=UTF-8'})

        return JsonResponse(response.json(), safe=False)        


def recentLouplus(request):
    content = requests.get(f"{baseUrl}fringe/recent-louplus-courses/")
    return JsonResponse(content.json(), safe=False)

def recentActivities(request):
    content = requests.get(f"{baseUrl}fringe/recent-activities/")
    return JsonResponse(content.json(), safe=False)

def questions(request):
    content = requests.get(f"{baseUrl}questions/", params=request.GET)
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

def labreports(request):
    content = requests.get(f"{baseUrl}labreports/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def library(request):
    content = requests.get(f"{baseUrl}library/")
    return JsonResponse(content.json(), safe=False)

def libraryBooks(request):
    content = requests.get(f"{baseUrl}library/books/", params=request.GET)
    return JsonResponse(content.json(), safe=False)

def search(request):
    content = requests.get(f"{baseUrl}search/", params=request.GET)
    return JsonResponse(content.json(), safe=False)
