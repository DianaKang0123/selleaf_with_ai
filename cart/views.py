from django.db import transaction
from django.utils import timezone

from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response

from rest_framework.views import APIView

from apply.models import Apply
from cart.models import Cart, CartDetail
from lecture.models import LectureProductFile


# 장바구니 서비스
class CartView(View):

    def get(self, request):
        # 세션에 로그인한 멤버조회
        member = request.session['member']
        # 멤버의 프로필 사진 정보(dict)
        member_file = request.session['member_files']
        member_id = member.get('id')  # 멤버id 추출

        # 장바구니 테이블에서 로그인한 멤버의 활성된 장바구니 조회
        my_cart = Cart.objects.filter(member_id=member_id, cart_status=0)

        if not my_cart:
            # 장바구니가 없는 경우 새로운 장바구니 생성
            my_cart = Cart.objects.create(member_id=member_id)
        else:
            # 장바구니가 있는 경우 장바구니를 불러옴
            my_cart = my_cart.first()

        # 화면에 보낼 정보를 담아 전송
        context= {

            'cart_id':my_cart.id,
            'memberProfile':member_file[0]['file_url'],
            'member':member
        }
        # 화면으로 랜더
        return render(request, 'cart/cart.html', context)


class CartListAPI(APIView):
    def get(self, request, cart_id):

        details = []  # 카트 상세정보 저장 리스트

        # 세션의 멤버와 관련된 apply(신청) 검색: apply_status -3 = 장바구니
        applies = Apply.objects.filter(member_id=request.session['member']['id'], apply_status=-3)

        # 각 apply 별 카트 상세정보 검색
        for apply in applies:
            # 카트 ID와 apply 관련 상세정보 검색 후 이름 변경
            items = CartDetail.objects.filter(cart_id=cart_id, cart_detail_status=0, apply=apply) \
                .annotate(
                lecture_price=F('apply__lecture__lecture_price'),  # 강의 가격
                lecture_title=F('apply__lecture__lecture_title'),  # 강의 제목
                teacher_name=F('apply__lecture__teacher__member__member_name'),  # 강사 이름
                quantity=F('apply__quantity'),  # 수량
                date=F('apply__date'),  # 날짜
                time=F('apply__time'),  # 시간
                kit=F('apply__kit'),  # 키트
                lecture_id=F('apply__lecture__id')  # 강의 ID
            ).values('id', 'quantity', 'lecture_title', 'date', 'kit', 'time', 'teacher_name', 'lecture_price',
                     'lecture_id')

            # 상세정보 항목 반복 처리
            for detail in items:
                # 강의 물품 사진 파일 URL 검색
                detail_file = LectureProductFile.objects.filter(lecture_id=detail['lecture_id']).values(
                    'file_url').first()
                detail['lecture_file'] = detail_file['file_url']

            # 비어있는 항목 처리
            if not items:
                continue

            # 상세정보 리스트에 추가
            details.extend(items)

        # 상세정보 응답 반환
        return Response(details)


class CartAPI(APIView):

    # 장바구니 항목 삭제
    def delete(self, request, detail_id):

        # 주어진 detail_id에 해당하는 장바구니 항목 가져오기
        detail = CartDetail.objects.filter(id=detail_id).first()

        # 장바구니 항목을 삭제 상태로 변경
        detail.cart_detail_status = -1

        # 업데이트 된 날짜 설정
        detail.updated_date = timezone.now()

        # 변경사항 저장
        detail.save(update_fields=['cart_detail_status', 'updated_date'])

        # 삭제된 항목의 apply 모델에도 적용
        apply = Apply.objects.filter(id=detail.apply.id).first()
        apply.apply_status = -1
        apply.updated_date = timezone.now()
        apply.save(update_fields=['apply_status', 'updated_date'])

        # 성공적으로 처리되었음을 응답
        return Response('success')

    # 장바구니 항목 세부 정보 가져오기
    def get(self, request, detail_id):
        # 주어진 detail_id에 해당하는 장바구니 항목의 세부 정보 가져오기
        details = CartDetail.objects.filter(id=detail_id) \
            .annotate(
            lecture_title=F('apply__lecture__lecture_title'),  # 강의 제목
            lecture_price=F('apply__lecture__lecture_price'),  # 강의 가격
            quantity=F('apply__quantity')  # 수량
        ) \
            .values('lecture_title', 'lecture_price', 'quantity', 'id')  # 필요한 필드 선택

        # 세부 정보 응답으로 반환
        return Response(details)


class CartCheckoutAPI(APIView):
    @transaction.atomic  # 데이터베이스 작업이 하나의 트랜잭션으로 실행되도록 보장
    # 주문 처리
    def post(self, request, cart_id):
        # 세션에서 멤버 ID 가져오기
        member_id = request.session['member']['id']

        # 멤버의 활성화된(cart_status=0) 장바구니 가져오기
        cart = Cart.objects.filter(member_id=member_id, cart_status=0).first()

        # 카트 디테일 중 상태가 0(활성화)인 것들 가져오기
        cart_details = CartDetail.objects.filter(cart_detail_status=0, cart_id=cart.id)

        # 각 카트 디테일의 상태를 1(주문)로 변경하고 업데이트된 날짜 설정
        for detail in cart_details:
            detail.cart_detail_status = 1
            detail.updated_date = timezone.now()
            detail.save(update_fields=['cart_detail_status', 'updated_date'])

        # 해당 주문의 주문 세부 정보 페이지로 리디렉션
        return redirect(f'/order/cart/order/{cart.id}')