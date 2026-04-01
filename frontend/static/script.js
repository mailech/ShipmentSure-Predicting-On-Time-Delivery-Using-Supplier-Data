document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        Warehouse_block: document.getElementById("Warehouse_block").value,
        Mode_of_Shipment: document.getElementById("Mode_of_Shipment").value,
        Customer_care_calls: Number(document.getElementById("Customer_care_calls").value),
        Customer_rating: Number(document.getElementById("Customer_rating").value),
        Cost_of_the_Product: Number(document.getElementById("Cost_of_the_Product").value),
        Prior_purchases: Number(document.getElementById("Prior_purchases").value),
        Product_importance: document.getElementById("Product_importance").value,
        Gender: document.getElementById("Gender").value,
        Discount_offered: Number(document.getElementById("Discount_offered").value),
        Weight_in_gms: Number(document.getElementById("Weight_in_gms").value)
    };

    const res = await fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();

    document.getElementById("result").innerText =
        result.prediction + " | Confidence: " + result.confidence;
});