
document.getElementById('upload-target').addEventListener('change', function(event) {
    const file = event.target.files[0]; // 사용자가 선택한 파일
    if (file) {
        const reader = new FileReader(); // FileReader로 이미지를 읽음

        reader.onload = function(e) {
            const uploadedImage = document.getElementById('avatar-img');
            uploadedImage.src = e.target.result; // 업로드한 이미지의 URL을 img 요소의 src에 설정
            uploadedImage.style.display = 'block'; // 이미지를 보이도록 설정
        
            sessionStorage.setItem('avatarImageUrl', e.target.result);
        };

        reader.readAsDataURL(file); // 파일을 DataURL로 읽기
    }
});

