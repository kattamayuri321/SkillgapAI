fetch("http://127.0.0.1:5000/analyze")
.then(res => res.json())
.then(data => {

    document.getElementById("matchPercent").innerText =
        data.percentages.matched + "%";

    document.getElementById("matchedCount").innerText = data.matched.length;
    document.getElementById("partialCount").innerText = data.partial.length;
    document.getElementById("missingCount").innerText = data.missing.length;

    const matrixDiv = document.getElementById("matrix");

    matrixDiv.innerHTML = "<div></div>";
    data.job_skills.forEach(s => {
        matrixDiv.innerHTML += `<b>${s}</b>`;
    });

    data.user_skills.forEach((u, i) => {
        matrixDiv.innerHTML += `<b>${u}</b>`;
        data.matrix[i].forEach(val => {
            let cls = val >= 0.75 ? "high" : val >= 0.4 ? "medium" : "low";
            matrixDiv.innerHTML += `<div class="cell ${cls}">${val}</div>`;
        });
    });

    new Chart(document.getElementById("skillChart"), {
        type: "doughnut",
        data: {
            labels: ["Matched", "Partial", "Missing"],
            datasets: [{
                data: [
                    data.percentages.matched,
                    data.percentages.partial,
                    data.percentages.missing
                ],
                backgroundColor: ["green", "orange", "red"]
            }]
        },
        options: {
            cutout: "65%",
            plugins: { legend: { position: "bottom" } }
        }
    });
});
