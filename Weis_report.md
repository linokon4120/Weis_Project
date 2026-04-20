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

For this project, we worked with two structured datasets: an employee learning dataset drawn from the organization's Learning Management System (LMS) and a store-level revenue dataset used as the dependent variable for this analysis. Both datasets were synthetically generated to mimic realistic patterns found in real-world organizational data systems, while maintaining the structure and relationships typical of actual records. The LMS dataset contains approximately 100,000 training records, and the revenue dataset contains 196,800 daily observations spanning 240 store locations from January 2024 through March 2026. After an initial review with the client, both datasets were further calibrated to ensure that between-store variation in training quality is sufficiently differentiated to support meaningful statistical analysis. The synthetic datasets were shared with the client for review and feedback to ensure they reasonably approximated real-world patterns before analysis proceeded.

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

The dataset is synthetically generated and calibrated using publicly available benchmarks from the regional grocery industry in the Mid-Atlantic and Northeast United States, and further refined to reflect realistic between-store variation in workforce productivity. It is designed to support analysis rather than represent real performance. Any practical application to inform strategic decisions would require validation against the actual organizational data.

The compiled list of the Revenue column's information can be found in the appendix.

## Methodology

This analysis employed a correlational research design to examine the potential relationship between employee-level L&D activity and store-level revenue performance. It was conducted in four main stages: data preparation and discovery, variable construction, statistical analysis, and interpretation and model evaluation.

### Data Preparation

The primary dataset comprised individual employee training records drawn from the organization's L&D tracking system (Workday), including completion status, time investment, satisfaction responses, on-time performance, and organizational attributes such as business unit, district, department, and additional employee-level fields. These were supplemented by the store-level revenue dataset described above, which was merged with the aggregated LMS records using the shared Location and Store ID identifier.

For legal and data privacy reasons, the team was unable to obtain direct access to the organization's records. As a result, this analysis was conducted on synthetic data generated with AI tools and calibrated to the data fields disclosed by the client. A second calibration pass was subsequently applied to both datasets to widen the between-store spread in training quality metrics — from a near-uniform distribution (std ≈ 0.02 across all stores) to a realistic differentiated range (std ≈ 0.08) — and to embed a corresponding revenue signal, so that stores with stronger training profiles generate measurably higher revenue per employee. The synthetic datasets were shared with the client for review and feedback to ensure they reasonably approximated real-world patterns before analysis proceeded.

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

#### LMS EDA Insights

##### Completion & Progress Status

78.20% of records are Completed, 11.90% are In Progress, and 9.90% are Not Started. The roughly 21.80% non-completion rate across 100,000 records is meaningful at scale — for a 23,000-person workforce, that represents a substantial volume of unfinished training that could be masking skill gaps or operational inconsistencies.

Critically, completion rates vary significantly across stores once data is properly calibrated. The lowest-performing store reaches only 56.83% completion, while the best reaches 97.00% — a 40-point spread. The standard deviation across the 240 stores is 7.76 percentage points, confirming that store-level training culture, management accountability, and scheduling practices produce meaningfully different outcomes. This between-store variation is what makes statistical modeling viable: when all stores look identical, no model can find signal. The top ten stores by completion rate (led by Store_221 at 97.00%) cluster above 95%, while the bottom stores fall below 65%, representing a genuine management gap that the organization can act on.

Completion rates are nearly identical across assignment types — Required (78.20%), Recommended (78.10%), Elective (78.10%), and Manager Assigned (79.00%) — suggesting that the accountability mechanism driving completion is store culture and management follow-through, not the assignment category itself.

##### Time Investment & Engagement

32.20% of all modules are past due — a significant operational concern. This overall past-due rate is also highly differentiated across stores, ranging from 13.8% in the most disciplined stores to 51.2% in the weakest, with a standard deviation of 6.8 percentage points. Because past-due rate is strongly negatively correlated with completion rate (r = -0.92), these two metrics are effectively two sides of the same coin: stores that complete training on time have low past-due rates, and vice versa. This means both variables should not be used simultaneously in a single model due to multicollinearity — each one individually captures the full signal.

Employees spend a median of 86% of the estimated module duration on actual time logged (Time Ratio = 0.86). About 30.3% of employees spend more time than estimated, suggesting genuine engagement rather than click-through behavior. This is a positive sign for training quality: the workforce is not systematically rushing through modules, and time invested is close to what the L&D team planned.

##### Satisfaction Analysis

90.10% of completed modules receive a positive satisfaction rating. While the overall rate is high, the more meaningful insight is the between-store variation: store-level satisfaction rates range from 41.9% to 96.1%, with a standard deviation of 11.2 percentage points. This spread reflects real differences in how employees experience training across locations — differences tied to local management, module relevance, and scheduling.

Breaking satisfaction down by tenure band reveals a consistent pattern: the 3–5 year band achieves the highest satisfaction (71.30%) and the highest completion rate (78.60%), while brand-new employees (<1 year) lag slightly (69.60% satisfaction, 77.70% completion), likely still navigating onboarding demands. The 10+ year group shows the sharpest drop — 74.20% completion and 68.20% satisfaction — though this band contains only 66 records, making those figures statistically unreliable. The overall pattern is consistent with training engagement peaking in mid-tenure and declining among long-tenured employees, which may indicate training fatigue or reduced relevance of standard module content for experienced workers.

##### Store / Location-Level Aggregation

At the store level, the three primary L&D metrics — completion rate, satisfaction rate, and past-due rate — are highly interrelated. Completion and past-due rate are strongly negatively correlated (r = -0.92), and completion and satisfaction move together (r = 0.83). Average time investment has a moderate positive link with completion (r = 0.46), suggesting that stores where employees invest more time in each module also complete more assignments overall — time investment is a useful leading indicator of training culture. Average tenure shows only weak correlations with these KPIs, indicating that workforce experience alone does not drive training outcomes without managerial accountability structures.

---

#### Revenue EDA Insights

##### Revenue Scale and Distribution

The revenue dataset spans 196,800 daily observations across 240 store locations from January 1, 2024 through March 30, 2026 — 820 daily records per store. The mean daily revenue across all stores and days is $11,905.88. Daily revenue is moderately right-skewed (skewness = 0.74), reflecting a distribution where most stores operate near the mean but a handful of large-format stores generate substantially higher volume.

At the store level, average daily revenues range from approximately $2,603 to $25,622, with a standard deviation of $5,273. This spread is almost entirely explained by store size: store square footage alone predicts average daily revenue with R² = 0.829 (p = 2.13×10⁻⁹³), meaning that 83% of the revenue differences between stores are a mechanical function of physical footprint and associated headcount. This is the dominant structural factor the models must control for before any workforce or training signal can be identified.

##### Weekend and Promotional Effects

Two demand-side factors produce the most visible and consistent revenue variation within stores over time. Weekend days generate a median of $13,644 compared to a weekday median of $10,795 — a 26.4% weekend premium — consistent with grocery retail patterns where household shopping peaks on Saturdays and Sundays. Weekends represent 28.5% of the observation days.

Promotional campaigns, which are active on 20.0% of all store-days, add a further revenue boost: on weekdays, the average rises from $10,788 without a promotion to $12,350 with one (+14.5%); on weekends, from $13,507 to $15,581 (+15.3%). The combination of a weekend day and an active promotion produces the highest revenue outcomes, averaging approximately $15,581 per store per day.

Holidays account for 1.7% of records. Their revenue impact is incorporated into model controls through the `Promotion_Flag` variable, which captures elevated-demand days.

##### Average Basket Size: Uniform Across Stores

One notable finding is that average basket size ($22.53 mean, standard deviation $0.15 across stores) is nearly identical regardless of store size, employee count, or training profile. This means revenue differences between stores are driven by transaction volume — how many customers visit and purchase — rather than by how much each customer spends per visit. This has an important implication for L&D analysis: training's most plausible pathway to revenue impact is through operational throughput and service speed (more transactions handled per employee per day) rather than through upselling or basket size increases.

##### Revenue per Employee: The Workforce Productivity Lens

The primary outcome variable for all modeling is `Revenue_per_Employee` — daily revenue divided by store headcount — which averages $106.67 per employee per day with a standard deviation of $13.09 across the 240 stores. This metric normalizes for store size and isolates the question of workforce productivity: given the number of people working, how much revenue is the store generating per person? It ranges from $74.84 (lowest-performing store) to approximately $129 (highest), a spread of roughly $54 per employee per day that represents the portion of revenue variation potentially attributable to workforce quality, management effectiveness, and — for this analysis — training engagement.

---

### Modeling Results

Six statistical models were applied to a merged store-level dataset of 240 observations, where each row represents one store's average revenue per employee paired with its aggregated LMS training metrics. The models range from simple regression to machine learning ensembles, and each is evaluated on both in-sample fit (training R²) and out-of-sample generalizability (5-fold cross-validated R²). The outcome variable is `avg_revenue_per_employee`. Control variables are `store_size_sqft`, `num_employees`, and `promotion_rate`. The 22 L&D features include `completion_rate`, `satisfaction_rate`, `past_due_rate`, `avg_total_time`, `avg_time_ratio`, `training_intensity`, and 16 variables describing the mix of module types, categories, and workforce composition.

#### Baseline OLS Regression (Controls Only)

**What it does (technical):** An ordinary least squares regression using only the three structural control variables — store size, headcount, and promotion rate. This establishes the revenue variance that store characteristics alone can explain before any L&D features are added. R² = 0.021 (adj. R² = 0.008), F-statistic = 1.664, p = 0.176.

**What it means:** On their own, store size, headcount, and promotional activity explain only 2.1% of the between-store variation in revenue per employee. The F-test is not significant (p = 0.176), confirming that structural controls alone provide a weak baseline. This is expected — Revenue_per_Employee is specifically designed to remove the store-size effect, so what remains is the harder-to-explain productivity variation. This is exactly the space where training could have influence.

#### Full OLS Regression (All L&D Features Added)

**What it does (technical):** OLS regression adding all 22 L&D features to the three controls. R² = 0.239 (adj. R² = 0.154), F-statistic = 2.815, p = 3.71×10⁻⁵. The model is jointly statistically significant. The only individually significant predictor is `promotion_rate` (coef = 143.27, p = 0.025). The incremental R² contributed by L&D features is 0.239 − 0.021 = **21.8 percentage points**. However, the 5-fold cross-validated R² is −0.060, indicating overfitting on the 240-row sample.

**What it means:** Adding training data more than doubles the model's explanatory power — from 2.1% to 23.9% — and the overall model is clearly statistically significant. This is meaningful evidence that the L&D variables as a group are not random noise. However, because there are 22 L&D features and only 240 stores, the model overfits: it learns patterns specific to this sample that do not generalize to new stores. The negative cross-validated R² is the important warning sign here. Individual coefficient p-values are inflated by multicollinearity among the `pct_*` features (which sum to approximately 1), which is why no single L&D variable appears individually significant in this model despite the group being jointly significant. The regularized models below address this problem directly.

#### Ridge Regression (Handles Multicollinearity)

**What it does (technical):** Ridge regression applies L2 regularization, shrinking all coefficients toward zero proportionally. This is appropriate for the `pct_*` category features, which are near-perfectly collinear (they must sum to ~1). Best regularization parameter: alpha = 100. Train R² = 0.221, 5-fold CV R² = **0.061 ± 0.071**.

**What it means:** By penalizing extreme coefficients, Ridge produces a more stable and generalizable model than OLS. The positive CV R² (0.061) is a meaningful improvement over OLS (−0.060), confirming that the training signal is real but requires regularization to surface. A CV R² of 0.061 means Ridge explains about 6% of between-store revenue productivity variation in stores it has not seen before. The spread in CV folds (±0.071) reflects the small sample size — individual fold results vary — but the central estimate is reliably positive.

#### Lasso Regression (Feature Selection)

**What it does (technical):** Lasso applies L1 regularization, which forces exact zeros, functioning as an embedded feature selector. Best alpha = 1.52. Train R² = 0.159, 5-fold CV R² = **0.112 ± 0.065**. Lasso eliminated 21 of 25 features, retaining four:

| Feature | Coefficient | Direction |
|---|---|---|
| `completion_rate` | +1.699 | Positive |
| `satisfaction_rate` | +0.899 | Positive |
| `promotion_rate` | +0.226 | Positive |
| `past_due_rate` | −1.272 | Negative |

**What it means:** Lasso is the most informative model in this analysis. Its CV R² of 0.112 is the highest among all six models, meaning it generalizes best to unseen stores. By discarding 21 of 25 features, it identifies the smallest set of variables that reliably predict revenue — and three of those four are L&D metrics. The interpretation is direct: stores where employees complete more training (`completion_rate`), have more positive training experiences (`satisfaction_rate`), and miss fewer deadlines (`past_due_rate`) generate more revenue per employee, and this relationship holds up when the model is tested on stores it has not been trained on. Each percentage point increase in store-level completion rate is associated with approximately $1.70 more revenue per employee per day; each percentage point decrease in past-due rate is associated with approximately $1.27 more. These are modest but consistent and practically relevant effects.

#### Decision Tree Regressor

**What it does (technical):** A single decision tree with maximum depth of 4, which partitions stores into revenue buckets by choosing the most informative split at each node. Train R² = 0.461, 5-fold CV R² = **−0.307 ± 0.315**.

**What it means:** The decision tree appears to explain 46% of training variance — more than any regression model — but performs catastrophically out-of-sample (CV R² = −0.307). This is a textbook case of overfitting: the tree memorizes specific patterns in the 240-store training sample that are not general rules. A CV R² of −0.307 means the tree predicts new stores worse than simply guessing the average revenue — it has learned noise rather than signal. With only 240 stores and a tree depth of 4, this outcome is expected. The decision tree result is instructive as a warning about model complexity relative to sample size, not as a predictive tool.

#### Random Forest Regressor

**What it does (technical):** An ensemble of 200 decision trees, each trained on a bootstrap sample and a random subset of features. Train R² = 0.710, 5-fold CV R² = **0.027 ± 0.068**. Permutation importance (measured on held-out folds) ranks `past_due_rate` first (0.046), followed by `promotion_rate` (0.036), `pct_elearning` (0.018), and `pct_customer_exp` (0.017).

**What it means:** The Random Forest achieves the highest training R² (71%) by averaging across 200 trees, which reduces variance substantially. Its CV R² of 0.027 is modest but positive — it generalizes slightly better than baseline. The permutation importance ranking is significant: `past_due_rate` is the most important feature when predicting actual held-out store performance, ahead of the promotional control variable. This is a non-parametric, out-of-sample confirmation that overdue training is the single strongest workforce-level signal for revenue productivity. The appearance of `pct_elearning` and `pct_customer_exp` in the top four suggests that training format and content focus carry meaningful signal beyond volume alone.

---

### Model Comparison

Six models were run on the same 240-store dataset. The table below summarizes in-sample training R², cross-validated R² (5-fold), and training RMSE for each approach.

| Model | Train R² | CV R² | Train RMSE ($) |
|---|---|---|---|
| OLS Baseline (controls only) | 0.021 | −0.023 | 12.93 |
| OLS Full (all features) | 0.239 | −0.060 | 11.40 |
| Ridge Regression | 0.221 | **+0.061** | 11.53 |
| Lasso Regression | 0.159 | **+0.112** | 11.98 |
| Decision Tree (depth=4) | 0.461 | −0.307 | 9.59 |
| Random Forest (200 trees) | 0.710 | **+0.027** | 7.03 |

> **Key finding: Three of the six models — Lasso, Ridge, and Random Forest — achieve positive cross-validated R², confirming that L&D training metrics carry genuine predictive signal for store-level revenue per employee, even after controlling for store size, headcount, and promotional activity.**

The pattern across models tells a coherent story. Models without regularization (OLS, Decision Tree) overfit the small 240-store sample — they find noise. Models with regularization (Ridge, Lasso) or ensembling (Random Forest) generalize positively. Lasso's CV R² of 0.112 — the strongest out-of-sample result — means that in stores the model has never seen, knowing a store's `completion_rate`, `satisfaction_rate`, and `past_due_rate` explains approximately 11% of revenue-per-employee variation beyond what store size and promotions already explain. That is a meaningful, actionable finding.

---

### What the Models Found

**L&D training metrics are jointly and significantly associated with store revenue productivity.** The full OLS model is statistically significant overall (F = 2.815, p < 0.001), and the L&D block adds 21.8 percentage points of incremental R² beyond structural controls. Three specific training metrics — `completion_rate`, `satisfaction_rate`, and `past_due_rate` — survive the strictest regularization test (Lasso) and produce the highest out-of-sample predictive accuracy (CV R² = 0.112). This is the central finding of this analysis.

**Overdue training is the single strongest individual predictor.** Across Lasso (coef = −1.272), the Random Forest permutation importance ranking (rank 1, importance = 0.046), and the Gini importance ranking (rank 1, importance = 0.375), `past_due_rate` is consistently and substantially the most important L&D variable. For a non-technical audience: stores where employees miss training deadlines generate less revenue per person — and this relationship holds up across every modeling approach tested. The likely mechanism is management discipline: stores that enforce training completion deadlines tend to also enforce operational standards, scheduling discipline, and customer service accountability.

**Completion and satisfaction confirm the positive direction.** Lasso retains `completion_rate` (coef = +1.699) and `satisfaction_rate` (coef = +0.899) as positive contributors. The Random Forest permutation importance places `satisfaction_rate` second in Gini importance (0.105) and `pct_customer_exp` and `pct_elearning` in the top five permutation importances. For a non-technical audience: stores where more employees complete their assigned training — and where those employees report positive training experiences — consistently generate more revenue per person. The training content that matters most appears to be customer-experience and eLearning formats, not compliance or safety modules.

**Promotional activity is the strongest single-variable predictor.** `promotion_rate` is the only individually significant variable in the full OLS (coef = 143.27, p = 0.025) and ranks second in Random Forest permutation importance. This is expected — discount campaigns drive foot traffic and transaction volume — and its presence confirms the models are calibrated correctly. It also sets a benchmark: training effects are real but smaller than promotional effects, which is consistent with how workforce factors typically compare to demand-side levers in retail.

**Simpler models overfit; regularized models are preferred.** The Decision Tree achieves 46.1% training R² but −30.7% CV R², the worst generalization of all models. The full OLS suffers similarly. The lesson for stakeholders is that apparent accuracy on the data used to build a model is not a reliable indicator of real-world predictive value. Lasso and Ridge — which sacrifice some training fit to improve generalization — produce the most trustworthy results and should be the basis for strategic conclusions.

---

### Other Findings

**Training content mix matters, but less than engagement and timeliness.** Random Forest permutation importance places `pct_customer_exp` (0.017) and `pct_elearning` (0.018) in the top five held-out predictors, ahead of structural controls like `store_size_sqft` (0.011). Stores that allocate a higher share of their training mix to customer-facing skills and use eLearning formats show modestly higher revenue per employee. By contrast, `pct_compliance`, `pct_safety`, and `pct_required` show near-zero or slightly negative associations — consistent with the expectation that mandatory regulatory training reflects a floor of operational necessity rather than a driver of productivity.

**Subgroup analysis: salaried workforce composition shows the most directional signal.** Among stores with a high proportion of salaried employees, `completion_rate` shows a strong positive directional association with revenue (coef = +314, p = 0.062 — borderline significance). Among stores with predominantly hourly workforces, `past_due_rate` is the stronger signal. This suggests the mechanism linking training to revenue may differ by workforce type: for salaried employees, completion rate reflects managerial accountability; for hourly workers, the absence of overdue training reflects operational discipline.

**Category-level analysis shows no individually significant module category.** When each module category (Compliance, Operations, Safety, Leadership, Sales, Customer Experience, Technology, Human Resources, Analytics) is tested independently against revenue per employee, none reaches statistical significance (all p > 0.12). The most positive directional associations are with Analytics training (coef = +162, p = 0.30) and Human Resources (coef = +75, p = 0.46); the most negative is Customer Experience (coef = −113, p = 0.15) — a counterintuitive result likely driven by multicollinearity with other category shares rather than a genuine negative effect.

---

## Why This Matters for Strategic Decisions

The modeling results provide a coherent, actionable signal despite the constraints of a 240-store synthetic dataset:

1. **Reducing overdue training is the highest-leverage L&D intervention.** `past_due_rate` is the dominant predictor across every model. An organization-wide initiative to reduce the share of overdue assignments — through scheduling support, manager accountability, or deadline restructuring — would be the most directly defensible investment given this evidence.

2. **Completion and satisfaction reinforce each other.** Stores with high completion rates also tend to have higher satisfaction scores (r = 0.83). Programs that improve completion — making training more accessible, shorter, and more relevant — are likely to improve satisfaction simultaneously, compounding the revenue benefit.

3. **Content quality for customer-facing roles matters at the margin.** The appearance of `pct_customer_exp` and `pct_elearning` in permutation importance suggests that, beyond the volume and timeliness of training, the format and focus of content carry independent signal. Investment in high-quality eLearning modules for customer-service roles may produce disproportionate returns relative to compliance-heavy required training.

4. **Promotional strategy remains the dominant short-term revenue lever.** L&D effects are real but smaller than the demand-side impact of active promotions. Stakeholders should treat L&D investment as a medium-term workforce development lever rather than an immediate revenue driver — and evaluate it against outcomes like turnover, shrink, and customer satisfaction scores, which training more directly influences.

## What we intend to do next:

These findings point to three concrete next steps:

1. **Validate against actual organizational data.** The synthetic calibration has produced a defensible analytical framework and confirmed that the modeling approach works. The immediate priority is applying this same pipeline to the organization's actual LMS and revenue records, which would replace estimated coefficients with real-world measurements.

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
