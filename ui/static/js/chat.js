async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value;

    if (!message.trim()) return; // Don't send empty messages

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p class="user"><strong>You:</strong> ${message}</p>`;

    inputField.value = "";

    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    });

    const data = await response.json();
    chatBox.innerHTML += `<p class="bot"><strong>Bot:</strong> ${data.reply}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight
}

document.getElementById("user-input").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

document.getElementById("toggle-dark").addEventListener("click", () => {
    document.body.classList.toggle("dark");
});