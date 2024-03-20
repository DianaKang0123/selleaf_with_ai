// 상품 가격을 보여주는 함수
const showPrice = (detail) => {
    let textlist = ``;
    let totalPrice = detail[0]['lecture_price'] * detail[0]['quantity']; // 총 가격 계산
    totalPrice = totalPrice.toLocaleString('ko-KR'); // 한국 통화 형식으로 변환
    textlist += `
      <div class="price-wrap ${detail[0]['id']}">
        <div class="name-side">${detail[0]['lecture_title']}</div>
        <div class="price-side">${totalPrice}원</div> 
      </div>
    `;
    return textlist;
}

// 장바구니에 담긴 상품을 보여주는 함수
const showCartItems = (details) => {
    let text = ``;

    // 장바구니에 상품이 없는 경우 처리
    if (details.length === 0) {
        text = `
          <div class="no-items-wrap">
              <h1 class="no-items-text">아직 장바구니에 담은 상품이 없어요.</h1>
              <div class="purchase-link-button-wrap">
                <a href="/lecture/total/" class="purchase-link-button">강의 바로가기</a>
              </div>
          </div>
        `;
    } else {
        // 장바구니에 상품이 있는 경우 처리
        details.forEach((detail) => {
            let totalPrice = detail['quantity'] * detail['lecture_price']; // 총 가격 계산
            totalPrice = totalPrice.toLocaleString('ko-KR'); // 한국 통화 형식으로 변환

            text += `
              <li class="product-preview-wrap ${detail['id']}">
                <div class="product-preview-container">
                  <div class="product-preview-inner">
                    <div class="selection ${detail['id']}"></div>
                    <h3 class="user-name">${detail['lecture_title']}</h3>
                    <div class="delete ${detail['id']}">삭제</div>
                  </div>
                  <hr class="divide"/>
                </div>
                <div class="order-product-info">
                  <figure class="product-preview-image">
                    <img
                        src="/upload/${detail['lecture_file']}"
                        class="product-image" alt=""
                    />
                  </figure>
                  <div class="product-info-contents">
                    <div class="delivery-condition">강사명 | ${detail['teacher_name']}</div>
                    <p class="product-name">
                      ${detail['date']} | ${detail['time']} | ${detail['kit']}
                    </p>
                    <p class="product-option">
                    <div class="selected-product-count">
                    인원
                        <div class="counted-number">
                          ${detail['quantity']}
                        </div>
                      </div>
                    </p>
                    <div class="product-price">
                      <span class="price-number">${totalPrice}</span>
                      <span class="won">원</span>
                    </div>
                  </div>
                </div>
              </li>
            `;
        });
    }
    return text;
}

// 장바구니 목록을 보여주는 <ul> 요소를 선택
const ul = document.querySelector('.cart-item-wrap');

// 결제 상세 정보가 표시되는 사이드바를 선택
const sidebar = document.querySelector('.payment-detail-container');

// 장바구니 목록을 가져와서 화면에 표시
cartService.getList(cart_id, showCartItems).then((text) => {
    ul.innerHTML = text; // 장바구니 목록을 HTML에 추가
});

// 장바구니 목록에 클릭 이벤트 리스너 추가
ul.addEventListener("click", async (e) => {
    // 삭제 버튼이 클릭된 경우
    if (e.target.classList[0] === 'delete') {
        // 삭제할 상품의 ID를 가져옴
        const detailId = e.target.classList[1];
        // 장바구니에서 상품 삭제
        await cartService.remove(detailId);
        // 변경된 장바구니 목록을 가져와서 HTML에 업데이트
        const updatedCart = await cartService.getList(cart_id, showCartItems);
        ul.innerHTML = updatedCart;

        // 선택된 상품 목록에서 삭제된 상품 제거
        const productNames = document.querySelector('.product-name-side');
        const productChildren = Array.from(productNames.children);
        productChildren.forEach((child) => {
            // 삭제된 상품의 ID와 일치하는 요소를 찾아 제거
            const targetId = child.classList[1];
            if (targetId === detailId) {
                child.remove();
            }
        });
    }
    // 선택 버튼이 클릭된 경우
    else if (e.target.classList[0] === 'selection') {
        let target = e.target;
        e.target.classList.toggle('count');
        // 선택된 경우
        if (target.classList.contains('count')) {
            // 선택한 상품의 배경색 변경
            target.style.backgroundColor = '#C06888';
            // 선택한 상품의 ID를 가져와서 가격 정보를 표시
            const detailId = e.target.classList[1];
            const selectedProduct = await cartService.select(detailId, showPrice);
            const productNames = document.querySelector('.product-name-side');
            productNames.innerHTML += selectedProduct;
            // 선택한 상품의 가격을 총 가격에 추가
            const prices = productNames.querySelectorAll('.price-side');
            let total = 0;
            prices.forEach((price) => {
                total += parseInt(price.innerText.replace(/[^\d]/g, ''));
            });
            const totalPrice = document.querySelector('.total-price');
            totalPrice.innerHTML = total.toLocaleString('ko-KR') + '원';
        }
        // 선택 해제된 경우
        else {
            // 선택 해제된 상품의 배경색 변경
            target.style.backgroundColor = '#fff';
            // 선택 해제된 상품의 ID를 가져와서 목록에서 제거
            const detailId = e.target.classList[1];
            const productNames = document.querySelector('.product-name-side');
            const productChildren = Array.from(productNames.children);
            productChildren.forEach((child) => {
                // 선택 해제된 상품과 동일한 ID를 가진 요소를 찾아 제거
                const targetId = child.classList[1];
                if (targetId === detailId) {
                    child.remove();
                    // 선택 해제된 상품의 가격을 총 가격에서 제거
                    const removedPrice = parseInt(child.querySelector('.price-side').innerText.replace(/[^\d]/g, ''));
                    const totalPrice = document.querySelector('.total-price');
                    const currentTotalPrice = parseInt(totalPrice.innerText.replace(/[^\d]/g, ''));
                    const newTotalPrice = currentTotalPrice - removedPrice;
                    totalPrice.innerHTML = newTotalPrice.toLocaleString('ko-KR') + '원';
                }
            });
        }
    }
});