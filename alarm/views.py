from django.db import transaction
from django.db.models import F
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from alarm.models import Alarm
from apply.models import Apply
from knowhow.models import Knowhow, KnowhowLike, KnowhowReply, KnowhowFile
from lecture.models import LectureReview, Lecture, LectureProductFile
from member.models import Member, MemberProfile
from post.models import PostLike, PostReply, PostFile


class AlarmView(View):
    def get(self, request):
        # 세션에서 멤버정보 가져오기
        member = request.session.get('member')
        # 프로필 사진 정보 가져오기
        member_file = request.session.get('member_files')
        # 읽지않은 알람 정보 필터 후 가져오기
        alarms= Alarm.objects.filter(receiver_id=member.get('id'),alarm_status=False)
        # 화면에서 검사할 알람을 숫자로 전달하기 위함
        alarm_count = len(alarms)
        # 화면에 알람수와 멤버, 프로필 사진 url 넘겨주기
        context = {
            'alarm_count': alarm_count,
            'member': member,
            'memberProfile': member_file[0].get('file_url'),
        }

        return render(request,'alarm/alarm.html', context)


# 알람 목록 API
class AlarmAPI(APIView):
    # js로 page를 받고 get으로 정보 전송

    def get(self, request, page):
        # 페이지당 알람 수와 오프셋, 리미트 계산
        row_count = 8
        offset = (page - 1) * row_count
        limit = page * row_count

        # 현재 멤버의 아이디 가져오기
        member_id = request.session.get('member').get('id')

        # 멤버에게 전달된 알람들 가져오기
        alarms = Alarm.objects.filter(receiver=member_id, alarm_status=False).values()

        # 각 알람에 대한 추가 정보 처리
        for alarm in alarms:
            # 알람의 발신자 정보 가져오기
            sender = Member.objects.filter(id=alarm.get('sender_id')).first()
            # 발신자의 정보 유효성 검사
            alarm['sender'] = sender.member_name if sender else None

            # 발신자 파일 URL 가져오기 또는 기본값 설정
            sender_file = MemberProfile.objects.filter(member_id=alarm.get('sender_id')).values('file_url').first()
            alarm['member_file'] = sender_file.get('file_url') if sender_file else 'file/2024/03/05/blank-image.png'

            # 알람 카테고리에 따라 메시지 생성

            # 내가 개설한 강의를 신청한 경우

            # 1. ApplyAlarm
            if alarm['alarm_category'] == 1:
                # 강의 신청자 = 알람을 보낸사람, 강사 = 로그인한 사람, 알람의 상태 = 읽지않음
                applies = Apply.objects.filter(member_id=alarm.get('sender_id'), lecture__teacher_id=member_id, apply_status=0)\
                    .annotate(title=F('lecture__lecture_title')).values('title','lecture_id')
                # 여러 알람에 반복문으로 추가요소 담기
                for apply in applies:
                    # 강의 대표사진을 가져와 target_file에 담아주기
                    target_file = LectureProductFile.objects.filter(lecture_id = apply.get('lecture_id')).values('file_url').first()
                    alarm['target_file'] = target_file['file_url'] if target_file else 'file/2024/03/05/blank-image.png'
                    #f스트링에 쓰기 위해서 변수 선언
                    title = apply.get('title')
                    alarm["message"] = f'님이 {title} 강의를 신청하였습니다.'
                    # 클릭시 페이지 이동을 위한 기본 url
                    alarm['target_url'] = '/member/mypage/teachers/'

            # 내가 쓴 노하우 글에 좋아요를 누른 경우

            # 2. KnowhowLikeAlarm
            elif alarm['alarm_category'] == 2:
                # 노하우 글에 좋아요를 누른 사용자 정보 가져오기
                knowhow_likes = KnowhowLike.objects.filter(member_id=alarm.get('sender_id'),
                                                           knowhow__member_id=member_id) \
                    .annotate(knowhow_name=F('knowhow__knowhow_title')).values('knowhow_name', 'knowhow_id')

                # 각 좋아요 정보에 대해 반복하여 처리
                for knowhow_like in knowhow_likes:
                    # 노하우 글의 대표 이미지 가져오기
                    target_file = KnowhowFile.objects.filter(knowhow_id=knowhow_like.get('knowhow_id')).values(
                        'file_url').first()
                    # 대표 이미지가 없을 경우 기본 이미지 사용
                    alarm['target_file'] = target_file['file_url'] if target_file else 'file/2024/03/05/blank-image.png'

                    # 노하우 글의 제목을 가져와 메시지에 추가
                    knowhow = knowhow_like.get('knowhow_name')
                    alarm["message"] = f'님이 {knowhow}를 좋아합니다.'

                    # 클릭 시 이동할 페이지의 URL 설정
                    alarm['target_url'] = '/knowhow/detail/?id='

            # 3. KnowhowReplyAlarm
            elif alarm['alarm_category'] == 3:
                # 노하우 댓글 정보 가져오기
                knowhow_replies = KnowhowReply.objects.filter(member_id=alarm.get('sender_id'),
                                                              knowhow__member_id=member_id) \
                    .annotate(knowhow_name=F('knowhow__knowhow_title'))

                # 각 댓글 정보에 대해 반복하여 처리
                for knowhow_reply in knowhow_replies:
                    # 댓글이 달린 노하우의 대표 이미지 가져오기
                    target_file = KnowhowFile.objects.filter(knowhow_id=knowhow_reply.knowhow_id).values(
                        'file_url').first()
                    # 대표 이미지가 없을 경우 기본 이미지 사용
                    alarm['target_file'] = target_file['file_url'] if target_file else 'file/2024/03/05/blank-image.png'

                    # 댓글이 달린 노하우의 제목 가져오기
                    knowhow = knowhow_reply.knowhow_name
                    # 댓글 내용 가져오기
                    alarm['reply'] = knowhow_reply.knowhow_reply_content
                    # 메시지 구성
                    alarm["message"] = f'님이 {knowhow}에 댓글을 남겼습니다.'
                    # 클릭 시 이동할 페이지의 URL 설정
                    alarm['target_url'] = '/knowhow/detail/?id='


            # 4. PostLikeAlarm
            elif alarm['alarm_category'] == 4:
                # 게시물 좋아요 정보 가져오기
                post_likes = PostLike.objects.filter(member_id=alarm.get('sender_id'), post__member_id=member_id) \
                    .annotate(post_name=F('post__post_title')).values('post_name', 'post_id')

                # 각 좋아요 정보에 대해 반복하여 처리
                for post_like in post_likes:
                    # 좋아요가 달린 게시물의 대표 이미지 가져오기
                    target_file = PostFile.objects.filter(post_id=post_like.get('post_id')).values('file_url').first()
                    # 대표 이미지가 없을 경우 기본 이미지 사용
                    alarm['target_file'] = target_file['file_url'] if target_file else 'file/2024/03/05/blank-image.png'

                    # 좋아요가 달린 게시물의 제목 가져오기
                    post_like = post_like.get('post_name')
                    # 메시지 구성
                    alarm["message"] = f'님이 {post_like}를 좋아합니다.'
                    # 클릭 시 이동할 페이지의 URL 설정
                    alarm['target_url'] = '/post/detail/?id='

            # 5. PostReplyAlarm
            elif alarm['alarm_category'] == 5:
                # 게시물 댓글 정보 가져오기
                post_replies = PostReply.objects.filter(member_id=alarm.get('sender_id'),
                                                        post__member_id=member_id) \
                    .annotate(post_name=F('post__post_title'))

                # 각 댓글 정보에 대해 반복하여 처리
                for post_reply in post_replies:
                    # 댓글이 달린 게시물의 대표 이미지 가져오기
                    target_file = PostFile.objects.filter(post_id=post_reply.post_id).values('file_url').first()
                    # 대표 이미지가 없을 경우 기본 이미지 사용
                    alarm['target_file'] = target_file['file_url'] if target_file else 'file/2024/03/05/blank-image.png'

                    # 댓글이 달린 게시물의 제목 가져오기
                    post = post_reply.post_name
                    # 댓글 내용 가져오기
                    alarm['reply'] = post_reply.post_reply_content
                    # 메시지 구성
                    alarm["message"] = f'님이 {post}에 댓글을 남겼습니다.'
                    # 클릭 시 이동할 페이지의 URL 설정
                    alarm['target_url'] = '/post/detail/?id='



            # 6. LectureReviewAlarm
            elif alarm['alarm_category'] == 6:
                # 강의 리뷰 정보 가져오기
                reviews = LectureReview.objects.filter(member_id=alarm.get('sender_id'), lecture__teacher_id=member_id) \
                    .annotate(lecture_name=F('lecture__lecture_title'), lecture_status=F('lecture__online_status'))

                # 각 리뷰 정보에 대해 반복하여 처리
                for review in reviews:
                    # 리뷰가 달린 강의의 대표 이미지 가져오기
                    target_file = LectureProductFile.objects.filter(lecture_id=review.lecture_id).values(
                        'file_url').first()
                    # 대표 이미지가 없을 경우 기본 이미지 사용
                    alarm['target_file'] = target_file.get(
                        'file_url') if target_file else 'file/2024/03/05/blank-image.png'

                    # 리뷰가 달린 강의의 제목 가져오기
                    lecture = review.lecture_name
                    # 메시지 구성
                    alarm["message"] = f'님이 {lecture}에 리뷰를 작성하였습니다.'
                    # 리뷰 제목 가져오기
                    alarm["reply"] = review.review_title

                    # 강의 온라인 상태에 따라 'offline' 또는 'online' 설정
                    if review.lecture_status == 0 or review.lecture_status == False:
                        alarm['lecture_status'] = 'offline'
                    elif review.lecture_status == 1 or review.lecture_status == True:
                        alarm['lecture_status'] = 'online'

                    # 강의 온라인 상태에 따라 URL 설정
                    lecture_status = alarm.get('lecture_status')
                    alarm['target_url'] = f'/lecture/detail/{lecture_status}/?id='

        # 처리된 알람 반환
        return Response(alarms[offset:limit])

    @transaction.atomic
    def patch(self, request):
        # 요청으로부터 알람 ID 가져오기
        alarm_id = request.data.get('alarm_id')

        # 알람 ID와 현재 멤버의 ID를 사용하여 알람 객체 가져오기
        alarm = Alarm.objects.get(id=alarm_id, receiver_id=request.session.get('member').get('id'))

        # 알람 상태를 '읽음'으로 변경하고 갱신 날짜 업데이트
        alarm.alarm_status = True
        alarm.updated_date = timezone.now()

        # 변경된 알람 상태와 갱신 날짜를 저장
        alarm.save(update_fields=['alarm_status', 'updated_date'])

        # 성공 메시지 반환
        return Response('success')

    def delete(self, request):
        # 모든 알람 객체 가져오기
        alarms = Alarm.objects.all()

        # 모든 알람에 대해 반복하여 처리
        for alarm in alarms:
            # 알람 상태를 '읽음'으로 변경하고 갱신 날짜 업데이트
            alarm.alarm_status = True
            alarm.updated_date = timezone.now()

            # 변경된 알람 상태와 갱신 날짜를 저장
            alarm.save(update_fields=['alarm_status', 'updated_date'])

        # 성공 메시지 반환