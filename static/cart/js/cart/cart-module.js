const cartService = (()=>{
    // 장바구니 서비스: 장바구니와 관련된 기능을 제공하는 객체

    // 장바구니 목록을 가져오는 함수
    const getList = async (cart_id, callback) =>{
        // 서버에 요청하여 장바구니 목록을 가져옴
        const response = await fetch(`/cart/list/${cart_id}`);
        // JSON 형식으로 받아온 목록을 변수에 저장
        const details = await response.json();
        // 콜백 함수가 주어진 경우 실행
        if (callback){
            return callback(details)
        }
        // 콜백 함수가 주어지지 않은 경우 목록 반환
        return details
    };

    // 장바구니에서 특정 항목을 삭제하는 함수
    const remove = async (detailId) => {
        // 서버에 항목 삭제 요청 전송
        await fetch(`/cart/${detailId}/`, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token
            }
        });
    }

    // 장바구니에서 특정 항목을 선택하는 함수
    const select = async (detailId, callback) =>{
        // 서버에 선택된 항목 정보 요청
        const response = await fetch(`/cart/${detailId}`);
        // JSON 형식으로 받아온 항목 정보를 변수에 저장
        const detail = await response.json();
        // 콜백 함수가 주어진 경우 실행
        if (callback){
            return callback(detail)
        }
        // 콜백 함수가 주어지지 않은 경우 선택된 항목 반환
        return detail
    };

    // 장바구니를 제출하는 함수
    const submit = async (cart_id) =>{
        // 서버에 장바구니 제출 요청 전송
        await fetch(`/cart/checkout/${cart_id}/`, {
            method: 'post',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token
            }
        });
    }

    // 외부에서 호출 가능한 함수들을 반환
    return {getList:getList, remove:remove, select:select, submit:submit}

})()