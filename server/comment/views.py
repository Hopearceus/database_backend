def get_notices(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        moments = Moment.objects.filter(creator=person)
        comments = Comment.objects.filter(mid__in=moments)
        notice_list = []
        for comment in comments:
            notice_list.append({
                'cid': comment.cid,
                'mid': comment.mid.mid,
                'content': comment.content,
                'userId': comment.pid.pid,
                'username': comment.pid.username,
                'userAvatar': comment.pid.avatar_url,
                'createTime': comment.time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'notices': notice_list}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_comments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        # comments = Moment_Person.objects.filter(mid=mid, content__isnull=False).values('id', 'content', 'pid__username', 'time')
        comments = Comment.objects.filter(mid=mid)
        comment_list = []
        for comment in comments:
            comment_list.append({
                'cid': comment.cid,
                'mid': comment.mid.mid,
                'content': comment.content,
                'userId': comment.pid.pid,
                'username': comment.pid.username,
                'userAvatar': comment.pid.avatar_url,
                'createTime': comment.time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'comments': comment_list}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
            content = data.get('content')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        moment = get_object_or_404(Moment, mid=mid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        # comment = Moment_Person.objects.create(mid=moment, pid=person, content=content, time=timezone.now())
        comment = Comment.objects.create(mid=moment, pid=person, content=content, time=timezone.now())
        return JsonResponse({'code': 0, 'message': '评论添加成功', 'data': {'id': comment.cid}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def delete_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        # comment = get_object_or_404(Moment_Person, id=id, content__isnull=False)
        comment = get_object_or_404(Comment, cid=id)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if person.pid == 0 or comment.pid.pid == person.pid or person.pid == comment.mid.creator.pid:
            comment.delete()
            return JsonResponse({'code': 0, 'message': '评论已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此评论'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)