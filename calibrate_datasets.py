import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)

lms = pd.read_csv('lms_synthetic_validated_100k.csv')
rev = pd.read_csv('revenue_dataset_240stores.csv')

for col in ['Hire Date', 'Assignment Date', 'Due Date', 'Complete Date']:
    lms[col] = pd.to_datetime(lms[col])

REF_DATE = pd.Timestamp('2026-03-30')

# ── 1. Assign a quality score to each store ───────────────────────────────────
revenue_stores = sorted([s for s in lms['Location'].unique() if s != 'HQ_001'])
raw = np.random.normal(0, 1, size=len(revenue_stores))
raw = (raw - raw.mean()) / raw.std()   # standardize to mean=0, std=1
store_quality = dict(zip(revenue_stores, raw))
store_quality['HQ_001'] = 0.0

# ── 2. Target per-store rates ──────────────────────────────────────────────────
# completion_rate : mean=0.783, std=0.08  → range ~0.55–0.97
# satisfaction    : mean=0.898, std=0.06  → range ~0.72–0.99  (among completed)
store_targets = {
    s: {
        'completion':   float(np.clip(0.783 + 0.08 * q, 0.50, 0.97)),
        'satisfaction': float(np.clip(0.898 + 0.06 * q, 0.70, 0.99)),
    }
    for s, q in store_quality.items()
}

# ── 3. Modify LMS records per store ───────────────────────────────────────────
lms_new = lms.copy()

for store, tgt in store_targets.items():
    mask  = lms_new['Location'] == store
    idx   = lms_new[mask].index
    n     = len(idx)
    if n == 0:
        continue

    # --- completion -----------------------------------------------------------
    n_comp = int(round(n * tgt['completion']))
    n_comp = min(n_comp, n)
    perm   = np.random.permutation(n)
    comp_pos    = perm[:n_comp]
    notcomp_pos = perm[n_comp:]
    comp_idx    = idx[comp_pos]
    notcomp_idx = idx[notcomp_pos]

    lms_new.loc[comp_idx, 'Progress Status'] = 'Completed'
    n_ip = int(len(notcomp_idx) * 0.55)
    lms_new.loc[notcomp_idx[:n_ip], 'Progress Status'] = 'In Progress'
    lms_new.loc[notcomp_idx[n_ip:], 'Progress Status'] = 'Not Started'

    # --- complete dates -------------------------------------------------------
    a_dates    = lms_new.loc[comp_idx, 'Assignment Date']
    d_dates    = lms_new.loc[comp_idx, 'Due Date']
    window     = (d_dates.values - a_dates.values).astype('timedelta64[D]').astype(int)
    window     = np.clip(window, 1, 365)

    late_mask  = np.random.random(n_comp) < 0.15
    on_time    = np.array([np.random.randint(0, w + 1) for w in window])
    late_extra = np.random.randint(1, 91, size=n_comp)
    days_to_add = on_time.copy()
    days_to_add[late_mask] = window[late_mask] + late_extra[late_mask]

    c_dates = pd.to_datetime(a_dates.values) + pd.to_timedelta(days_to_add, unit='D')
    c_dates = pd.Series(c_dates).where(pd.Series(c_dates) <= REF_DATE, REF_DATE).values
    lms_new.loc[comp_idx,    'Complete Date'] = pd.to_datetime(c_dates)
    lms_new.loc[notcomp_idx, 'Complete Date'] = pd.NaT

    # --- satisfaction (only for completed records) ----------------------------
    n_sat     = int(round(n_comp * tgt['satisfaction']))
    n_sat     = min(n_sat, n_comp)
    sat_perm  = np.random.permutation(n_comp)
    sat_idx   = comp_idx[sat_perm[:n_sat]]
    nsat_idx  = comp_idx[sat_perm[n_sat:]]
    lms_new.loc[sat_idx,     'Satisfied'] = 'Yes'
    lms_new.loc[nsat_idx,    'Satisfied'] = 'No'
    lms_new.loc[notcomp_idx, 'Satisfied'] = np.nan

# ── 4. Recompute Past Due / Days Past Due (vectorized) ────────────────────────
due      = pd.to_datetime(lms_new['Due Date'])
complete = pd.to_datetime(lms_new['Complete Date'])
is_comp  = lms_new['Progress Status'] == 'Completed'

comp_late        = is_comp  & complete.notna() & (complete > due)
notcomp_overdue  = ~is_comp & (REF_DATE > due)

lms_new['Past Due']      = 'No'
lms_new.loc[comp_late | notcomp_overdue, 'Past Due'] = 'Yes'

lms_new['Days Past Due'] = 0
lms_new.loc[comp_late,       'Days Past Due'] = (complete[comp_late] - due[comp_late]).dt.days.astype(int)
lms_new.loc[notcomp_overdue, 'Days Past Due'] = (REF_DATE - due[notcomp_overdue]).dt.days.astype(int)

# ── 5. Restore date columns to string format ──────────────────────────────────
for col in ['Hire Date', 'Assignment Date', 'Due Date', 'Complete Date']:
    lms_new[col] = pd.to_datetime(lms_new[col], errors='coerce')
    lms_new[col] = lms_new[col].dt.strftime('%Y-%m-%d').where(lms_new[col].notna(), other=None)

lms_new.to_csv('lms_synthetic_calibrated.csv', index=False)
print("Saved: lms_synthetic_calibrated.csv")

# ── 6. Verify LMS store-level spread ──────────────────────────────────────────
lms_v = lms_new.copy()
lms_v['Is_Completed'] = (lms_v['Progress Status'] == 'Completed').astype(int)
lms_v['Is_Satisfied'] = (lms_v['Satisfied'] == 'Yes').astype(int)
lms_v['Is_Past_Due']  = (lms_v['Past Due'] == 'Yes').astype(int)

sv = lms_v[lms_v['Location'] != 'HQ_001'].groupby('Location').agg(
    completion_rate   = ('Is_Completed', 'mean'),
    satisfaction_rate = ('Is_Satisfied', 'mean'),
    past_due_rate     = ('Is_Past_Due',  'mean'),
).reset_index()

print("\n── LMS store-level spread ──────────────────────────────────")
for col in ['completion_rate', 'satisfaction_rate', 'past_due_rate']:
    print(f"  {col:25s}  min={sv[col].min():.3f}  max={sv[col].max():.3f}  std={sv[col].std():.3f}")

# ── 7. Revenue calibration ────────────────────────────────────────────────────
# Composite quality score from the three LMS metrics
for col in ['completion_rate', 'satisfaction_rate', 'past_due_rate']:
    mu, sigma = sv[col].mean(), sv[col].std()
    sv[f'{col}_z'] = (sv[col] - mu) / sigma

sv['quality_raw'] = (
    0.5 * sv['completion_rate_z']
  + 0.3 * sv['satisfaction_rate_z']
  - 0.2 * sv['past_due_rate_z']
)
# Standardize to std=1 so alpha has a clean interpretation
sv['quality_score'] = sv['quality_raw'] / sv['quality_raw'].std()

# alpha = 0.055 → targets ~15–20% of store-level Revenue_per_Employee variance
ALPHA = 0.055
sv['revenue_multiplier'] = 1 + ALPHA * sv['quality_score']

print(f"\n── Revenue multiplier range ─────────────────────────────────")
print(f"  min={sv['revenue_multiplier'].min():.4f}  max={sv['revenue_multiplier'].max():.4f}"
      f"  std={sv['revenue_multiplier'].std():.4f}")

rev_new = rev.merge(
    sv[['Location', 'revenue_multiplier']],
    left_on='Store_ID', right_on='Location',
    how='left'
)
rev_new['revenue_multiplier'] = rev_new['revenue_multiplier'].fillna(1.0)

# Scale base financial columns
for col in ['Daily_Revenue', 'Gross_Sales', 'Net_Revenue', 'Profit', 'Transactions']:
    rev_new[col] = (rev_new[col] * rev_new['revenue_multiplier']).round(2)

# Recompute all derived columns
rev_new['Revenue_per_Employee']      = (rev_new['Daily_Revenue'] / rev_new['Num_Employees']).round(4)
rev_new['Transactions_per_Employee'] = (rev_new['Transactions']  / rev_new['Num_Employees']).round(4)
rev_new['Avg_Basket_Size']           = (rev_new['Daily_Revenue'] / rev_new['Transactions']).round(4)
rev_new['Sales_per_SqFt']            = (rev_new['Daily_Revenue'] / rev_new['Store_Size_SqFt']).round(4)
rev_new['Profit_Margin_Pct']         = (rev_new['Profit'] / rev_new['Daily_Revenue']).round(6)
rev_new = rev_new.sort_values(['Store_ID', 'Date']).reset_index(drop=True)
rev_new['Revenue_Growth_Pct']        = rev_new.groupby('Store_ID')['Daily_Revenue'].pct_change().round(6)

rev_new = rev_new.drop(columns=['revenue_multiplier', 'Location'])
rev_new.to_csv('revenue_dataset_calibrated.csv', index=False)
print("\nSaved: revenue_dataset_calibrated.csv")

# ── 8. Verify revenue correlations ────────────────────────────────────────────
store_rev = rev_new.groupby('Store_ID')['Revenue_per_Employee'].mean().reset_index()
store_rev.columns = ['Location', 'avg_rev_per_emp']
merged = sv.merge(store_rev, on='Location')

print("\n── Key correlations with avg Revenue_per_Employee ───────────")
for col in ['completion_rate', 'satisfaction_rate', 'past_due_rate', 'quality_score']:
    r, p = stats.pearsonr(merged[col], merged['avg_rev_per_emp'])
    sig = '***' if p < 0.001 else ('**' if p < 0.01 else ('*' if p < 0.05 else ''))
    print(f"  {col:25s}  r={r:+.3f}  p={p:.4f}  {sig}")

print(f"\nStore-level Revenue_per_Employee  std={store_rev['avg_rev_per_emp'].std():.2f}")
print(f"Overall Revenue_per_Employee      std={rev_new['Revenue_per_Employee'].std():.2f}")
print("\nDone.")
