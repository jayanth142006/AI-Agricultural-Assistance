document.getElementById("cropForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
        nitrogen: +document.getElementById("nitrogen").value,
        phosphorus: +document.getElementById("phosphorus").value,
        potassium: +document.getElementById("potassium").value,
        temperature: +document.getElementById("temperature").value,
        humidity: +document.getElementById("humidity").value,
        ph: +document.getElementById("ph").value,
        rainfall: +document.getElementById("rainfall").value,
    };

    try {
        const response = await fetch("/api/crop_recommendation/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        const resultDiv = document.getElementById("result");

        if (result.recommended_crop) {
            resultDiv.innerText = `Recommended Crop: ${result.recommended_crop}`;
        } else {
            resultDiv.innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById("result").innerText = `Error: ${error.message}`;
    }
});

