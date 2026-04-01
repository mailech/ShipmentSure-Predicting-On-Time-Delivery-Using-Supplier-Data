const historyBox = document.getElementById("history");

document.getElementById("form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "⏳ Analyzing shipment...";

    const data = {
        ID: Number(ID.value),
        Warehouse_block: Warehouse_block.value,
        Mode_of_Shipment: Mode_of_Shipment.value,
        Customer_care_calls: Number(Customer_care_calls.value),
        Customer_rating: Number(Customer_rating.value),
        Cost_of_the_Product: Number(Cost_of_the_Product.value),
        Prior_purchases: Number(Prior_purchases.value),
        Product_importance: Product_importance.value,
        Gender: Gender.value,
        Discount_offered: Number(Discount_offered.value),
        Weight_in_gms: Number(Weight_in_gms.value)
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await res.json();

        const confidence = Number(result.confidence) * 100;
        const confidenceText = confidence.toFixed(2);

        let color = "green";
        let risk = "Low Risk";

        // ✅ CORRECT RISK LOGIC
        if (result.prediction_label === "Late") {
            if (confidence > 70) {
                color = "red";
                risk = "High Risk";
            } else if (confidence > 40) {
                color = "yellow";
                risk = "Medium Risk";
            } else {
                color = "green";
                risk = "Low Risk";
            }
        } else { // On Time
            if (confidence > 70) {
                color = "green";
                risk = "Low Risk";
            } else {
                color = "yellow";
                risk = "Medium Risk";
            }
        }

        resultDiv.innerHTML = `
            <h3>${result.prediction_label}</h3>
            <p>Confidence: ${confidenceText}%</p>
            <p>Risk Level: ${risk}</p>

            <div class="bar">
                <div class="fill ${color}" style="width:${confidence}%"></div>
            </div>
        `;

        // HISTORY
        const entry = `ID ${data.ID} → ${result.prediction_label} (${confidenceText}%)`;
        historyBox.innerHTML = entry + "<br>" + historyBox.innerHTML;

    } catch (error) {
        resultDiv.innerHTML = "❌ Error connecting to server";
    }
});


// 🌙 DARK MODE
document.getElementById("toggleTheme").onclick = () => {
    document.body.classList.toggle("dark");
};


// ⚡ SAMPLE DATA
function fillSample() {
    ID.value = 5000;
    Warehouse_block.value = "A";
    Mode_of_Shipment.value = "Flight";
    Customer_care_calls.value = 4;
    Customer_rating.value = 3;
    Cost_of_the_Product.value = 200;
    Prior_purchases.value = 3;
    Product_importance.value = "low";
    Gender.value = "M";
    Discount_offered.value = 5;
    Weight_in_gms.value = 3000;
}