// 페이지 초기화
let page = 1;

// 텍스트를 일정 길이로 자르고 말줄임표를 추가하여 반환하는 함수
function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...'; // 말줄임표 추가
    } else {
        return text;
    }
}

// 알람을 화면에 표시하는 함수
const showAlarm = (alarms) => {
  // 전체 알람 수 초기화
  let totalalarms = alarms.length;

  // HTML에 알람 수 업데이트
  const alarmCounts = document.querySelectorAll('.alarm-count');
  alarmCounts.forEach((alarmCount) => {
    alarmCount.innerText = totalalarms;
  });

  let text = ``;

  // 각 알람에 대해 HTML 생성
  alarms.forEach((alarm) => {
      let member_file = '';
      // 멤버 파일이 URL인지 확인하여 적절한 경로 설정
      if (alarm.member_file.includes('http')) {
        member_file = alarm.member_file;
      } else {
        member_file = `/upload/${alarm.member_file}`;
      }

      // 알람 카테고리에 따라 HTML 생성
      if (alarm.alarm_category === 1) {
          text += `
            <div>    
              <div class="notice-contents">
                <a href="" class="notice-profile-box">
                  <img src="${member_file}" alt="" class="notice-profile" />
                </a>
                <a href="${alarm.target_url}" class="notice-content-box">
                  <div class="inner-txt-wrap">
                    <span class="inner-txt">
                      <strong>${alarm.sender}</strong>
                        ${alarm.message}                  
                    </span>
                    <span class="last-time">${timeForToday(alarm.updated_date)}</span>
                  </div>
                  <img src="/upload/${alarm.target_file}" alt="" class="notice-img" />
                </a>
                <div class="check ${alarm.id}">확인</div>
              </div>
            <div>`;
      } else if (alarm.alarm_category === 3 || alarm.alarm_category === 5 || alarm.alarm_category === 6) {
          text += `
          <div>    
            <div class="notice-contents">
              <a href="" class="notice-profile-box">
                <img src="${member_file}" alt="" class="notice-profile" />
              </a>
              <a href="${alarm.target_url}${alarm.target_id}" class="notice-content-box">
                <div class="inner-txt-wrap">
                  <span class="inner-txt">
                    <strong>${alarm.sender}</strong>
                      ${alarm.message}                  
                  </span>
                  <span class="inner-txt">
                      ${truncateText(alarm.reply, 20)}                  
                  </span>
                  <span class="last-time">${timeForToday(alarm.updated_date)}</span>
                </div>
                <img src="/upload/${alarm.target_file}" alt="" class="notice-img" />
              </a>
              <div class="check ${alarm.id}">확인</div>
            </div>
          <div>`;
      } else {
          text += `
          <div>    
            <div class="notice-contents">
              <a href="" class="notice-profile-box">
                <img src="${member_file}" alt="" class="notice-profile" />
              </a>
              <a href="${alarm.target_url}${alarm.target_id}" class="notice-content-box">
                <div class="inner-txt-wrap">
                  <span class="inner-txt">
                    <strong>${alarm.sender}</strong>
                      ${alarm.message}                  
                  </span>
                  <span class="last-time">${timeForToday(alarm.updated_date)}</span>
                </div>
                <img src="/upload/${alarm.target_file}" alt="" class="notice-img" />
              </a>
              <div class="check ${alarm.id}">확인</div>
            </div>
          <div>`;
      }
  });

  // 생성된 HTML 반환
  return text;
}

// .here 클래스를 가진 요소 선택
const target = document.querySelector('.here');

// 알람 리스트를 가져오는 함수 호출
alarmService.alarmList(page++, showAlarm).then((text) => {
  // 가져온 HTML을 선택한 요소에 추가
  target.innerHTML += text;
});

// 스크롤 이벤트 리스너 추가
window.addEventListener("scroll", () => {
    // 현재 스크롤 위치
    const scrollTop = document.documentElement.scrollTop;
    // 브라우저 창 높이
    const windowHeight = window.innerHeight;
    // 문서 전체 높이
    const totalHeight = document.documentElement.scrollHeight;

    // 스크롤이 문서 끝에 도달하면 추가 알람을 가져와서 표시
    if (scrollTop + windowHeight >= totalHeight) {
        alarmService.alarmList(page++, showAlarm()).then((text) => {
            // 가져온 HTML을 선택한 요소에 추가
            target.innerHTML += text;
        });
    }
});

// 시간 변환 함수
function timeForToday(datetime) {
    const today = new Date();
    const date = new Date(datetime);

    let gap = Math.floor((today.getTime() - date.getTime()) / 1000 / 60);

    if (gap < 1) {
        return "방금 전";
    }

    if (gap < 60) {
        return `${gap}분 전`;
    }

    gap = Math.floor(gap / 60);

    if (gap < 24) {
        return `${gap}시간 전`;
    }

    gap = Math.floor(gap / 24);

    if (gap < 31) {
        return `${gap}일 전`;
    }

    gap = Math.floor(gap / 31);

    if (gap < 12) {
        return `${gap}개월 전`;
    }

    gap = Math.floor(gap / 12);

    return `${gap}년 전`;
}

// 'click' 이벤트 리스너 추가
target.addEventListener('click', async (e) => {
    // 클릭된 요소가 'check' 클래스를 가지고 있는지 확인
    if (e.target.classList[0] === 'check') {
        // 알람의 고유 ID를 가져옴
        const alarm_id = e.target.classList[1];
        // 알람 제거 함수 호출
        await alarmService.removeAlarm(alarm_id);
    }
    // 페이지 초기화
    page = 1;
    // 업데이트된 알람 리스트 가져오기
    const updatedText = await alarmService.alarmList(page, showAlarm);
    // 알람을 표시할 요소에 새로운 HTML 삽입
    target.innerHTML = updatedText;
});

// 모두읽기 버튼 'check-all' 클래스를 가진 요소 선택
const readAll = document.querySelector('.check-all');

// 'click' 이벤트 리스너 추가
readAll.addEventListener('click', async (e) => {
    // 모든 알람 제거 함수 호출
    await alarmService.removeAll(page);
    // 페이지 초기화
    page = 1;
    // 업데이트된 알람 리스트 가져오기
    const newText = await alarmService.alarmList(page, showAlarm);
    // 알람을 표시할 요소에 새로운 HTML 삽입
    target.innerHTML = newText;
});