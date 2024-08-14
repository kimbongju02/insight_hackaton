const recordButton = document.getElementById('recordButton');
const audio = document.getElementById('audioPlayer');
const backgroundVideo = document.getElementById('backgroundVideo');
const recordIcon = document.getElementById('recordIcon');

let mediaRecorder;
const originalVideoSource = '/static/video/Idle_2.mp4'; // 원래 배경 비디오
const randomVideos = [
    '/static/video/Speaking_gesture.mp4',
    '/static/video/Speaking_gesture1.mp4',
    '/static/video/Speaking_gesture2.mp4',
    '/static/video/Speaking_gesture3.mp4',
    '/static/video/Speaking.mp4'
];

recordButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state == "recording") {
        mediaRecorder.stop();
        recordIcon.className = 'fas fa-microphone';
    } else {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            const chunks = [];

            mediaRecorder.ondataavailable = (event) => {
                chunks.push(event.data);
            };

            mediaRecorder.onstop = (event) => {
                const blob = new Blob(chunks, { 'type': 'audio/mpeg' });
                
                const formData = new FormData();
                formData.append('audio_file', blob, 'recording.mp3');
                
                fetch('/upload_audio', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    audio.addEventListener('loadedmetadata', () => {
                        const duration = audio.duration;
                        console.log('음성 파일의 총 재생 시간:', duration, '초');
                    });

                    // 녹음이 시작되면 랜덤 비디오로 배경 변경
                    const randomIndex = Math.floor(Math.random() * randomVideos.length);
                    backgroundVideo.src = randomVideos[randomIndex];
                    backgroundVideo.load();

                    
                    audio.src = url;
                    audio.autoplay = true;

                    audio.onended = () => {
                        // 오디오가 종료되면 원래 비디오로 돌아가기
                        backgroundVideo.src = originalVideoSource;
                        backgroundVideo.load();
                    };

                })
                .catch(error => {
                    console.error('Error:', error);
                });
                  
            };

            

            
            mediaRecorder.start();
            recordIcon.className = 'fas fa-stop';
        })
        .catch(err => {
            console.error('Error accessing media devices.', err);
        });
    }
});
