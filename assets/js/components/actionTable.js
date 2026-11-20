/**
 * Actionable Priority Customer Outreach Table Component
 */
const ActionTableComponent = {
  render(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;

    el.innerHTML = `
      <section class="table-card">
        <div class="table-header">
          <div class="table-title">
            <h3>🎯 Prioritized Customer Outreach Roster</h3>
            <p style="font-size: 13px; color: var(--text-muted); margin-top: 2px;">
              Dynamically filtered action list answering the decision question for the subscription retention team.
            </p>
          </div>
        </div>
        <div class="table-wrapper">
          <table id="rosterTable">
            <thead>
              <tr>
                <th>Customer ID</th>
                <th>Gender / Age</th>
                <th>Tenure</th>
                <th>Tenure Bucket</th>
                <th>Plan Tier</th>
                <th>Monthly Fee</th>
                <th>Contract</th>
                <th>Tickets (90d)</th>
                <th>Payment Method</th>
                <th>Churn Status</th>
                <th>Outreach Priority Tier</th>
              </tr>
            </thead>
            <tbody id="rosterBody">
              <!-- Rendered via update() -->
            </tbody>
          </table>
        </div>
      </section>
    `;
  },

  update(filteredData) {
    const tbody = document.getElementById("rosterBody");
    if (!tbody) return;

    tbody.innerHTML = "";

    if (filteredData.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="11" style="text-align: center; padding: 24px; color: #64748b;">
            No matching subscriber accounts found for the selected filter combination.
          </td>
        </tr>
      `;
      return;
    }

    // Sort: Churned (Yes) first, then tickets descending
    const sorted = [...filteredData].sort(
      (a, b) =>
        (b.churned === "Yes" ? 1 : -1) - (a.churned === "Yes" ? 1 : -1) ||
        b.tickets - a.tickets
    );

    sorted.forEach((row) => {
      const tr = document.createElement("tr");

      const churnBadge =
        row.churned === "Yes"
          ? '<span class="badge badge-churned">Yes</span>'
          : '<span class="badge badge-retained">No</span>';

      let priorityBadge = '<span class="badge badge-t3">Tier 3: Low Risk</span>';
      if (row.priority.includes("Tier 1")) {
        priorityBadge = '<span class="badge badge-t1">Tier 1: Emergency Outreach</span>';
      } else if (row.priority.includes("Tier 2")) {
        priorityBadge = '<span class="badge badge-t2">Tier 2: Onboarding Assist</span>';
      }

      tr.innerHTML = `
        <td><strong>${row.id}</strong></td>
        <td>${row.gender}, ${row.age}</td>
        <td>${row.tenure} mos</td>
        <td>${row.bucket}</td>
        <td>${row.plan}</td>
        <td>₹${row.charge.toFixed(2)}</td>
        <td>${row.contract}</td>
        <td><strong>${row.tickets}</strong></td>
        <td>${row.payment}</td>
        <td>${churnBadge}</td>
        <td>${priorityBadge}</td>
      `;
      tbody.appendChild(tr);
    });
  }
};

