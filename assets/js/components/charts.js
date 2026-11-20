/**
 * Charts Component (Chart.js visualizations)
 */
const ChartsComponent = {
  chartInstances: {},

  render(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;

    el.innerHTML = `
      <section class="charts-grid">
        <!-- Chart 1: Churn by Contract -->
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <h3>Observed Churn Rate by Contract Commitment</h3>
              <p>Comparing churn rate (%) across contract durations</p>
            </div>
          </div>
          <div class="chart-body">
            <canvas id="chartContract"></canvas>
          </div>
          <div class="chart-insight">
            <strong>Descriptive Insight:</strong> 100% of Month-to-Month accounts churned (7 of 7), while Annual and Two-Year contracts had 0% churn. Monthly terms impose no exit friction.
          </div>
        </div>

        <!-- Chart 2: Revenue at Risk by Tenure -->
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <h3>Monthly Revenue at Risk (INR) by Tenure Bucket</h3>
              <p>Total monthly charge of churned accounts by customer lifecycle stage</p>
            </div>
          </div>
          <div class="chart-body">
            <canvas id="chartTenureRev"></canvas>
          </div>
          <div class="chart-insight">
            <strong>Descriptive Insight:</strong> 80.5% of total revenue at risk (₹329.94) is concentrated in subscribers in their first 12 months. Churn is zero for accounts older than 24 months.
          </div>
        </div>

        <!-- Chart 3: Support Tickets vs Churn -->
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <h3>Customer Support Inquiries (90 Days) vs. Churn Status</h3>
              <p>Subscriber count across ticket frequency bands</p>
            </div>
          </div>
          <div class="chart-body">
            <canvas id="chartTickets"></canvas>
          </div>
          <div class="chart-insight">
            <strong>Descriptive Insight:</strong> Every customer filing 3 or more tickets churned (7/7). High ticket volume is an operational friction symptom rather than a direct cause of churn.
          </div>
        </div>

        <!-- Chart 4: Subscription Tier Distribution -->
        <div class="chart-card">
          <div class="chart-header">
            <div class="chart-title">
              <h3>Observed Churn Rate by Subscription Tier</h3>
              <p>Basic (₹49.99) vs Pro (₹79.99) vs Enterprise (₹149.99)</p>
            </div>
          </div>
          <div class="chart-body">
            <canvas id="chartPlan"></canvas>
          </div>
          <div class="chart-insight">
            <strong>Descriptive Insight:</strong> Basic tier subscribers exhibited 71.4% churn and Pro exhibited 50.0%, whereas Enterprise subscribers exhibited 0.0% churn.
          </div>
        </div>
      </section>
    `;

    this.initChartInstances();
  },

  initChartInstances() {
    // 1. Contract Chart
    const ctx1 = document.getElementById("chartContract").getContext("2d");
    this.chartInstances.contract = new Chart(ctx1, {
      type: "bar",
      data: {
        labels: ["Monthly", "Annual", "Two-Year"],
        datasets: [{
          label: "Churn Rate (%)",
          data: [100.0, 0.0, 0.0],
          backgroundColor: ["#d62728", "#1f77b4", "#1f77b4"],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, max: 110, ticks: { callback: (v) => v + "%" } }
        },
        plugins: { legend: { display: false } }
      }
    });

    // 2. Tenure Revenue Risk Chart
    const ctx2 = document.getElementById("chartTenureRev").getContext("2d");
    this.chartInstances.tenureRev = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: ["0–6m", "7–12m", "13–24m", "25m+"],
        datasets: [{
          label: "Revenue at Risk (₹)",
          data: [199.96, 129.98, 79.99, 0.0],
          backgroundColor: "#d62728",
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { callback: (v) => "₹" + v } }
        },
        plugins: { legend: { display: false } }
      }
    });

    // 3. Tickets vs Churn Chart
    const ctx3 = document.getElementById("chartTickets").getContext("2d");
    this.chartInstances.tickets = new Chart(ctx3, {
      type: "bar",
      data: {
        labels: ["0", "1", "2", "3", "4", "5", "6"],
        datasets: [
          { label: "Retained", data: [2, 4, 2, 0, 0, 0, 0], backgroundColor: "#1f77b4", borderRadius: 4 },
          { label: "Churned", data: [0, 0, 0, 2, 2, 2, 1], backgroundColor: "#d62728", borderRadius: 4 }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 1 } }
        }
      }
    });

    // 4. Plan Churn Chart
    const ctx4 = document.getElementById("chartPlan").getContext("2d");
    this.chartInstances.plan = new Chart(ctx4, {
      type: "bar",
      data: {
        labels: ["Basic (₹49.99)", "Pro (₹79.99)", "Enterprise (₹149.99)"],
        datasets: [{
          label: "Churn Rate (%)",
          data: [71.4, 50.0, 0.0],
          backgroundColor: ["#d62728", "#ff7f0e", "#16a34a"],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, max: 100, ticks: { callback: (v) => v + "%" } }
        },
        plugins: { legend: { display: false } }
      }
    });
  },

  update(filteredData) {
    if (!this.chartInstances.contract) return;

    // Recalculate Contract Churn Rates
    const contractTypes = ["Monthly", "Annual", "Two-Year"];
    const contractRates = contractTypes.map((ct) => {
      const match = filteredData.filter((d) => d.contract === ct);
      if (match.length === 0) return 0;
      const ch = match.filter((d) => d.churned === "Yes").length;
      return Number(((ch / match.length) * 100).toFixed(1));
    });
    this.chartInstances.contract.data.datasets[0].data = contractRates;
    this.chartInstances.contract.update();

    // Recalculate Tenure Revenue at Risk
    const tenureBuckets = ["0–6m", "7–12m", "13–24m", "25m+"];
    const tenureRevs = tenureBuckets.map((tb) => {
      return filteredData
        .filter((d) => d.bucket === tb && d.churned === "Yes")
        .reduce((sum, d) => sum + d.charge, 0);
    });
    this.chartInstances.tenureRev.data.datasets[0].data = tenureRevs;
    this.chartInstances.tenureRev.update();

    // Recalculate Ticket Counts
    const ticketLabels = ["0", "1", "2", "3", "4", "5", "6"];
    const retainedTickets = ticketLabels.map((t) => {
      return filteredData.filter((d) => d.tickets === Number(t) && d.churned === "No").length;
    });
    const churnedTickets = ticketLabels.map((t) => {
      return filteredData.filter((d) => d.tickets === Number(t) && d.churned === "Yes").length;
    });
    this.chartInstances.tickets.data.datasets[0].data = retainedTickets;
    this.chartInstances.tickets.data.datasets[1].data = churnedTickets;
    this.chartInstances.tickets.update();

    // Recalculate Plan Churn Rates
    const plans = [
      { name: "Basic", label: "Basic (₹49.99)" },
      { name: "Pro", label: "Pro (₹79.99)" },
      { name: "Enterprise", label: "Enterprise (₹149.99)" }
    ];
    const planRates = plans.map((p) => {
      const match = filteredData.filter((d) => d.plan === p.name);
      if (match.length === 0) return 0;
      const ch = match.filter((d) => d.churned === "Yes").length;
      return Number(((ch / match.length) * 100).toFixed(1));
    });
    this.chartInstances.plan.data.datasets[0].data = planRates;
    this.chartInstances.plan.update();
  }
};
