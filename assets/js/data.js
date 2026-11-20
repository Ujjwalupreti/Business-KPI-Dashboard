/**
 * Subscriber dataset store.
 * Sourced from customer_churn_cleaned.csv
 */
const SUBSCRIBER_DATA = [
  { id: "CUST-1001", gender: "Female", age: 34, tenure: 12, bucket: "7–12m", plan: "Basic", charge: 49.99, contract: "Monthly", tickets: 3, payment: "Credit Card", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1002", gender: "Male", age: 45, tenure: 24, bucket: "13–24m", plan: "Pro", charge: 79.99, contract: "Annual", tickets: 1, payment: "Bank Transfer", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1003", gender: "Female", age: 29, tenure: 6, bucket: "0–6m", plan: "Basic", charge: 49.99, contract: "Monthly", tickets: 5, payment: "UPI", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1004", gender: "Male", age: 52, tenure: 36, bucket: "25m+", plan: "Enterprise", charge: 149.99, contract: "Two-Year", tickets: 0, payment: "Credit Card", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1005", gender: "Female", age: 41, tenure: 8, bucket: "7–12m", plan: "Pro", charge: 79.99, contract: "Monthly", tickets: 4, payment: "Debit Card", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1006", gender: "Male", age: 31, tenure: 18, bucket: "13–24m", plan: "Basic", charge: 49.99, contract: "Annual", tickets: 2, payment: "UPI", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1007", gender: "Female", age: 23, tenure: 3, bucket: "0–6m", plan: "Basic", charge: 49.99, contract: "Monthly", tickets: 6, payment: "Credit Card", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1008", gender: "Male", age: 60, tenure: 48, bucket: "25m+", plan: "Enterprise", charge: 149.99, contract: "Two-Year", tickets: 1, payment: "Bank Transfer", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1009", gender: "Female", age: 38, tenure: 15, bucket: "13–24m", plan: "Pro", charge: 79.99, contract: "Annual", tickets: 2, payment: "Credit Card", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1010", gender: "Male", age: 27, tenure: 4, bucket: "0–6m", plan: "Basic", charge: 49.99, contract: "Monthly", tickets: 4, payment: "UPI", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1011", gender: "Female", age: 49, tenure: 30, bucket: "25m+", plan: "Enterprise", charge: 149.99, contract: "Two-Year", tickets: 0, payment: "Credit Card", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1012", gender: "Male", age: 33, tenure: 14, bucket: "13–24m", plan: "Pro", charge: 79.99, contract: "Monthly", tickets: 3, payment: "Debit Card", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1013", gender: "Female", age: 55, tenure: 22, bucket: "13–24m", plan: "Basic", charge: 49.99, contract: "Annual", tickets: 1, payment: "Bank Transfer", churned: "No", priority: "Tier 3: Low Risk / Retained" },
  { id: "CUST-1014", gender: "Male", age: 26, tenure: 2, bucket: "0–6m", plan: "Basic", charge: 49.99, contract: "Monthly", tickets: 5, payment: "UPI", churned: "Yes", priority: "Tier 1: Emergency Outreach" },
  { id: "CUST-1015", gender: "Female", age: 43, tenure: 40, bucket: "25m+", plan: "Enterprise", charge: 149.99, contract: "Two-Year", tickets: 1, payment: "Credit Card", churned: "No", priority: "Tier 3: Low Risk / Retained" }
];

