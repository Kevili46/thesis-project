let history = document.getElementsByClassName('pt-history')[0];
let textfield = document.getElementById('question');
history.scrollTop = history.scrollHeight;
history.scrollTo({
    left: 0,
    top: history.scrollTop,
    behavior: 'smooth'
});

function writeMessage() {
    history.appendChild(createChatline('user', textfield.value));
    history.scrollTop = history.scrollHeight;
    history.scrollTo({
        left: 0,
        top: history.scrollTop,
        behavior: 'smooth'
    });
    setTimeout(() => {
        history.appendChild(createLoader());
        history.scrollTop = history.scrollHeight;
        history.scrollTo({
            left: 0,
            top: history.scrollTop,
            behavior: 'smooth'
        });
    }, 400)
}

function createChatline(author, text) {
    let chatline = document.createElement('div');
    chatline.className = `chat-line ${author} fade`;
    let textDiv = document.createElement('div');
    textDiv.className = 'text';
    textDiv.innerHTML = text;
    chatline.appendChild(textDiv);
    return chatline
}

function createLoader() {
    let chatline = document.createElement('div');
    chatline.className = `chat-line system fade`;
    let textDiv = document.createElement('div');
    textDiv.className = 'text';
    textDiv.innerHTML = "Schreibt ..."
    chatline.appendChild(textDiv);
    return chatline
}
