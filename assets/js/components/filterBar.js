/**
 * Filter Bar Component (Interactive Slicers)
 */
const FilterBarComponent = {
  render(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;

    el.innerHTML = `
      <section class="filters-bar">
        <span class="filter-label">Interactive Slicers:</span>
        <div class="filter-group">
          <label for="filterContract">Contract:</label>
          <select id="filterContract">
            <option value="ALL">All Contracts</option>
            <option value="Monthly">Monthly</option>
            <option value="Annual">Annual</option>
            <option value="Two-Year">Two-Year</option>
          </select>
        </div>
        <div class="filter-group">
          <label for="filterTenure">Tenure Bucket:</label>
          <select id="filterTenure">
            <option value="ALL">All Tenures</option>
            <option value="0–6m">0–6 months</option>
            <option value="7–12m">7–12 months</option>
            <option value="13–24m">13–24 months</option>
            <option value="25m+">25+ months</option>
          </select>
        </div>
        <div class="filter-group">
          <label for="filterPayment">Payment Method:</label>
          <select id="filterPayment">
            <option value="ALL">All Methods</option>
            <option value="Credit Card">Credit Card</option>
            <option value="UPI">UPI</option>
            <option value="Bank Transfer">Bank Transfer</option>
            <option value="Debit Card">Debit Card</option>
          </select>
        </div>
        <button class="btn-reset" id="btnResetFilters">Reset Filters</button>
      </section>
    `;

    // Wire DOM events to State Manager
    document.getElementById("filterContract").addEventListener("change", (e) => {
      DashboardState.setFilter("contract", e.target.value);
    });

    document.getElementById("filterTenure").addEventListener("change", (e) => {
      DashboardState.setFilter("tenure", e.target.value);
    });

    document.getElementById("filterPayment").addEventListener("change", (e) => {
      DashboardState.setFilter("payment", e.target.value);
    });

    document.getElementById("btnResetFilters").addEventListener("click", () => {
      document.getElementById("filterContract").value = "ALL";
      document.getElementById("filterTenure").value = "ALL";
      document.getElementById("filterPayment").value = "ALL";
      DashboardState.resetFilters();
    });
  }
};

