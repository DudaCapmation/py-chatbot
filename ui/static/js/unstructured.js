document.getElementById("unstructured-form").addEventListener("submit", async function(event) {
    event.preventDefault(); //Prevents the user from submitting the form again until the processing is done

    const fileInput = document.getElementById("file-input").files[0];
    const textInput = document.getElementById("text-input").value;
    const jsonSchema = document.getElementById("json-schema").value;

    const formData = new FormData() //To upload text and files in one request
    if (fileInput) {
        formData.append("file", fileInput);
    }
    formData.append("text", textInput);
    formData.append("schema", jsonSchema);

   try {
        const response = await fetch("http://127.0.0.1:8000/unstructured/process/", { 
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        document.getElementById("result").innerText = JSON.stringify(result, null, 2);
    }
    
    catch (error) {
        console.error("Error processing data:", error);
        document.getElementById("result").innerText = "An error occurred during processing.";
    }
});