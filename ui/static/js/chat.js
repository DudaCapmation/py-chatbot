async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const message = inputField.value;

    if (!message.trim()) return; // Don't send empty messages

    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: message})
    });

    const data = await response.json();

    const chatBox = document.getElementById("chatbox");
    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.reply}</p>`;

    inputField.value = "";
}
