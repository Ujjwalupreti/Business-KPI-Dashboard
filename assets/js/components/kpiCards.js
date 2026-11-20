/**
 * KPI Cards Banner Component
 */
const KpiCardsComponent = {
  render(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;

    el.innerHTML = `
      <section class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-title">Total Active Accounts</div>
          <div class="kpi-value" id="kpiTotalCust">-</div>
          <div class="kpi-subtext">Distinct subscriber count</div>
        </div>
        <div class="kpi-card alert">
          <div class="kpi-title">Observed Churn Rate</div>
          <div class="kpi-value" id="kpiChurnRate">-</div>
          <div class="kpi-subtext" id="kpiChurnCount">-</div>
        </div>
        <div class="kpi-card success">
          <div class="kpi-title">Customer Retention Rate</div>
          <div class="kpi-value" id="kpiRetRate">-</div>
          <div class="kpi-subtext" id="kpiRetCount">-</div>
        </div>
        <div class="kpi-card alert">
          <div class="kpi-title">Monthly Revenue at Risk</div>
          <div class="kpi-value" id="kpiRevRisk">-</div>
          <div class="kpi-subtext" id="kpiRevPct">-</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">Tenure (Churn vs Retained)</div>
          <div class="kpi-value" id="kpiTenureSplit">-</div>
          <div class="kpi-subtext">Average completed months</div>
        </div>
      </section>
    `;
  },

  update(filteredData) {
    const total = filteredData.length;
    const churned = filteredData.filter((d) => d.churned === "Yes").length;
    const retained = total - churned;

    const churnRate = total > 0 ? ((churned / total) * 100).toFixed(1) + "%" : "0.0%";
    const retRate = total > 0 ? ((retained / total) * 100).toFixed(1) + "%" : "0.0%";

    const totalRev = filteredData.reduce((acc, d) => acc + d.charge, 0);
    const revRisk = filteredData
      .filter((d) => d.churned === "Yes")
      .reduce((acc, d) => acc + d.charge, 0);
    const revRiskPct = totalRev > 0 ? ((revRisk / totalRev) * 100).toFixed(1) + "%" : "0.0%";

    const churnTenures = filteredData.filter((d) => d.churned === "Yes").map((d) => d.tenure);
    const retTenures = filteredData.filter((d) => d.churned === "No").map((d) => d.tenure);

    const avgChurnTenure =
      churnTenures.length > 0
        ? (churnTenures.reduce((a, b) => a + b, 0) / churnTenures.length).toFixed(1) + "m"
        : "N/A";
    const avgRetTenure =
      retTenures.length > 0
        ? (retTenures.reduce((a, b) => a + b, 0) / retTenures.length).toFixed(1) + "m"
        : "N/A";

    document.getElementById("kpiTotalCust").textContent = total;
    document.getElementById("kpiChurnRate").textContent = churnRate;
    document.getElementById("kpiChurnCount").textContent = `${churned} of ${total} churned`;
    document.getElementById("kpiRetRate").textContent = retRate;
    document.getElementById("kpiRetCount").textContent = `${retained} of ${total} retained`;
    document.getElementById("kpiRevRisk").textContent = "₹" + revRisk.toFixed(2);
    document.getElementById("kpiRevPct").textContent = `${revRiskPct} of filtered billing`;
    document.getElementById("kpiTenureSplit").textContent = `${avgChurnTenure} vs ${avgRetTenure}`;
  }
};
