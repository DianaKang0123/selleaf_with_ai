const alarmService = (() => {

    // 알람 목록을 가져오는 함수
    const alarmList = async (page, callback) => {
        // 서버로 알람 목록 요청을 보냄
        const response = await fetch(`/alarm/show/main/${page}`);
        // 응답을 JSON 형식으로 파싱하여 알람 목록을 가져옴
        const alarms = await response.json();
        // 콜백 함수가 주어졌을 경우에만 호출하여 알람 목록을 처리함
        if (callback) {
            return callback(alarms);
        }
        // 콜백 함수가 주어지지 않은 경우에는 알람 목록을 반환함
        return alarms;
    };

    // 특정 알람을 제거하는 함수
    const removeAlarm = async (alarm_id) => {
        // 서버로 알람 제거 요청을 보냄
        await fetch(`/alarm/update/`, {
            method: 'patch',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ alarm_id: alarm_id })
        });
    };

    // 모든 알람을 제거하는 함수
    const removeAll = async (page) => {
        // 서버로 모든 알람 제거 요청을 보냄
        await fetch(`/alarm/remove/`, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ page: page })
        });
    };

    // 외부로 노출할 메서드를 객체로 반환
    return { alarmList: alarmList, removeAlarm: removeAlarm, removeAll: removeAll };
})();