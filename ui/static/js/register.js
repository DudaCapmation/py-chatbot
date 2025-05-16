document.getElementById("reg-btn").addEventListener("click", async () => {
    const user = document.getElementById("reg-username").value;
    const pw = document.getElementById("reg-password").value;
    const err = document.getElementById("reg-error");
    const ok = document.getElementById("reg-success");
    err.textContent = "";
    ok.textContent = "";

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
        ok.textContent = "Registered! Please log in."
    } catch (e) {
        err.textContent = e.detail || "Registration failed."
    }
});