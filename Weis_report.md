# Chain Store Project: Employee Learning Data

**Team GOLF**

Charlene Bui, Ellyn Ngo, Dulguun Soyol-Erdene, Selina Tang

---

## Background

A major regional grocery chain operating across the Mid-Atlantic and Northeast United States, primarily in Pennsylvania, is committed not only to providing high-quality products and services to its customers but also to fostering a high-performing workforce. To this end, the HR department invests significantly in Learning and Development (L&D) initiatives, including training programs, professional development courses, and leadership instruction. These offerings are structured across employee levels - from entry-level store associates to department managers and store managers - and are designed to enhance skills, engagement, and operational effectiveness across the organization's numerous store locations.

To provide context for the scale of this challenge: the organization operates approximately 200 stores across the Mid-Atlantic region and employs roughly 23,000 associates, generating approximately $4 billion in annual revenue. The breadth and complexity of this workforce make the effective allocation of L&D resources a strategically significant operational decision, as even marginal improvements in training effectiveness could have a meaningful impact at scale.

The organization maintains detailed employee-level training records as part of its L&D operations, capturing information on module assignments, completion behavior, time investment, and satisfaction across its workforce. These records are further linked to organizational attributes such as store location, department, and employment classification, providing a foundation for analysis across multiple dimensions of the workforce. The HR department's current challenge is to leverage this data to establish a clear, quantifiable correlation between training activity and revenue performance, helping stakeholders make confident, evidence-based strategic decisions.

## Problem Statement

At present, the HR division lacks a robust, data-driven framework to verify the financial impact of its Learning and Development initiatives. Due to legal and data privacy constraints, the team was unable to obtain direct access to the organization's proprietary records. Therefore, approved and approximated synthetic data is used to analyze the problem. This project addresses a two-fold problem:

1. **Correlation Deficit:** L&D effectiveness is currently evaluated through participation counts, completion scores, and anecdotal manager feedback - measures that capture activity but do not address financial outcomes. As a result, decisions about which programs to fund or expand are made without a clear evidence base linking training investment to business performance. Establishing this link will shift stakeholders from perception-based decisions to measurable, outcome-driven ones.

2. **Optimization Strategy:** Current L&D resource allocation may not be optimally structured to maximize revenue impact. Resources appear distributed relatively evenly across programs, with certain initiatives favored by historical precedent or leadership preference rather than by demonstrated returns. Identifying which training dimensions show the strongest association with revenue will enable stakeholders to reallocate investment toward programs that generate the highest measurable financial return.

## Data

For this project, we worked with two structured datasets: an employee learning dataset drawn from the organization's Learning Management System (LMS) and a store-level revenue dataset used as an analysis variable. Both datasets were synthetically generated to mimic realistic patterns found in real-world organizational data systems, while maintaining the structure and relationships typical of actual records. We estimated the synthetic data at approximately 100,000 LMS records and annual revenue data for 205 stores. The synthetic datasets were shared with the client for review and feedback to ensure they reasonably approximated real-world patterns before analysis proceeded.

### LMS Dataset

The LMS dataset captures individual employee interactions with learning and development modules across the organization. Each record represents a specific employee's engagement with a single training module, providing a granular view of learning activity across the workforce.

Employee identity was established through identity detail columns (e.g., Employee ID and Last Name). Organizational context is provided by Business Unit, District, Location, Department, and Job Code, along with Supervisor Employee ID, Supervisor Name, and Supervisor Email Address, which define each employee's reporting structure. FullTime/PartTime and Is Salaried classifications enabled comparisons across employment and compensation types, while Hire Date served as the basis for calculating tenure.

Training modules were identified by Learning Module Code and Name, with Type and Category distinguishing format (e.g., eLearning vs. instructor-led) and content area (e.g., compliance vs. leadership). Assignment-tracking variables captured the full training lifecycle, including identifiers (Progress Instance, Progress ID), assignment details (Assignment Type), and key dates (Assignment, Due, and Complete). Derived fields such as Past Due and Days Past Due measured timeliness, while Progress Status indicated completion state.

Engagement was evaluated using Estimated Duration and actual Total Time spent, comparing expected versus actual effort. The Satisfied variable captured employee feedback, enabling analysis of training effectiveness and perceived quality.

The compiled list of the LMS columns information can be found in the appendix.

### Revenue Dataset

The revenue dataset captures store-level financial performance at daily observation intervals and serves as the dependent variable for this analysis. Each record represents a single store on a timeline from January 2024 through March 2026, providing a granular view of financial activity across the organization's locations.

Store identity was established using the Store ID field, formatted to match the Location identifier in the LMS dataset, and used as the shared key to merge the two datasets. The Date field records each observation's calendar date, from which the Day of Week was derived, and Is Weekend was constructed to distinguish weekend days from weekdays, enabling analysis of revenue variation across the weekly cycle. The February start date and January end date ensure that holiday-season sales are fully captured, which is important for analyzing retail performance trends.

Core financial performance is captured through Daily Revenue (total sales in USD) and Transactions (total customer visits per store per day). Avg Basket Size, calculated as revenue divided by transactions, reflects the average spend per visit. At the same time, the Promotion Flag indicates whether a promotional campaign was active, helping account for revenue variation driven by marketing rather than operations.

The workforce context is provided by the Number of Employees, averaging around 115 per store, along with two derived productivity metrics: Revenue per Employee and Transactions per Employee. These measures link financial outcomes to staffing levels, offering insight into both financial efficiency and operational throughput. Together, these metrics serve as the primary bridge between financial performance and the workforce-level insights drawn from the LMS data.

The dataset is synthetically generated and calibrated using publicly available benchmarks from the regional grocery industry in the Mid-Atlantic and Northeast United States. It is designed to support analysis rather than represent real performance. Any practical application to inform strategic decisions would require validation against the actual organizational data.

The compiled list of the Revenue column's information can be found in the appendix.

## Methodology

This analysis employed a correlational research design to examine the potential relationship between employee-level L&D activity and store-level revenue performance. It was conducted in four main stages: data preparation and discovery, variable construction, statistical analysis, and interpretation and model evaluation.

### Data Preparation

The primary dataset comprised individual employee training records drawn from the organization's L&D tracking system (Workday), including completion status, time investment, satisfaction responses, on-time performance, and organizational attributes such as business unit, district, department, and additional employee-level fields. These were supplemented by the store-level revenue dataset described above, which was merged with the aggregated LMS records using the shared Location and Store ID identifier.

For legal and data privacy reasons, the team was unable to obtain direct access to the organization's records. As a result, this analysis was conducted on synthetic data generated with AI tools and calibrated to the data fields disclosed by the client. The synthetic datasets were shared with the client for review and feedback to ensure they reasonably approximated real-world patterns before analysis proceeded.

Because the unit of analysis for revenue is the store location, individual employee records were aggregated to the store level, yielding a dataset in which each observation represents a single location with corresponding summary L&D measures and revenue figures. Because the datasets were synthetically generated under controlled parameters, systematic data quality issues, such as missing values and formatting inconsistencies, are minimal. Nonetheless, the team conducted a review for internal consistency, outlier detection, and structural completeness before proceeding with analysis.

### Variable Construction

Independent variables were derived from the LMS dataset and organized into three categories:

- **Participation and Completion:** Store-level training completion rate, proportion of assignments completed on time, average days past due for late or incomplete modules, and exemption rate by module type.
- **Training Intensity:** Time Investment Ratio, calculated as Total Time / Estimated Duration and reflecting actual versus expected effort per module, average number of modules assigned per employee, and proportion of optional versus mandatory training completed.
- **Program Composition:** Distribution of training activity across module types, module categories, departments, and employee classifications within each store.

The dependent variable is store-level revenue performance, represented primarily by Daily Revenue and the derived productivity metrics Revenue per Employee and Transactions per Employee from the revenue dataset, as described in the Data section above.

### Statistical Analysis

The analysis used a combination of Microsoft Excel, Python, and Tableau. Excel handled initial data cleaning, aggregation, and exploratory summaries. Python supported more detailed statistical modeling and visualization. Tableau facilitated data exploration and the creation of clearer, more accessible visualizations for stakeholder presentation.

The analysis took place in two phases. The first phase used correlation analysis to identify which individual L&D variables were significantly associated with revenue performance. The second phase applied multiple modeling approaches - including regression analysis and decision trees - to examine the overall relationship between L&D variables and revenue while accounting for store-level factors that might independently influence performance, such as store size, district, workforce composition, and the Promotion Flag control variable from the revenue dataset. This allowed for a more precise estimate of the incremental contribution of specific training elements. Subgroup analyses were also conducted across departments, employee classifications, and module categories to examine whether the relationship between training and revenue varied by workforce segment or program type.

### Interpretation and Limitations

Findings were interpreted in the context of the organization's strategic L&D goals, and results were translated into actionable recommendations for resource reallocation. Two important limitations should be noted.

First, this analysis establishes correlation rather than causation. Statistically significant associations inform investment prioritization but do not definitively prove that improved training resource allocation will directly drive revenue. External factors - including local market conditions, store tenure, and labor market stability - may independently influence both variables.

Second, because both datasets are synthetically generated, findings should be understood as illustrative of the analytical framework rather than conclusive. This framing applies equally to the results and conclusions that follow: All findings represent the output of a methodologically sound analytical approach applied to synthetic data, and validation against the organization's actual proprietary records would be required before these results are used to inform strategic decisions.

## Results

### EDA Insights

#### Completion & Progress Status

78.30% of records are Completed, 12.20% are In Progress, and 9.50% are Not Started. The roughly 21.70% non-completion rate across 100,000 records is meaningful at scale - for a 23,000-person workforce, that represents a substantial volume of unfinished training that could be masking skill gaps.

Corporate Leadership stands sharply apart with a 91.70% completion rate - nearly 20 points above the lowest group, Regional Leadership (72.00%). This is the widest segmentation gap observed anywhere in the data and may reflect stronger accountability structures at the corporate level. The pattern where leadership-titled departments diverge so significantly is worth flagging to stakeholders.

#### Time Investment & Engagement

About 18.9% of the total modules are past due. Among overdue assignments, delays are severe, with a median of 275 days and a maximum of 814 days. These are not minor overdue but likely represent abandoned training. Leadership modules have the highest past-due rate of 19.70%, while Analytics has the lowest with 17.60%, though the 2-point spread across categories is narrow.

Full-time and part-time employees spend virtually the same median time on training (19 vs 18 minutes). The distributions overlap almost entirely, confirming that module format and category - not employment status - are the primary drivers of time investment. Part-time employees do not appear to rush through modules despite likely having fewer scheduled hours.

The synthetic data reflects a workforce skewed toward newer employees, consistent with typical grocery retail turnover patterns. The median tenure at time of training assignment is just 1.0 year, and 75% of records come from employees with under 2.4 years on the job. The distribution is strongly right-skewed, with very few long-tenured employees, reflecting typical grocery retail turnover patterns and indicating that the training data largely captures early-career engagement.

#### Satisfaction Analysis

The synthetic satisfaction level is very high overall. 89.80% of completed modules are rated positively. While this reflects well on the L&D program design, such a high floor limits the discriminating power of satisfaction across segments. Only about 10% of completed records are dissatisfied, so small absolute differences in satisfaction rates (e.g., 88% vs 91%) still represent a meaningful signal given the dataset scale.

The 1-3 year band is the training sweet spot - highest completion (79.20%) and satisfaction (71.10%) - while brand-new employees (<1yr) underperform slightly, likely still onboarding. The 10+ year group drops sharply to 65.20% completion and 57.60% satisfaction, but this band has only 66 records, making those figures statistically unreliable. A general pattern of peak engagement in the mid- to early tenure period, followed by a gradual decline, is consistent with training fatigue.

#### Store / Location-Level Aggregation

Completion rate and past-due rate are strongly negatively correlated (r = -0.92), confirming they are two sides of the same coin; using both in a revenue model would introduce multicollinearity. Completion and satisfaction are highly correlated (r = 0.83). Average total time has a moderate positive link with completion (r = 0.46), suggesting stores where employees invest more time in training also complete more - a useful leading indicator. Lastly, average tenure time shows only weak correlations with the other KPIs.

## OLS Regression

### Baseline Model (Controls Only)

The controls-only model anchors our incremental attribution framework. Store size (`store_size_sqft`) and headcount (`num_employees`) reflect structural capacity, while `promotion_rate` proxies for external revenue levers. Any R² improvement observed when L&D features are added in Section 4 represents variance that store characteristics alone cannot explain - i.e., the identifiable workforce-development signal.

The incremental R² over the baseline indicates how much additional revenue-per-employee variance is explained by L&D training profiles after controlling for store size and promotional activity. In practice, this increment was 7.0 percentage points (baseline R² = 0.027, full model R² = 0.097), but it did not hold out-of-sample, indicating overfitting rather than a real signal. Positive coefficients in this chart reflect directional associations only - none reached statistical significance. Notably, `past_due_rate` carries a negative coefficient as expected - but the effect is not significant - while engagement-oriented categories like `pct_customer_exp`, `pct_sales`, and `pct_leadership` show positive directional associations that likewise do not reach significance. Multicollinearity among the `pct_*` category features inflates standard errors, motivating the regularized models in Sections 5 and 6.

### Ridge Regression (Handles Multicollinearity)

Ridge regression shrinks correlated predictors toward each other rather than eliminating any, which is appropriate given the near-linear dependencies among the `pct_*` category features (they must sum to ~1). Comparing Ridge CV R² to the full OLS R² reveals whether OLS was overfitting the 240-row sample. If Ridge CV R² is materially lower than OLS R², the OLS estimates were optimistic. The sign pattern of Ridge coefficients provides a more stable ranking of directional effects than OLS t-statistics when multicollinearity is present.

### Lasso Regression (Feature Selection)

Lasso applies L1 regularization, which produces exact zeros and thus acts as an embedded feature selector. In this analysis, Lasso eliminated all 22 L&D features, retaining zero training-related predictors — the strongest possible signal that no L&D variable adds explanatory power once store-level controls are accounted for. The expectation was that if engagement-related variables (`completion_rate`, `satisfaction_rate`, `pct_customer_exp`, `pct_leadership`) survived alongside workforce composition (`pct_fulltime`, `avg_tenure`), it would strengthen the case that L&D program quality contributes to productivity. None did. Features eliminated by Lasso can be safely deprioritized in subsequent analysis.

### Decision Tree Regressor

The root split of the decision tree identifies the single variable that most cleanly partitions stores by revenue per employee. In this analysis, the first split involves a structural control variable, confirming that store capacity is the dominant driver. A notable gap between train R² and cross-validation R² confirms the tree is overfitting at depth 4 — the model memorized the training sample rather than learning generalizable patterns — which motivates the ensemble approach in Section 8.

### Random Forest Regressor

Random Forest aggregates 200 trees, substantially reducing the variance of single-tree estimates. Permutation importance is more reliable than MDI (mean decrease impurity) for mixed-scale features because it measures actual hold-out predictive degradation. If L&D features - particularly `completion_rate`, `avg_tenure`, or `pct_customer_exp` - appear in the top 10 permutation importances alongside structural controls, it provides non-parametric evidence that training profiles carry real predictive information beyond store size and promotional activity.

## Model Comparison

This analysis examined whether stores whose employees complete more training, finish it on time, and report higher satisfaction, etc also generate more revenue per employee. Six different statistical models were run, from simple regression to random forest, all controlling for factors outside HR's control, such as store size, headcount, and promotional activity. The outcome variable was revenue per employee per day, the most direct measure of how workforce performance translates to financial output.

*We want to point out that we did not get confirmation from the client about the revenue dataset until Thursday, April 16. As a result, most of the findings below are based on preliminary models built on our assumptions about the expected data structure. The team will keep refining and retraining the models next week to match the client's finalized data specifications.*

> No statistically significant relationship was found between any L&D training metric and revenue per employee across the 240 stores analyzed.

Some of our findings are:

- The correlation between completion rate and revenue per employee was r = –0.07 (p = 0.30), which is statistically indistinguishable from zero
- Satisfaction rate, past-due rate, training intensity, and time invested in training all showed similarly negligible correlations (all p > 0.15)
- Stores with top-quartile training completion rates averaged $105.46 revenue per employee per day. Stores with bottom-quartile completion rates averaged $107.17 - so it's essentially identical to top-quartile training, a difference of only $1.71. This is a great opportunity for us to revisit the synthetic data generation to make sure there is a clear distinction between the top-performing stores and the rest.

## What the Models Found

**Store characteristics explain very little revenue variation:** Even combining store size, headcount, and promotional activity, the baseline model explained only 2.7% of the variation in revenue per employee across stores. Adding all 22 L&D variables raised this to 9.7% - but when tested on stores the model had never seen, performance was actually worse than simply guessing the average. This pattern (called overfitting) indicates the model found noise rather than real signal.

**The only significant predictor was promotions:** Across all models, promotional activity (whether a store ran a discount campaign on a given day) was the single variable that consistently and significantly predicted revenue. This is expected - and confirms that the models are working correctly. It also highlights that short-term revenue at the store level is primarily driven by demand-side factors (marketing, foot traffic, local competition) rather than workforce factors.

**Lasso kept no L&D variables:** The Lasso model is designed to automatically discard variables that don't pull their weight. It eliminated all 22 L&D features, retaining zero training-related predictors in the final model. This is the strongest statistical signal that, within this dataset, training metrics do not add explanatory power once store-level controls are accounted for.

## Other Findings

The following reflects the directional associations observed in the full OLS model's point estimates. **None of these associations are statistically significant** — all p > 0.05, all were eliminated by Lasso regularization, and cross-validated models confirm they do not hold out-of-sample. They are documented here as theoretically expected directions — consistent with what the L&D literature would predict — and as a guide for future testing once better outcome variables or longer time horizons are available.

L&D variables with positive directional associations in OLS point estimates (not statistically significant):

- **`completion_rate`** - stores where employees complete assigned training at higher rates show a positive directional association with workforce productivity, though the effect is too small and unstable to be statistically meaningful in this dataset. This is one of the most actionable levers to monitor in future analysis, as completion is directly observable and improvable through scheduling and accountability structures.
- **`satisfaction_rate`** - learner satisfaction shows a positive directional association with outcomes, suggesting training quality and relevance may matter beyond mere compliance - but the signal is not statistically distinguishable from noise here.
- **`pct_customer_exp`** and **`pct_sales`** - stores allocating more of their training mix to customer-facing and sales skill-building show a positive directional association with revenue per employee, consistent with the expectation that content - not just volume - matters for front-line productivity. Not statistically significant.
- **`pct_leadership`** - leadership development shows a positive directional association with store performance, likely because managers shape service culture, scheduling, and team motivation. Not statistically significant.
- **`avg_tenure`** - experienced workforces show a positive directional association with revenue per training hour invested, reinforcing the value of retention alongside learning. Not statistically significant.
- **`training_intensity`** - stores where employees complete more assignments per person show a positive directional association with productivity, up to a point. Not statistically significant.

L&D variables with neutral or negative directional associations in OLS point estimates:

- **`past_due_rate`** - shows the most consistent negative directional association across models. Stores with higher rates of overdue training show lower revenue per employee in OLS point estimates, though this does not reach significance. This may reflect management attention deficits: if compliance deadlines are missed, operational discipline broadly may be weaker.
- **`pct_compliance`** and **`pct_safety`** - near-zero or slightly negative directional associations with revenue, which is expected. These are necessary but not sufficient for performance - they reflect regulatory minimums rather than capability development.
- **`pct_required`** - a high share of required (vs. elective) training shows a negative directional association, suggesting a reactive L&D environment with limited discretionary development investment. Elective training, driven by employee initiative, tends to be more strongly applied.

## Why This Might Be Happening

Several structural reasons explain why L&D metrics may not appear correlated with daily store revenue in this dataset:

1. **Revenue is driven by factors training can't control.** Store-level daily revenue is heavily influenced by store size, local competition, population density, and promotional cadence - none of which training can move. Once those factors are held constant, the remaining revenue variance is small, leaving little room for training to explain.

2. **The observation window may be too short.** Training affects skill development gradually. The benefits of a compliance course completed in Q1 2024 may not appear in customer satisfaction or transaction throughput until much later. A 2-year window may not be long enough to detect a lagged effect.

3. **Completion rate may be the wrong measure of training quality.** Completing a module is a binary event - it tells us nothing about whether learning actually occurred. Behavior change on the floor, not module completion, is what drives revenue. The dataset captures activity, not impact.

## What we intend to do next:

These findings point to three concrete next steps:

1. **Refine our synthetic data.** We aim for our findings to be as close to reality as possible. To achieve this, we are refining both datasets to ensure that no statistically significant relationships are missed.

2. **Reframe the outcome variable.** Rather than daily revenue, consider outcomes that training more directly influences:
   - Customer satisfaction scores (NPS or survey-based)
   - Employee retention and turnover rates
   - Shrink/loss rates (for safety and compliance training)
   - Department-level gross margin (not whole-store revenue)

3. **Analyze at the employee or department level, not the store level.** If individual-level performance data exists (e.g., department comps, individual productivity metrics), linking those to individual training records would be far more powerful than the store-level approach used here.

4. **Build a longer time series and test lagged effects.** Run the same analysis with a 6–12 month lag between training completion and the revenue measurement window. If training has a delayed payoff, a contemporaneous correlation will always appear weak.

---

## Appendix

### LMS columns information

| Variable Name | Category | Description |
|---|---|---|
| Employee ID | Identity | Unique identifier for each employee across all training records |
| First Name | Identity | Employee first name |
| Last Name | Identity | Employee last name |
| Full Name | Identity | Concatenated first and last name |
| Email Address | Identity | Employee work email address |
| Hire Date | Workforce | Date the employee was hired; used to derive tenure at time of training assignment |
| Business Unit | Organizational | High-level division the employee belongs to (e.g. Store Operations, Corporate Services) |
| District | Organizational | Regional grouping of stores (e.g. East_District_01); links stores to a shared management structure |
| Location | Organizational | Store or site identifier (e.g. Store_001, HQ_001); matches Store_ID in the revenue dataset and serves as the join key |
| Department | Organizational | Functional department within the store or business unit (e.g. Produce, Store Management, Compliance) |
| Job Code | Organizational | Standardized role code classifying the employee's position level |
| Supervisor Employee ID | Organizational | Employee ID of the direct supervisor; used to map reporting structure |
| Supervisor Name | Organizational | Full name of the employee's direct supervisor |
| Supervisor Email Address | Organizational | Work email of the direct supervisor |
| FullTimePartTime | Workforce | Employment classification: Full Time or Part Time |
| Is Salaried | Workforce | Indicates whether the employee is on a salaried (Yes) or hourly (No) pay structure |
| Learning Module Code | Module | Unique code identifying the training module (e.g. CMP001, OPS007) |
| Learning Module Name | Module | Descriptive title of the training module |
| Learning Module Type | Module | Delivery format of the module: eLearning, Instructor-Led, Assessment, or Microlearning |
| Learning Module Category | Module | Content area the module belongs to: Compliance, Operations, Safety, Leadership, Sales, Customer Experience, Technology, Human Resources, or Analytics |
| Estimated Duration | Module | Expected time to complete the module, in minutes, as set by the L&D team |
| Progress Instance | Assignment Tracking | Sequential instance number for repeated assignments of the same module to the same employee |
| Progress ID | Assignment Tracking | Unique identifier for each individual training record (one row = one employee × one module instance) |
| Assignment Type | Assignment Tracking | How the training was assigned: Required, Elective, Recommended, or Manager Assigned |
| Assignment Date | Assignment Tracking | Date the training module was assigned to the employee |
| Due Date | Assignment Tracking | Deadline by which the module must be completed |
| Complete Date | Assignment Tracking | Date the employee marked the module as complete; null if not yet completed |
| Progress Status | Assignment Tracking | Current completion state: Completed, In Progress, or Not Started |
| Past Due | Assignment Tracking (Derived) | Indicates whether the module was completed or remains incomplete past the Due Date: Yes or No |
| Days Past Due | Assignment Tracking (Derived) | Number of days the assignment is overdue; 0 for on-time or incomplete records not yet past the deadline |
| Total Time | Engagement | Actual time the employee spent on the module in minutes, as logged by the LMS |
| Satisfied | Engagement | Post-completion satisfaction rating reported by the employee: Yes (satisfied) or No (not satisfied) |

### Revenue columns information

| Variable Name | Category | Description |
|---|---|---|
| Store_ID | Identity | Unique identifier for each store (e.g. Store_001); matches Location in the LMS dataset and serves as the join key |
| Date | Time | Calendar date of the observation (daily grain; ranges Jan 1 2024 – Mar 30 2026) |
| Day_of_Week | Time (Derived) | Day of the week derived from Date at runtime (e.g. Monday, Tuesday) |
| Is_Weekend | Time (Derived) | Boolean flag indicating whether the day falls on a Saturday or Sunday |
| Is_Holiday | Time | Binary flag (0/1) indicating whether the date is a federal or major retail holiday (~1.7% of records) |
| Daily_Revenue | Financial | Total store revenue in USD for that calendar day |
| Gross_Sales | Financial | Total sales before returns, adjustments, or discounts are applied |
| Net_Revenue | Financial | Revenue after returns and post-sale adjustments; typically slightly below Daily_Revenue |
| Profit | Financial | Absolute profit in USD for the day (Net Revenue minus cost of goods and operating expenses) |
| Revenue_Growth_Pct | Financial (Derived) | Day-over-day percentage change in Daily_Revenue for the same store |
| Profit_Margin_Pct | Financial (Derived) | Profit divided by Daily_Revenue; expressed as a decimal (e.g. 0.13 = 13%) |
| Transactions | Customer Activity | Total number of individual customer transactions (i.e. purchases) recorded at the store that day |
| Avg_Basket_Size | Customer Activity (Derived) | Average spend per transaction (Daily_Revenue ÷ Transactions) |
| Num_Employees | Workforce | Total number of employees rostered at the store; constant per store across the dataset |
| Revenue_per_Employee | Productivity (Derived) | Revenue generated per employee per day (Daily_Revenue ÷ Num_Employees); primary outcome variable for L&D analysis |
| Transactions_per_Employee | Productivity (Derived) | Transactions handled per employee per day (Transactions ÷ Num_Employees); measures operational throughput |
| Store_Size_SqFt | Store Characteristics | Physical footprint of the store in square feet; constant per store; ranges from ~2,888 to ~20,779 sq ft |
| Sales_per_SqFt | Store Characteristics (Derived) | Daily_Revenue divided by Store_Size_SqFt; normalizes revenue for store size comparison |
| Promotion_Flag | Marketing | Binary flag (0/1) indicating whether a promotional or discount campaign was active at the store that day (~20% of records) |
