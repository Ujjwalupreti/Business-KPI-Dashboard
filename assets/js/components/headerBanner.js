/**
 * Header Banner Component
 */
const HeaderBannerComponent = {
  render(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;

    el.innerHTML = `
      <header class="header-banner">
        <div class="header-title">
          <h1>Subscription Business KPI Executive Dashboard</h1>
          <p>Data Source: customer_churn_cleaned.csv | Track: Data Analytics & BI Development</p>
        </div>
        <div class="decision-badge">
          <strong>Core Decision Question</strong>
          <span>Which customer groups should a fictional subscription team contact first to reduce avoidable churn?</span>
        </div>
      </header>
    `;
  }
};
