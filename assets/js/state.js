/**
 * Reactive Dashboard State Manager.
 * Manages active filter state and notifies subscribed components.
 */
const DashboardState = (function () {
  let activeFilters = {
    contract: "ALL",
    tenure: "ALL",
    payment: "ALL"
  };

  const listeners = [];

  function getFilters() {
    return { ...activeFilters };
  }

  function setFilter(filterKey, value) {
    activeFilters[filterKey] = value;
    notifyListeners();
  }

  function resetFilters() {
    activeFilters = {
      contract: "ALL",
      tenure: "ALL",
      payment: "ALL"
    };
    notifyListeners();
  }

  function subscribe(fn) {
    listeners.push(fn);
  }

  function notifyListeners() {
    const filteredData = filterData();
    listeners.forEach((listener) => listener(filteredData, activeFilters));
  }

  function filterData() {
    return SUBSCRIBER_DATA.filter((item) => {
      const matchContract =
        activeFilters.contract === "ALL" || item.contract === activeFilters.contract;
      const matchTenure =
        activeFilters.tenure === "ALL" || item.bucket === activeFilters.tenure;
      const matchPayment =
        activeFilters.payment === "ALL" || item.payment === activeFilters.payment;
      return matchContract && matchTenure && matchPayment;
    });
  }

  return {
    getFilters,
    setFilter,
    resetFilters,
    subscribe,
    filterData
  };
})();
