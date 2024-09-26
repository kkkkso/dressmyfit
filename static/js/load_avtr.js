// load 대신 DOMContentLoaded 사용함
window.addEventListener('DOMContentLoaded', function() {
    const avatarImageUrl = sessionStorage.getItem('avatarImageUrl'); // 로컬 저장소에서 URL 불러오기
    if (avatarImageUrl) {
      const avatarImage = document.getElementById('avatar-img'); // 다음 페이지의 이미지 요소
      avatarImage.src = avatarImageUrl;
      avatarImage.style.display = 'block';
    }
  });