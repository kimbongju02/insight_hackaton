const recordButton = document.getElementById('recordButton');
const audio = document.getElementById('audioPlayer');

let mediaRecorder;

recordButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state == "recording") {
        mediaRecorder.stop();
        recordButton.textContent = "녹음 시작";
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
                    audio.src = url;
                    audio.autoplay = true;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
                  
            };
            
            mediaRecorder.start();
            recordButton.textContent = "녹음 중지";
        })
        .catch(err => {
            console.error('Error accessing media devices.', err);
        });
    }
});