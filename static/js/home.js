const msg = document.querySelector('#msg');
const send = document.querySelector('#send');

if (msg) {
    msg.addEventListener('input', () => {
        if (msg.value.trim().length > 0) {
            send.disabled = false;
            send.classList.replace('btn-secondary', 'btn-primary')
        } else {
            send.disabled = true;
            send.classList.replace('btn-primary', 'btn-secondary')
        }
    });
}

function chatScroll() {
    var chatContainer = document.getElementById("chat-section");
    chatContainer.scrollTop = chatContainer.scrollHeight;
    chatContainer.scrollBehavior = 'auto';
}

function toastHidden() {
    var toast = document.querySelector('.toast');
    toast.classList.add('show');
    setTimeout(function(){
        toast.classList.remove('show');
    }, 4000);
}


document.addEventListener("DOMContentLoaded", function () {
    var messages = document.getElementsByClassName("p-msg");

    if (messages.length > 10) {
        chatScroll();
    }
    if (document.querySelector(".toast")) {
        toastHidden();
    }
});



// MODALS FRIENDS 

var addFriendElement = document.getElementById('addFriend');
var addFriendModal = new bootstrap.Modal(addFriendElement);

var editFriendElement = document.getElementById('editFriend');
var editFriendModal = new bootstrap.Modal(editFriendElement);

function openModal(event) {
    var targetElement = event.target;
    if (targetElement.id === 'dataAddFriend'){
        var dataElement = document.querySelector('#dataAddFriend');
        var data = dataElement.getAttribute('data-user-id');
        var field = document.getElementById('friend_modal');
        field.value = data;
    
        addFriendModal.show();
    } if (targetElement.id === 'dataEditFriend') {
        var dataElement = document.querySelector('#dataEditFriend');
        var data = dataElement.getAttribute('data-name_save');
        var field = document.getElementById('edit_name_modal');
        field.value = data;
        console.log(dataElement);
        console.log(data)
        console.log(field )

        editFriendModal.show();
    }
}

addFriendElement.addEventListener('hidden.bs.modal', function (event) {
    var backdropElement = document.querySelector('.modal-backdrop');
    backdropElement.parentNode.removeChild(backdropElement);
});
