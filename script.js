async function submitForm() {
    const context = document.getElementById('context').value;
    const files = document.getElementById('screenshots').files;

    const formData = new FormData();
    formData.append('context', context);
    for (let i = 0; i < files.length; i++) {
        formData.append('screenshots', files[i]);
    }

    console.log("Form data prepared:", formData);
    
    try {
        console.log("Sending request to the backend...");
        const response = await fetch('http://127.0.0.1:5000/generate-instructions', {
            method: 'POST',
            body: formData
        });

        console.log("Response received:", response);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.text();
        
        const htmlContent = result;

       
        document.getElementById('result').innerHTML = htmlContent;
      
    } catch (error) {
        console.error("Error during fetch:", error);
        document.getElementById('result').innerText = "An error occurred: " + error.message;
    }
}
