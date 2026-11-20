/**
 * Dashboard Application Bootstrap
 * Initializes all modular components and connects them to DashboardState.
 */
document.addEventListener("DOMContentLoaded", () => {
  // 1. Mount layout components
  HeaderBannerComponent.render("banner-root");
  FilterBarComponent.render("filters-root");
  KpiCardsComponent.render("kpi-root");
  ChartsComponent.render("charts-root");
  ActionTableComponent.render("table-root");

  // 2. Subscribe interactive components to reactive state changes
  DashboardState.subscribe((filteredData) => {
    KpiCardsComponent.update(filteredData);
    ChartsComponent.update(filteredData);
    ActionTableComponent.update(filteredData);
  });

  // 3. Initial state broadcast
  const initialData = DashboardState.filterData();
  KpiCardsComponent.update(initialData);
  ActionTableComponent.update(initialData);
});
