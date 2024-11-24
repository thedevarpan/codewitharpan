document.querySelectorAll('.reply-button').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        const parentId = this.getAttribute('data-parent-id');
        const replyForm = document.querySelector('#reply-form-template').cloneNode(true);
        replyForm.classList.remove('d-none');
        replyForm.querySelector('#parent_id').value = parentId;
        
        // Append the reply form under the current comment
        this.closest('.item-box').appendChild(replyForm);
    });
});