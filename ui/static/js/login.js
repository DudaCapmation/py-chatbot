document.getElementById("login-btn").addEventListener("click", async () => {
    const user = document.getElementById("login-username").value;
    const pw = document.getElementById("login-password").value;
    const err = document.getElementById("login-error");
    err.textContent = "";

    if (!user || !pw) {
        err.textContent = "Both fields are required.";
        return;
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: user, password: pw})
        });
        if (!res.ok) throw await res.json();
        // If success, go to chat
        window.location.href = "/";
    } catch (e) {
        err.textContent = e.detail || "Login failed.";
    }
});