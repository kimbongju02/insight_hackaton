const recordButton = document.getElementById('recordButton');

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
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(data => {
                    console.log('Success:', data);
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