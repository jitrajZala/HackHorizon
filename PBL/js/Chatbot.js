document.addEventListener("DOMContentLoaded", function () {
    const chatContainer = document.querySelector(".chat-container");
    const chatIcon = document.getElementById("chat-icon");
    const closeButton = document.getElementById("close-btn");

    // Initially hide chat container
    chatContainer.classList.add("hidden");

    // When clicking the chat icon, open the chatbox
    chatIcon.addEventListener("click", function () {
        chatContainer.classList.remove("hidden");
        chatIcon.style.display = "none"; // Hide the chat icon
    });

    // When clicking the close button, hide the chatbox and show the chat icon
    closeButton.addEventListener("click", function () {
        chatContainer.classList.add("hidden");
        chatIcon.style.display = "flex"; // Show the chat icon again
    });

    function sendMessage() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();
        if (!message) return;

        addMessage(message, 'user-message');
        input.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        })
        .then(response => response.json())
        .then(data => addMessage(data.response, 'bot-message'))
        .catch(() => addMessage('Sorry, I encountered an error. Please try again.', 'bot-message'));
    }

    function addMessage(message, className) {
        const messagesDiv = document.getElementById('chat-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${className}`;

        // Add chatbot logo for bot messages
        if (className === "bot-message") {
            messageElement.innerHTML = `<img src="img.png" class="bot-logo"> <span>${message}</span>`;
        } else {
            messageElement.textContent = message;
        }

        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    window.onload = function () {
        addMessage('Hello! I am KJSIT chatbot. How can I help you today?', 'bot-message');
    };

    document.getElementById("send-btn").addEventListener("click", sendMessage);
    document.getElementById("user-input").addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });
});
