document.getElementById("reg-btn").addEventListener("click", async () => {
    const user = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;
    
    const err = document.getElementById("reg-error");
    const ok = document.getElementById("reg-success");

    err.textContent = "";
    ok.textContent = "";

    if (!user || !password || !email) {
        err.textContent = "Both fields are required.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/register/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: user, password: password, email: email})
        });

        if (!response.ok) throw await response.json();
        ok.textContent = "Registered! Please log in."
        
    } catch (e) {
        err.textContent = e.detail || JSON.stringify(e) || "Registration failed."
    }
});