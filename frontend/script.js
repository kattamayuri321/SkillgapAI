let chart;

function analyze() {
  const formData = new FormData();
  formData.append("resume", document.getElementById("resume").files[0]);
  formData.append("jd", document.getElementById("jd").files[0]);

  fetch("http://127.0.0.1:5000/extract", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("skills").innerHTML =
      data.resume_skills.map(s => `<span>${s}</span>`).join("");

    document.getElementById("total").innerText = data.total_skills;
    document.getElementById("matched").innerText = data.matched_count;
    document.getElementById("percent").innerText = data.match_percentage;

    drawChart(data.matched_count, data.total_skills);
  });
}

function drawChart(matched, total) {
  const ctx = document.getElementById("chart");
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Matched", "Unmatched"],
      datasets: [{
        data: [matched, total - matched]
      }]
    }
  });
}
