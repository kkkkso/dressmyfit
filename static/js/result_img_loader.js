 // 페이지 로드 시 sessionStorage에서 이미지 가져오기
 window.addEventListener('DOMContentLoaded', () => {
    const resultImageB64 = sessionStorage.getItem('result_image');
    const maskedPersonB64 = sessionStorage.getItem('masked_person');
    const avatarImageUrl = sessionStorage.getItem('avatarImageUrl');
    const clothType = sessionStorage.getItem('cloth_type');
    const fittingType = sessionStorage.getItem('fitting_type');
    //선택한 cloth 이미지 말하는 거임.
    const clothImageUrl = sessionStorage.getItem('cloth_image'); //imageUrl의 키 이름인 'cloth_image' 저장은 server_comm.js에 있음
    if (clothImageUrl) {
        const clothImage = document.getElementById('inference-used'); // 다음 페이지의 이미지 요소
        clothImage.src = clothImageUrl;
        //avatarImage.style.display = 'block';
      }
    
    document.getElementById('target-used').src = avatarImageUrl;
    document.getElementById('cloth-type-txt').textContent = clothType;
    document.getElementById('fitting-type-txt').textContent = fittingType;


    if (resultImageB64 && maskedPersonB64) {
        document.getElementById('avatar-image').src = `data:image/png;base64,${resultImageB64}`; //result_page.html에서는 avatar-image라는 아이디를 가진 자리가 제일 큰 result 자리임.
        // document.getElementById('mask-used').src = `data:image/png;base64,${maskedPersonB64}`;
    } else {
        alert('이미지 데이터가 없습니다. 다시 시도해주세요.');
        window.location.href = '/';
    }
});

// "Go Back" 버튼 클릭 시 이전 페이지로 이동
// document.getElementById('go-back').addEventListener('click', function() {
//     window.location.href = '/';
// });