const labels = [];
const cpu = [];
const memory = [];
const disk = [];

// Read values directly from the table
document.querySelectorAll("table tbody tr").forEach(row => {
  labels.push(row.children[0].innerText);     // # column
  cpu.push(Number(row.children[1].innerText));
  memory.push(Number(row.children[2].innerText));
  disk.push(Number(row.children[3].innerText));
});

new Chart(document.getElementById("metricsChart"), {
  type: "line",
  data: {
    labels: labels,   // 🔥 SAME AS TABLE NUMBERS
    datasets: [
      {
        label: "CPU (%)",
        data: cpu,
        borderColor: "#00b4d8",
        tension: 0.4
      },
      {
        label: "Memory (%)",
        data: memory,
        borderColor: "#80ed99",
        tension: 0.4
      },
      {
        label: "Disk (%)",
        data: disk,
        borderColor: "#ffb703",
        tension: 0.4
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#e5e7eb" }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Record Number (Current Page)",
          color: "#e5e7eb"
        },
        ticks: { color: "#9ca3af" }
      },
      y: {
        min: 0,
        max: 100,
        title: {
          display: true,
          text: "Resource Utilization (%)",
          color: "#e5e7eb"
        },
        ticks: { color: "#9ca3af" }
      }
    }
  }
});
