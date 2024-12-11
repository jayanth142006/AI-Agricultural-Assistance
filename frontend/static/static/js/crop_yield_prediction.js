document.getElementById("cropYieldForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Send a POST request to the backend
    fetch("/api/crop_yield_prediction/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Show the predicted yield result
        if (result.predicted_yield) {
            document.getElementById("yieldResult").innerText = `Predicted Yield: ${result.predicted_yield}`;
        } else {
            document.getElementById("yieldResult").innerText = `Error: ${result.error}`;
        }
    })
    .catch(error => {
        document.getElementById("yieldResult").innerText = `Error: ${error.message}`;
    });
});
