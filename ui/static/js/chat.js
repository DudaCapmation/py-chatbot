async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const message = inputField.value;

    if (!message.trim()) return; // Don't send empty messages

    // Shows user's message
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p class="user"><strong>You:</strong> ${message}</p>`;
    // Clears input field 
    inputField.value = "";

    // Placeholder for the bot's streaming reply
    const botPlaceholder = document.createElement("p")
    botPlaceholder.className = "bot";
    botPlaceholder.innerHTML = "<strong>Bot:</strong> ";
    chatBox.appendChild(botPlaceholder)

    // Fetching while streaming
    try { 
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: message})
        });

        if (!response.ok) {
        throw new Error("HTTP error: " + response.status);
        }

        // Reads stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let partialChunk = "";

        while (true) {
            const {value, done} = await reader.read();
            if (done) break;
            if (value) {
                // Appends each chunk of text/delta
                const chunk = decoder.decode(value, {stream: true});
                partialChunk += chunk;
                botPlaceholder.innerHTML += chunk;
                // Auto-scroll
                chatBox.scrollTop = chatBox.scrollHeight
            }
        }
    } catch (error) {
    console.error("Error during fetch or stream:", error);
    botPlaceholder.innerHTML += "<em>(error)</em>";
    }
}

// Enter sends the message
document.getElementById("user-input").addEventListener("keydown", e => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

// Toggle dark mode
document.getElementById("toggle-dark").addEventListener("click", () => {
    document.body.classList.toggle("dark");
});