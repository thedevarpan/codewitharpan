document.addEventListener('DOMContentLoaded', function () {
    // Get all reply buttons
    const replyButtons = document.querySelectorAll('.reply-button');

    // Iterate over each reply button
    replyButtons.forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Remove any existing reply form
            const existingReplyForm = document.querySelector('.reply-form');
            if (existingReplyForm) {
                existingReplyForm.remove();
            }

            // Clone the hidden reply form template
            const replyFormTemplate = document.getElementById('reply-form-template');
            const replyForm = replyFormTemplate.cloneNode(true);
            replyForm.id = '';
            replyForm.classList.remove('d-none');
            replyForm.classList.add('reply-form');

            // Insert the reply form after the comment item box
            const commentBox = button.closest('.item-box');
            commentBox.appendChild(replyForm);

            // Add event listener for submit reply button
            replyForm.querySelector('.submit-reply').addEventListener('click', function () {
                const replyMessage = replyForm.querySelector('textarea[name="message"]').value;
                console.log('Reply message:', replyMessage);

                // Here you can handle the form submission (e.g., send the reply to the server)
                // For now, we'll just remove the form
                replyForm.remove();
            });
        });
    });
});
