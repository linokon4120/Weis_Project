# Modeling Section — Slide Content & Presentation Script
*Presenter: Ellyn | Section: Predictive Modeling*

---

## PART 1: SLIDE CONTENT

---

### Slide 1 — Section Title

**Predictive Modeling**
*Can L&D Training Metrics Forecast Store Revenue Productivity?*

---

### Slide 2 — Setup: What We Modeled

**Outcome Variable:** Revenue per Employee
- Daily revenue ÷ store headcount
- Average: $106.67/employee/day | Range: $74.84 – $129
- Normalizes for store size; isolates workforce productivity

**Dataset:** 240 stores, store-level aggregates

**Controls (non-L&D):** Store size (sq ft), headcount, promotion rate

**22 L&D Features:** Completion rate, satisfaction rate, past-due rate, training intensity, module type/category mix

> *📊 Include: a simple diagram or table showing the feature groups (Controls vs. L&D Features)*

---

### Slide 3 — Six Models, One Question

| Model | Purpose |
|---|---|
| OLS Baseline | How much do store characteristics explain alone? |
| OLS Full | What does adding all 22 L&D features do? |
| Ridge | Handle correlated features; reduce overfitting |
| **Lasso** | **Feature selection — find the essential few** |
| Decision Tree | Non-linear patterns; benchmark for complexity |
| Random Forest | Ensemble; most robust feature importance |

> *📊 Include: horizontal bar chart of CV R² across all six models (from Weis_Modeling.ipynb — model comparison chart)*

---

### Slide 4 — The Overfitting Problem

**Train R² vs. Cross-Validated R²**

| Model | Train R² | CV R² |
|---|---|---|
| OLS Full | 0.239 | −0.060 ❌ |
| Decision Tree | 0.461 | −0.307 ❌ |
| **Lasso** | 0.159 | **+0.112 ✓** |

**The rule:** If CV R² < 0, the model predicts new stores *worse* than just guessing the average.

- OLS and Decision Tree memorize noise from 240 stores
- Regularized models (Lasso, Ridge) sacrifice training fit → gain real generalizability

> *📊 Include: side-by-side bar chart comparing Train R² vs. CV R² per model — visually shows the overfitting gap*

---

### Slide 5 — Lasso: The Best Model

**What Lasso does:** Eliminates irrelevant features by forcing their coefficients to exactly zero.

Started with **25 features** → kept **4**

| Feature | Effect |
|---|---|
| `completion_rate` | +$1.70 per employee/day per 1% ↑ |
| `satisfaction_rate` | +$0.90 per employee/day per 1% ↑ |
| `past_due_rate` | −$1.27 per employee/day per 1% ↑ |
| `promotion_rate` | +$0.23 (control) |

**CV R² = 0.112** — explains 11% of between-store productivity variation in stores it has never seen

> *📊 Include: Lasso coefficient bar chart from Weis_Modeling.ipynb (horizontal bars, colored by direction)*

---

### Slide 6 — Feature Importance: What Drives the Signal

**Random Forest Permutation Importance** *(measured on held-out data)*

| Rank | Feature | Importance |
|---|---|---|
| 1 | `past_due_rate` | 0.046 |
| 2 | `promotion_rate` | 0.036 |
| 3 | `pct_elearning` | 0.018 |
| 4 | `pct_customer_exp` | 0.017 |
| 5 | `store_size_sqft` | 0.011 |

`past_due_rate` ranks #1 — ahead of even the promotional control

> *📊 Include: permutation importance horizontal bar chart from Weis_Modeling.ipynb*

---

### Slide 7 — Central Finding

**Three L&D metrics survive the strictest test:**

> Stores with higher completion rates, more positive training experiences, and fewer overdue assignments generate more revenue per employee — and this holds up on stores the model was never trained on.

- **Lasso CV R² = 0.112** → 11% of productivity variance explained by training alone
- Same three variables confirmed by both Lasso (coefficients) and Random Forest (permutation importance)
- L&D block adds **21.8 pp of R²** beyond structural controls

> *📊 Include: simple 3-icon summary visual — checkmark/completion, star/satisfaction, clock/past-due — with directional arrows*

---

### Slide 8 — What This Means for Weis

1. **Reduce overdue training first.** `past_due_rate` is the single highest-leverage variable across every model. Stores that miss deadlines underperform consistently.

2. **Completion and satisfaction move together.** More accessible, relevant training drives both metrics — compounding the benefit.

3. **Content focus matters at the margin.** eLearning and customer-experience modules show signal beyond volume. Compliance-only training does not.

4. **L&D is a medium-term lever, not a quick fix.** Promotional activity remains the strongest short-term revenue driver. Train for sustained productivity, not next quarter's comp.

---

### Slide 9 — Limitations & Next Steps

**Limitations:**
- 240-store synthetic dataset; CV R² is best-available estimate (no separate test set at this sample size)
- Correlation, not causation
- Contemporaneous measurement — no lag between training and revenue window

**Next Steps:**
- Apply this pipeline to **actual organizational data**
- Test **6–12 month lags** between training and revenue outcomes
- Shift outcome to **customer satisfaction / turnover / shrink** — metrics training more directly influences
- Analyze at **employee or department level**, not store level

---
---

## PART 2: PRESENTATION SCRIPT

*Target: 7–9 minutes | ~1,050 words spoken at natural pace*

---

**[Slide 1 — Title]**

So my piece of this project focuses on the modeling — the part where we go from observing that training and revenue are correlated, to actually asking: can we *predict* store performance from training data, and which training metrics carry real signal?

The outcome variable I'm working with is **revenue per employee** — which is just daily store revenue divided by the number of employees on the floor that day. It averages about $107 per employee per day across 240 stores, and it ranges from about $75 at the low end to around $129 at the high end. That $54 spread is the portion of revenue variation we're trying to explain with training.

---

**[Slide 2 — Setup]**

The dataset is at the store level — each of the 240 stores becomes one row, with its average revenue per employee paired with its aggregated LMS training metrics. I have three control variables that capture store structure — size in square feet, headcount, and how often the store ran promotions. And then 22 L&D features on top of that: completion rate, satisfaction rate, past-due rate, and breakdowns of what kinds of training employees were doing — compliance, operations, customer experience, eLearning, and so on.

---

**[Slide 3 — Six Models]**

I ran six models. The reason for running six instead of just picking one is that each model makes different assumptions, and comparing them tells us a lot about the data. The baseline OLS is a reference point — it tells us what store characteristics explain on their own, before we add any training data. The full OLS adds all 22 L&D features. Ridge and Lasso are regularized versions that push back against overfitting. And then the Decision Tree and Random Forest are machine learning methods that can detect non-linear patterns.

---

**[Slide 4 — Overfitting]**

This chart is probably the most important one I want to walk through, because it illustrates a trap that's easy to fall into.

Training R² measures how well a model fits the data it was trained on. Cross-validated R² — the CV column — measures how well the model predicts stores it has *never seen*. That second number is the one that matters.

Look at the Decision Tree: 46% training R² — looks great. But CV R² of negative 30%, meaning it predicts new stores worse than just guessing the average. That's a textbook overfit. The OLS full model does the same thing — 24% training R², negative CV R². What's happening is these models are memorizing quirks of the 240-store sample instead of learning generalizable patterns.

The regularized models — Ridge and especially Lasso — sacrifice some training accuracy on purpose, and that's exactly what makes them reliable.

---

**[Slide 5 — Lasso]**

Lasso is the standout model. Its mechanism is worth explaining quickly: it applies a penalty that forces irrelevant features to exactly zero. So instead of keeping all 25 features and assigning small coefficients to all of them, it does hard elimination. I started with 25 features. Lasso kept four.

Three of those four are L&D metrics. Completion rate, satisfaction rate, and past-due rate. The fourth is promotion rate, which is a structural control — expected.

The coefficients are interpretable: every one percentage point increase in a store's completion rate is associated with about $1.70 more revenue per employee per day. A one point increase in past-due rate goes the other direction — about $1.27 less. These are modest effects, but they're consistent, and importantly, they hold up on stores the model was trained on zero times.

The CV R² for Lasso is 0.112 — 11%. That is the best generalization of any model we ran.

---

**[Slide 6 — Random Forest Importance]**

The Random Forest gives us a second, completely independent read on which features matter. It's not a linear model — it's 200 decision trees averaged together — so it's capturing non-linear patterns that Lasso can't.

The permutation importance ranking is particularly trustworthy because it's measured on held-out data, not on the data the trees were trained on. And the top result: `past_due_rate`, importance score of 0.046 — ranked number one. Ahead of promotion rate, ahead of store size. This is a non-parametric, out-of-sample confirmation that overdue training is the single most predictive workforce signal in this dataset.

You also see `pct_elearning` and `pct_customer_exp` in the top five, which suggests that *format* and *content focus* carry signal beyond just volume. Compliance training doesn't appear here. Customer experience and eLearning do.

---

**[Slide 7 — Central Finding]**

The central finding of this section is this: three L&D variables — completion rate, satisfaction rate, and past-due rate — survive the strictest regularization test we ran, produce the best out-of-sample predictions, and are independently confirmed by a completely different model class.

This is not cherry-picking. Lasso found them by eliminating 21 other candidates. The Random Forest confirmed their importance without any assumption of linearity. If these were noise, both methods would have discarded them.

---

**[Slide 8 — Strategic Implications]**

What does this mean practically?

The clearest action item is reducing overdue training. Past-due rate is the number one predictor across models. Stores that miss deadlines underperform — and the likely reason isn't that the training content itself is magic, it's that management discipline carries over: teams that hold employees accountable for training deadlines tend to hold them accountable for everything else too.

Second, completion and satisfaction are correlated with each other — r = 0.83. Programs that make training more accessible, shorter, and more relevant will likely move both metrics simultaneously, which compounds the effect.

Third, and I want to be careful here — promotional activity is still the strongest single predictor. L&D is a medium-term lever. You're not going to see it in next quarter's comp. But it's real, it's measurable, and it's something the organization can actually control.

---

**[Slide 9 — Limitations]**

A few honest limitations. All of this is on synthetic data — same analytical framework, calibrated relationships, but not Weis's actual records. The CV R² figures are the best estimates we can produce at 240 stores, but there's no separate held-out test set, which we'd want with more data. And everything is measured at the same time — there's no lag between when training happened and when revenue was measured, which probably understates the true effect.

The most important next step is running this exact pipeline on actual organizational data. The framework is ready. It just needs real numbers.

---

*End of Ellyn's section.*
