async function predict() {

    const data = {
        warehouse: document.getElementById("warehouse").value,
        mode: document.getElementById("mode").value,
        calls: document.getElementById("calls").value,
        rating: document.getElementById("rating").value,
        cost: document.getElementById("cost").value,
        purchases: document.getElementById("purchases").value,
        importance: document.getElementById("importance").value,
        gender: document.getElementById("gender").value,
        discount: document.getElementById("discount").value,
        weight: document.getElementById("weight").value
    };

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        console.log("Response:", result); // DEBUG

        if (result.error) {
            alert("Error: " + result.error);
            return;
        }

        document.getElementById("status").innerText = result.prediction;
        document.getElementById("confidence").innerText = result.confidence;

    } catch (error) {
        console.error("Fetch error:", error);
        alert("Something went wrong!");
    }
}