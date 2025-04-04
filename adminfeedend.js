#submitting feedback
document.getElementById('feedbackForm').addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(this);

    fetch('submit_feedback.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            document.getElementById('feedbackForm').reset();
        }
    });
});

#displaying the feedback for admin
fetch('view_feedback.php')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let feedbackList = document.getElementById('feedbackList');
            feedbackList.innerHTML = '';
            
            data.feedbacks.forEach(feedback => {
                let row = `<tr>
                    <td>${feedback.id}</td>
                    <td>${feedback.reg_number}</td>
                    <td>${feedback.feedback}</td>
                    <td>${feedback.timestamp}</td>
                </tr>`;
                feedbackList.innerHTML += row;
            });
        } else {
            alert(data.message);
        }
    });
