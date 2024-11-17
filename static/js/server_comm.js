let cloth_image = null;
let person_image = null;
let imageUrl = null;

setTimeout( () => {
    let progressBar = document.getElementById('progress-bar');
    console.log('pb: ', progressBar)    
}, 1000);

// 옷 이미지를 클릭할 때
document.querySelectorAll('[class^="cloth-img"]').forEach(image => {
    image.addEventListener('click', async function() {
        imageUrl = this.src; // 선택된 이미지의 경로 저장
        sessionStorage.setItem('cloth_image', imageUrl); //result_img_loader에서 가져오려고.

        // 선택된 이미지를 강조 표시
        document.querySelectorAll('[class^="cloth-img"]').forEach(img => img.classList.remove('selected'));
        this.classList.add('selected');

        fetch(imageUrl)
            .then(res=>res.blob())
            .then(blob => {
                cloth_image = new File([blob], 'cloth_image.png', {type: 'image/png'});
            });

    });
});

// "SEE THE RESULT" 버튼 클릭 시
document.getElementById('see-the-result').addEventListener('click', async function(event) {
    event.preventDefault();
    const c_type = document.getElementById('select-c-type').value;
    const f_type = document.getElementById('select-f-type').value;
    const personImageUrl = document.getElementById('avatar-img').src;
    const loadingEl = document.getElementById('loading');
    loadingEl.style.display = 'flex';

    if (!imageUrl) {
        alert('Please select a clothing image!');
        event.preventDefault();
    } else if (!c_type || !f_type) {
        alert('Please select cloth type and fitting type.');
        event.preventDefault();
    } else {

     const blob = await  fetch(personImageUrl)
            .then(res=>res.blob())
      person_image = new File([blob], 'person_image.png', { type: 'image/png' });

    //    fetch(personImageUrl)
    //        .then(res=>res.blob())
    //        .then(blob =>{
    //            person_image = new File([blob], 'person_image.png', { type: 'image/png' });
    //        });
   
        //javascript는 비동기 언어이기 때문이다.
        //아래에서 peroson_image를 쓰고 있기 때문에, await를 꼭 써줘야함.

            
        // 서버로 데이터 전송
        const formData = new FormData();
        formData.append('cloth_type', c_type);
        formData.append('fitting_type', f_type);
        formData.append('cloth_image', cloth_image);
        formData.append('person_image', person_image);

        // 서버로 요청 보내기 (AJAX)
        // fetch('http://203.153.147.3:3000/process-image', {
        // asyncronous language: javascript
        fetch('http://127.0.0.1:3000/process-image', {
            method: 'POST',
             body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            console.log(JSON.stringify(data, null, 2));
            if (data.result_image && data.masked_person) {
                // sessionStorage에 Base64 이미지 저장
                sessionStorage.setItem('result_image', data.result_image);
                sessionStorage.setItem('masked_person', data.masked_person);
    loadingEl.style.display = 'none';
                sessionStorage.setItem('cloth_type', c_type)
                sessionStorage.setItem('fitting_type', f_type)
                // 결과 페이지로 이동
                window.location.href = '/result-page';
            } else {
                alert('이미지 처리에 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('서버와의 통신 중 오류가 발생했습니다.');
        });
        setTimeout( () => {
            const ws = new WebSocket(`ws://127.0.0.1:3000/ws/`);
            console.log('websocket created!');
            const progressRender = document.getElementById('progress-render');
            const progressText = document.getElementById('progress-text');

            console.log('progressDiv: ', progressRender)
            ws.onmessage = (event) => {
                console.log('Received:', event.data);
                if (event.data === 'Processing complete') {
                    ws.close();
                    progressDiv.innerHTML = "Processing complete!";
                } else {
                    // Update progress bar or UI element with progress
                    const progress = parseFloat(event.data) * 100;
                    console.log('Progress parsed:', progress);
                    progressRender.style.width = `${progress}%`;
                    progressText.textContent = `${progress.toFixed(0)}%`;
                }
            };

            ws.onclose = () => {
                console.log('WebSocket connection closed');
            };
        }, 300)
    }
});