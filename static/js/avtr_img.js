document.getElementById("avatar-form").addEventListener("submit", function(event) {
    event.preventDefault(); // 기본 폼 제출 방지

    // 입력된 데이터를 수집
//    const height = document.getElementById("height").value;
//    const weight = document.getElementById("weight").value;
//    const gender = document.getElementById("gender").value;
//    const note = document.getElementById("note").value;

    const formData = new FormData(document.getElementById("avatar-form"));
    // 서버로 비동기 요청 보내기 (AJAX)
    fetch('/create-avatar', {
        method: 'POST',
        //headers: {
        //    'Content-Type': 'application/json',
        //},
        //body: JSON.stringify({ height: height, weight: weight, gender: gender, note: note })
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // 서버로부터 반환된 이미지 URL 사용
        const avatarImage = document.getElementById("avatar-img");
        avatarImage.src = data.avatar_img_url;
        avatarImage.style.display = 'block'; // 이미지를 보이게 설정
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
