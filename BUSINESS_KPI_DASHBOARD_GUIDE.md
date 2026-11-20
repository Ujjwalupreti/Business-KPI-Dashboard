# 📊 Business KPI Dashboard: Customer Churn & Retention Guide

**Role:** Senior BI Developer & Data Analyst  
**Project:** Subscription Churn & Revenue Risk Mitigation Dashboard  
**Dataset Used:** `customer_churn_cleaned.csv`  
**Deliverable Directory:** [c:/Users/Hp/Downloads/EDAI/KPI](file:///c:/Users/Hp/Downloads/EDAI/KPI)  
**Interactive Artifacts Generated:**  
- Ready-to-use Excel Dashboard: [customer_churn_kpi_dashboard.xlsx](file:///c:/Users/Hp/Downloads/EDAI/KPI/customer_churn_kpi_dashboard.xlsx)  
- Live Interactive Web/HTML Dashboard: [index.html](file:///c:/Users/Hp/Downloads/EDAI/KPI/index.html)  
- Production Cleaned Data: [customer_churn_cleaned.csv](file:///c:/Users/Hp/Downloads/EDAI/KPI/customer_churn_cleaned.csv)  

---

## 🎯 Executive Summary & Decision Question

> **Decision Question:**  
> **Which customer groups should a fictional subscription team contact first to reduce avoidable churn?**

### The Senior BI Solution Architecture
This guide provides an end-to-end, multi-tool blueprint (Power BI, Tableau, Excel/Google Sheets, Looker Studio) to turn clean customer churn data into a high-impact, single-page executive decision dashboard.

---

## 🧮 Step 1: Core KPIs, Helper Columns & Exact Formulas

### 1.1 Strict Analytical Constraints
- **Primary Key Rule:** Never aggregate `customer_id` as a numerical measure (use `DISTINCTCOUNT` / `COUNTD` / `COUNTA(UNIQUE(...))` only).
- **Separation of Evidence from Prediction:** All baseline KPIs measure empirical historical performance.
- **Correlation $\neq$ Causation:** High support tickets correlate strongly with churn, but support requests reflect customer friction rather than direct causation.

---

### 1.2 Multi-Tool Formula Reference Table

| Metric / Field | Power BI (DAX) | Tableau (Calculated Field) | Excel / Google Sheets Formula | Looker Studio Formula |
| :--- | :--- | :--- | :--- | :--- |
| **Total Customers** | `DISTINCTCOUNT(customer_churn_cleaned[customer_id])` | `COUNTD([customer_id])` | `=COUNTA(UNIQUE(A2:A16))` | `COUNT_DISTINCT(customer_id)` |
| **Churned Customers** | `CALCULATE(DISTINCTCOUNT(customer_churn_cleaned[customer_id]), customer_churn_cleaned[churned] = "Yes")` | `COUNTD(IF [churned] = 'Yes' THEN [customer_id] END)` | `=COUNTIF(L2:L16, "Yes")` | `COUNT_DISTINCT(CASE WHEN churned = "Yes" THEN customer_id END)` |
| **Retained Customers** | `CALCULATE(DISTINCTCOUNT(customer_churn_cleaned[customer_id]), customer_churn_cleaned[churned] = "No")` | `COUNTD(IF [churned] = 'No' THEN [customer_id] END)` | `=COUNTIF(L2:L16, "No")` | `COUNT_DISTINCT(CASE WHEN churned = "No" THEN customer_id END)` |
| **Churn Rate (%)** | `DIVIDE([Churned Customers], [Total Customers], 0)` *(Format: `0.0%`)* | `[Churned Customers] / [Total Customers]` *(Format: `0.0%`)* | `=COUNTIF(L2:L16, "Yes") / COUNTA(A2:A16)` | `[Churned Customers] / [Total Customers]` |
| **Retention Rate (%)** | `1 - [Churn Rate]` *(or `DIVIDE([Retained Customers], [Total Customers], 0)`)* | `1 - [Churn Rate]` | `=COUNTIF(L2:L16, "No") / COUNTA(A2:A16)` | `1 - [Churn Rate]` |
| **Monthly Revenue at Risk (INR)** | `CALCULATE(SUM(customer_churn_cleaned[monthly_charge]), customer_churn_cleaned[churned] = "Yes")` *(Format: `₹#,##0.00`)* | `SUM(IF [churned] = 'Yes' THEN [monthly_charge] END)` *(Format: Currency `₹`)* | `=SUMIF(L2:L16, "Yes", F2:F16)` *(Format: `₹#,##0.00`)* | `SUM(CASE WHEN churned = "Yes" THEN monthly_charge ELSE 0 END)` |
| **Average Tenure (Overall)** | `AVERAGE(customer_churn_cleaned[tenure_months])` *(Format: `0.0` mos)* | `AVG([tenure_months])` | `=AVERAGE(D2:D16)` | `AVG(tenure_months)` |
| **Median Tenure (Overall)** | `MEDIAN(customer_churn_cleaned[tenure_months])` | `MEDIAN([tenure_months])` | `=MEDIAN(D2:D16)` | `MEDIAN(tenure_months)` |
| **Avg Tenure (Churned)** | `CALCULATE(AVERAGE(customer_churn_cleaned[tenure_months]), customer_churn_cleaned[churned] = "Yes")` | `AVG(IF [churned] = 'Yes' THEN [tenure_months] END)` | `=AVERAGEIF(L2:L16, "Yes", D2:D16)` | `AVG(CASE WHEN churned = "Yes" THEN tenure_months END)` |
| **Avg Tenure (Retained)** | `CALCULATE(AVERAGE(customer_churn_cleaned[tenure_months]), customer_churn_cleaned[churned] = "No")` | `AVG(IF [churned] = 'No' THEN [tenure_months] END)` | `=AVERAGEIF(L2:L16, "No", D2:D16)` | `AVG(CASE WHEN churned = "No" THEN tenure_months END)` |
| **Median Tenure (Churned)** | `CALCULATE(MEDIAN(customer_churn_cleaned[tenure_months]), customer_churn_cleaned[churned] = "Yes")` | `MEDIAN(IF [churned] = 'Yes' THEN [tenure_months] END)` | `=MEDIAN(IF(L2:L16="Yes", D2:D16))` *(Dynamic Array / Ctrl+Shift+Enter)* | `MEDIAN(CASE WHEN churned = "Yes" THEN tenure_months END)` |
| **Median Tenure (Retained)** | `CALCULATE(MEDIAN(customer_churn_cleaned[tenure_months]), customer_churn_cleaned[churned] = "No")` | `MEDIAN(IF [churned] = 'No' THEN [tenure_months] END)` | `=MEDIAN(IF(L2:L16="No", D2:D16))` | `MEDIAN(CASE WHEN churned = "No" THEN tenure_months END)` |

---

### 1.3 Helper Fields: Tenure Buckets & Segmentation Logic

#### A. Tenure Buckets (`tenure_bucket`)
Creates standardized cohorts for cohort analysis and slicers:

**Power BI (Calculated Column):**
```dax
Tenure Bucket = 
SWITCH(
    TRUE(),
    customer_churn_cleaned[tenure_months] <= 6, "0–6m",
    customer_churn_cleaned[tenure_months] <= 12, "7–12m",
    customer_churn_cleaned[tenure_months] <= 24, "13–24m",
    "25m+"
)
```
*(Sort by numeric order column `Tenure Bucket Sort`: `1` for `0–6m`, `2` for `7–12m`, `3` for `13–24m`, `4` for `25m+`)*

**Tableau (Calculated Field):**
```tableau
IF [tenure_months] <= 6 THEN '0–6m'
ELSEIF [tenure_months] <= 12 THEN '7–12m'
ELSEIF [tenure_months] <= 24 THEN '13–24m'
ELSE '25m+'
END
```

**Excel / Google Sheets:**
```excel
=IFS(D2<=6, "0–6m", D2<=12, "7–12m", D2<=24, "13–24m", TRUE, "25m+")
```

**Looker Studio:**
```sql
CASE 
  WHEN tenure_months <= 6 THEN "0–6m" 
  WHEN tenure_months <= 12 THEN "7–12m" 
  WHEN tenure_months <= 24 THEN "13–24m" 
  ELSE "25m+" 
END
```

#### B. Priority Outreach Tier (`priority_tier`)
Identifies highest-risk customers for immediate intervention:

**Power BI (Calculated Column):**
```dax
Priority Tier = 
SWITCH(
    TRUE(),
    customer_churn_cleaned[contract_type_standardized] = "Monthly" && customer_churn_cleaned[support_tickets] >= 3, "Tier 1: Emergency Outreach (100% Churn)",
    customer_churn_cleaned[tenure_months] <= 6 && customer_churn_cleaned[support_tickets] >= 2, "Tier 2: Proactive Onboarding Assist",
    "Tier 3: Low Risk / Retained"
)
```

---

## 📐 Step 2: Dashboard Layout & Interactive Slicers

### 2.1 Single-Page Executive Wireframe Layout

```text
+-------------------------------------------------------------------------------------------------------+
| 📊 SUBSCRIPTION BUSINESS KPI EXECUTIVE DASHBOARD                                                      |
| Decision Question: Which customer groups should the subscription team contact first to reduce churn?  |
+-------------------------------------------------------------------------------------------------------+
| 🔍 FILTERS: [Contract Type: ALL v]  [Tenure Bucket: ALL v]  [Payment Method: ALL v]  [Reset Filters]  |
+-------------------------------------------------------------------------------------------------------+
| [ Total Customers ] | [ Churn Rate (%) ] | [ Retention Rate ] | [ Rev at Risk (₹) ] | [ Tenure Split ]|
|        15           |       46.7%        |       53.3%        |      ₹409.93        |  7.0m vs 29.1m  |
+---------------------+--------------------+--------------------+---------------------+-----------------+
| VISUAL 1: Churn Rate by Contract         | VISUAL 2: Revenue at Risk by Tenure Bucket                 |
| (Bar Chart: Monthly 100% vs Annual 0%)   | (Column Chart: 0-6m ₹199.96, 7-12m ₹129.98...)             |
| [Insight: 100% churn in Monthly plans]   | [Insight: 80.5% revenue risk concentrated in <=12m]        |
+------------------------------------------+------------------------------------------------------------+
| VISUAL 3: Support Tickets vs Churn Status| VISUAL 4: Churn Rate by Subscription Tier                  |
| (Grouped Bar: 0-2 tickets vs 3+ tickets) | (Bar Chart: Basic 71.4%, Pro 50.0%, Enterprise 0.0%)       |
| [Insight: Inflection point at 3+ tickets]| [Insight: Enterprise accounts show 0% churn]               |
+-------------------------------------------------------------------------------------------------------+
| VISUAL 5: ACTIONABLE PRIORITY OUTREACH ROSTER TABLE                                                   |
| Columns: Customer ID | Age/Gender | Tenure | Bucket | Plan | Monthly Fee | Contract | Tickets | Tier  |
| (Conditional Formatting: Red highlight for Churned & Tier 1, Green for Retained)                      |
+-------------------------------------------------------------------------------------------------------+
```

### 2.2 Slicer & Filter Configuration

1. **Contract Type Slicer:**
   - **Field:** `contract_type_standardized` (or `contract_type`).
   - **Control Style:** Dropdown or Horizontal Button Tile Bar.
   - **Selection:** Single or Multi-select with an "All" default.
   - **Behavior:** Slices all cards, charts, and table rows simultaneously.

2. **Tenure Slicer:**
   - **Field:** `tenure_bucket` (Categorical buttons) or `tenure_months` (Between Range Slider).
   - **Recommended:** `tenure_bucket` (`0–6m`, `7–12m`, `13–24m`, `25m+`). Ensures immediate visual cohort filtering.

3. **Payment Method Slicer:**
   - **Field:** `payment_method` (`Credit Card`, `UPI`, `Bank Transfer`, `Debit Card`).
   - **Note on Missing Data:** If `payment_method` were ever absent in future datasets, replace with `support_tickets` Tier (`Low: 0–1`, `Moderate: 2`, `High: 3+`).

---

## 🎨 Step 3: Visualizations & Accessible Design

### 3.1 Colorblind-Safe Accessible Color Palette

| Purpose | Semantic Role | Hex Code | Swatch Preview | Contrast Ratio |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Navy** | Canvas Headers / Cards | `#1B365D` | Deep Navy | Compliant WCAG AAA |
| **Retained Blue** | Retained Customers / Safe | `#1F77B4` | Accessible Slate Blue | Compliant WCAG AA |
| **Churn Alert Red** | Churned / Revenue at Risk | `#D62728` | High-Contrast Crimson | Compliant WCAG AA |
| **Warning Orange** | Moderate Risk / Pro Tier | `#FF7F0E` | Amber Orange | Compliant WCAG AA |
| **Neutral Background**| Page / Card Fill | `#F8FAFC` | Off-White / Ghost Gray | Reduces eye strain |
| **Grid / Borders** | Structural Dividers | `#E2E8F0` | Light Border Gray | Subtle layout framing |

---

### 3.2 Visual Specifications & Setup

#### Visual 1: Churn Rate by Contract Commitment Type
- **Chart Type:** Clustered Horizontal Bar Chart (or 100% Column Chart).
- **X-Axis:** Observed Churn Rate (`0%` to `100%`).
- **Y-Axis:** Contract Commitment (`Monthly`, `Annual`, `Two-Year`).
- **Sorting:** Descending by Churn Rate (`Monthly` on top).
- **Color:** Red (`#D62728`) for Monthly; Blue (`#1F77B4`) for Annual & Two-Year.
- **Data Labels:** Inside End (`100.0%`, `0.0%`, `0.0%`).

#### Visual 2: Monthly Revenue at Risk by Tenure Bucket
- **Chart Type:** Vertical Column Chart.
- **X-Axis:** `tenure_bucket` (`0–6m`, `7–12m`, `13–24m`, `25m+`).
- **Y-Axis:** Monthly Revenue at Risk (`₹0` to `₹250`).
- **Sorting:** Chronological by tenure order (`0–6m` $\to$ `25m+`).
- **Color:** Red Alert (`#D62728`).
- **Data Labels:** Above Bar with currency formatting (`₹199.96`, `₹129.98`, `₹79.99`, `₹0.00`).

#### Visual 3: Support Inquiries (90 Days) vs. Churn Outcome
- **Chart Type:** Grouped Column Count Chart.
- **X-Axis:** `support_tickets` ($0, 1, 2, 3, 4, 5, 6$).
- **Y-Axis:** Customer Count ($0$ to $5$).
- **Legend:** `churned` (Retained: `#1F77B4`, Churned: `#D62728`).
- **Annotation:** Vertical dashed red reference line at ticket count $= 2.5$ with label: *"Sharp Inflection: 100% Churn at $\ge 3$ tickets"*.

#### Visual 4: Churn Rate by Subscription Plan Tier
- **Chart Type:** Bar Chart.
- **X-Axis:** Subscription Tier (`Basic`, `Pro`, `Enterprise`).
- **Y-Axis:** Churn Rate (`0%` to `100%`).
- **Data Labels:** `71.4%` (Basic), `50.0%` (Pro), `0.0%` (Enterprise).

#### Visual 5: Actionable Priority Outreach Roster (Bottom Action Table)
- **Component:** Interactive Matrix / Table with Conditional Formatting.
- **Columns:** `customer_id`, `gender`/`age`, `tenure_months`, `tenure_bucket`, `subscription_type`, `monthly_charge`, `contract_type_standardized`, `support_tickets`, `churned`, `priority_tier`.
- **Conditional Formatting:**
  - `churned = "Yes"`: Soft red pill badge (`#FEE2E2` text `#991B1B`).
  - `churned = "No"`: Soft green pill badge (`#DCFCE7` text `#15803D`).
  - `priority_tier = Tier 1`: Highlighted row border.

---

## 📝 Step 4: Written Insights & Executive Outreach Plan

### 4.1 Visual Insight Callouts (Ready-to-Paste for Portfolio)

1. **Beside Visual 1 (Contract Type):**
   > *"Descriptive Finding: 100% of churned accounts (7 of 7) were subscribed to Month-to-Month contracts, whereas Annual and Two-Year plans experienced zero churn. Monthly contracts provide zero switching friction when customer dissatisfaction arises."*

2. **Beside Visual 2 (Tenure Buckets):**
   > *"Descriptive Finding: 80.5% of total revenue at risk (₹329.94) is concentrated in subscribers within their first 12 months. Churn drops to zero once customer accounts mature past 24 months."*

3. **Beside Visual 3 (Support Ticket Volume):**
   > *"Descriptive Finding: A clear inflection point occurs at 3 support inquiries; all accounts with 2 or fewer tickets were retained, while all accounts with 3 or more tickets churned. High ticket volume serves as an operational proxy for product friction rather than a direct cause of churn."*

4. **Beside Visual 4 (Subscription Tier):**
   > *"Descriptive Finding: Churn is inversely associated with subscription tier: Basic subscribers experienced 71.4% churn, Pro experienced 50.0%, and Enterprise experienced 0.0%."*

---

### 4.2 Priority Outreach Summary (Answering the Decision Question)

> **Decision Question:** *Which customer groups should a fictional subscription team contact first to reduce avoidable churn?*

The subscription team should implement a 3-tiered triage protocol based on the empirical friction signals:

| Priority Tier | Target Customer Cohort | Operational Trigger | Recommended Action | Business Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Emergency Outreach (Immediate)** | Month-to-Month subscribers with $\ge 3$ support tickets in prior 90 days | Support tickets $\ge 3$ on monthly billing | **Senior Technical Check-in:** Inbound routing to senior specialists and outbound phone check-in within 24h, plus courtesy credit. | Focuses directly on the 100% churn risk segment to rescue accounts before contract expiration. |
| **Tier 2: Early Friction Assist (Proactive)** | Early-tenure accounts ($< 6$ months) on Basic/Pro tiers | Customer logs their **2nd** support ticket | **Guided Onboarding Assist:** Automated outreach from Customer Success to resolve initial setup roadblocks. | Intervenes before ticket count hits the critical 3-ticket threshold. |
| **Tier 3: Commercial Migration (Strategic)** | Month-to-Month subscribers reaching 5 or 11 months tenure | Milestone tenure anniversary | **Contract Upgrade Incentive:** Offer a 10–15% annual discount or 2 free months upon migrating to an Annual plan. | Locks in predictable recurring revenue and eliminates monthly cancellation exposure. |

---

## 💻 Built-In Project Artifacts

You can immediately explore and present the generated dashboard assets in [c:/Users/Hp/Downloads/EDAI/KPI](file:///c:/Users/Hp/Downloads/EDAI/KPI):

1. **Working Excel Dashboard:** [customer_churn_kpi_dashboard.xlsx](file:///c:/Users/Hp/Downloads/EDAI/KPI/customer_churn_kpi_dashboard.xlsx)  
   *Pre-built with Excel formulas (`COUNTIF`, `SUMIF`, `IFS`), formatted KPI cards, tenure bucket breakdowns, and conditional formatting.*
2. **Interactive HTML Dashboard:** [index.html](file:///c:/Users/Hp/Downloads/EDAI/KPI/index.html)  
   *Double-click to open in Chrome/Edge or host directly on GitHub Pages! Features real-time interactive JavaScript slicers (Contract, Tenure, Payment Method) and dynamic Chart.js visuals.*
3. **Clean Production CSV:** [customer_churn_cleaned.csv](file:///c:/Users/Hp/Downloads/EDAI/KPI/customer_churn_cleaned.csv)  
   *Ready to import into Power BI, Tableau Desktop, or Looker Studio.*

