"""
NayePankh "Where to Help Next" — District Need-Targeting Model
==============================================================
A self-contained ML pipeline (numpy/pandas only, no scikit-learn) that turns
real NFHS-5 (2019-21) district indicators into an actionable priority ranking
for an NGO deciding where to run education / menstrual-hygiene / nutrition drives.

What it does:
  1. Builds a transparent composite NEED INDEX from 5 indicators.
  2. Groups districts into 3 priority tiers with k-means (implemented from scratch).
  3. Trains & compares 4 regression models (OLS, Ridge, kNN, Decision Tree),
     all coded from scratch, to predict menstrual-hygiene access from the other
     socio-economic indicators, evaluated with leave-one-out cross-validation.
  4. Identifies the DRIVERS of the menstrual-hygiene gap and flags districts that
     "under-perform" their predicted level (an access/awareness gap = NGO opportunity).
  5. Exports results.json for the live dashboard.

Data: NFHS-5 district fact sheets, compiled by github.com/pratapvardhan/NFHS-5
"""

import json
import numpy as np
import pandas as pd

np.random.seed(42)

# ----------------------------------------------------------------------------
# 1. LOAD DATA
# ----------------------------------------------------------------------------
df = pd.read_csv("nfhs5_districts.csv")

# Indicator orientation: does a HIGHER value mean MORE need?
#   female_literacy   higher = better  -> need rises when LOW
#   menstrual_hygiene higher = better  -> need rises when LOW   (NGO target metric)
#   sanitation        higher = better  -> need rises when LOW
#   child_marriage    higher = worse   -> need rises when HIGH
#   child_stunting    higher = worse   -> need rises when HIGH
INDICATORS = {
    "female_literacy":   "lower_is_worse",
    "menstrual_hygiene": "lower_is_worse",
    "sanitation":        "lower_is_worse",
    "child_marriage":    "higher_is_worse",
    "child_stunting":    "higher_is_worse",
}
LABELS = {
    "female_literacy":   "Female literacy",
    "menstrual_hygiene": "Menstrual hygiene use",
    "sanitation":        "Improved sanitation",
    "child_marriage":    "Girls married before 18",
    "child_stunting":    "Child stunting (under-5)",
}

# ----------------------------------------------------------------------------
# 2. NEED INDEX  (transparent, min-max normalised "deprivation" per indicator)
# ----------------------------------------------------------------------------
def deprivation(series, orientation):
    """Scale an indicator to 0-100 where 100 = highest need in the sample."""
    lo, hi = series.min(), series.max()
    rng = hi - lo if hi > lo else 1.0
    if orientation == "lower_is_worse":      # low value -> high need
        return (hi - series) / rng * 100.0
    else:                                    # high value -> high need
        return (series - lo) / rng * 100.0

dep = pd.DataFrame({col: deprivation(df[col], ori) for col, ori in INDICATORS.items()})
dep.columns = [c + "_dep" for c in dep.columns]

# Default = equal weights (0.20 each). The dashboard lets the user re-weight live.
WEIGHTS = {c: 0.20 for c in INDICATORS}
df["need_index"] = sum(dep[c + "_dep"] * WEIGHTS[c] for c in INDICATORS).round(1)

# ----------------------------------------------------------------------------
# 3. STANDARDISE  (z-scores; used by k-means, kNN, Ridge, and driver analysis)
# ----------------------------------------------------------------------------
def zscore(X, mean=None, std=None):
    if mean is None: mean = X.mean(axis=0)
    if std is None:  std = X.std(axis=0); std[std == 0] = 1.0
    return (X - mean) / std, mean, std

X_all = df[list(INDICATORS)].to_numpy(float)
Xz_all, mu_all, sd_all = zscore(X_all)

# ----------------------------------------------------------------------------
# 4. K-MEANS CLUSTERING (from scratch) -> 3 priority tiers
# ----------------------------------------------------------------------------
def kmeans(X, k=3, n_init=12, max_iter=200, seed=42):
    rng = np.random.default_rng(seed)
    best_inertia, best_labels, best_centers = np.inf, None, None
    for _ in range(n_init):
        # k-means++ initialisation
        centers = [X[rng.integers(len(X))]]
        for _ in range(1, k):
            d2 = np.min([((X - c) ** 2).sum(1) for c in centers], axis=0)
            probs = d2 / d2.sum()
            centers.append(X[rng.choice(len(X), p=probs)])
        centers = np.array(centers)
        for _ in range(max_iter):
            dists = np.stack([((X - c) ** 2).sum(1) for c in centers], axis=1)
            labels = dists.argmin(1)
            new = np.array([X[labels == j].mean(0) if (labels == j).any()
                            else centers[j] for j in range(k)])
            if np.allclose(new, centers): break
            centers = new
        inertia = sum(((X[labels == j] - centers[j]) ** 2).sum() for j in range(k))
        if inertia < best_inertia:
            best_inertia, best_labels, best_centers = inertia, labels, centers
    return best_labels, best_centers, best_inertia

labels, centers, inertia = kmeans(Xz_all, k=3)

# Order clusters by mean need index -> name tiers
order = (pd.Series(df["need_index"].values).groupby(labels).mean()
         .sort_values(ascending=False).index.tolist())
tier_name = {order[0]: "High priority", order[1]: "Medium priority", order[2]: "Lower priority"}
df["cluster"] = labels
df["tier"] = [tier_name[c] for c in labels]

# ----------------------------------------------------------------------------
# 5. SUPERVISED MODELS (from scratch) — predict menstrual hygiene from the rest
# ----------------------------------------------------------------------------
PRED_FEATURES = ["female_literacy", "sanitation", "child_marriage", "child_stunting"]
TARGET = "menstrual_hygiene"
Xf = df[PRED_FEATURES].to_numpy(float)
y  = df[TARGET].to_numpy(float)

class LinearReg:
    """Ordinary least squares via the normal equation (pseudo-inverse)."""
    def __init__(self, ridge=0.0): self.ridge = ridge
    def fit(self, X, y):
        Xs, self.mu, self.sd = zscore(X)           # standardise for stable/Ridge
        Xb = np.c_[np.ones(len(Xs)), Xs]
        n = Xb.shape[1]
        R = self.ridge * np.eye(n); R[0, 0] = 0.0  # don't penalise the intercept
        self.beta = np.linalg.pinv(Xb.T @ Xb + R) @ Xb.T @ y
        return self
    def predict(self, X):
        Xs = (X - self.mu) / self.sd
        return np.c_[np.ones(len(Xs)), Xs] @ self.beta

class KNNReg:
    def __init__(self, k=5): self.k = k
    def fit(self, X, y):
        self.Xs, self.mu, self.sd = zscore(X); self.y = y; return self
    def predict(self, X):
        Xs = (X - self.mu) / self.sd
        out = []
        for row in Xs:
            d = ((self.Xs - row) ** 2).sum(1)
            idx = np.argsort(d)[:self.k]
            out.append(self.y[idx].mean())
        return np.array(out)

class DecisionTreeReg:
    """Compact CART regressor (variance-reduction splits)."""
    def __init__(self, max_depth=4, min_leaf=3): self.max_depth, self.min_leaf = max_depth, min_leaf
    def fit(self, X, y): self.root = self._build(X, y, 0); return self
    def _build(self, X, y, depth):
        node = {"leaf": True, "val": float(y.mean())}
        if depth >= self.max_depth or len(y) < 2 * self.min_leaf or np.allclose(y, y[0]):
            return node
        best = None; best_sse = ((y - y.mean()) ** 2).sum()
        for f in range(X.shape[1]):
            vals = np.unique(X[:, f])
            for t in (vals[:-1] + vals[1:]) / 2:
                lm = X[:, f] <= t; rm = ~lm
                if lm.sum() < self.min_leaf or rm.sum() < self.min_leaf: continue
                sse = ((y[lm] - y[lm].mean()) ** 2).sum() + ((y[rm] - y[rm].mean()) ** 2).sum()
                if sse < best_sse:
                    best_sse = sse; best = (f, t, lm, rm)
        if best is None: return node
        f, t, lm, rm = best
        return {"leaf": False, "f": f, "t": t,
                "L": self._build(X[lm], y[lm], depth + 1),
                "R": self._build(X[rm], y[rm], depth + 1)}
    def _one(self, x, node):
        while not node["leaf"]:
            node = node["L"] if x[node["f"]] <= node["t"] else node["R"]
        return node["val"]
    def predict(self, X): return np.array([self._one(x, self.root) for x in X])

MODELS = {
    "Linear Regression": lambda: LinearReg(ridge=0.0),
    "Ridge Regression":  lambda: LinearReg(ridge=2.0),
    "k-Nearest Neighbours": lambda: KNNReg(k=5),
    "Decision Tree":     lambda: DecisionTreeReg(max_depth=4, min_leaf=3),
}

def metrics(y_true, y_pred):
    err = y_true - y_pred
    rmse = float(np.sqrt((err ** 2).mean()))
    mae = float(np.abs(err).mean())
    ss_res = (err ** 2).sum(); ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    r2 = float(1 - ss_res / ss_tot)
    return {"r2": round(r2, 3), "rmse": round(rmse, 2), "mae": round(mae, 2)}

# Leave-One-Out cross-validation (honest evaluation on tiny N)
def loo_cv(make_model, X, y):
    preds = np.empty(len(y))
    for i in range(len(y)):
        mask = np.arange(len(y)) != i
        m = make_model().fit(X[mask], y[mask])
        preds[i] = m.predict(X[i:i+1])[0]
    return preds

model_results = {}
for name, make in MODELS.items():
    cv_pred = loo_cv(make, Xf, y)
    model_results[name] = metrics(y, cv_pred)

best_model_name = min(model_results, key=lambda n: model_results[n]["rmse"])

# ----------------------------------------------------------------------------
# 6. DRIVERS — standardised OLS coefficients + correlations with the target
# ----------------------------------------------------------------------------
ols = LinearReg(ridge=0.0).fit(Xf, y)        # standardised inside -> beta comparable
drivers = []
for j, f in enumerate(PRED_FEATURES):
    corr = float(np.corrcoef(df[f], y)[0, 1])
    drivers.append({"feature": f, "label": LABELS[f],
                    "coef": round(float(ols.beta[j + 1]), 2),   # +1 skips intercept
                    "corr": round(corr, 2)})
drivers.sort(key=lambda d: abs(d["coef"]), reverse=True)

# In-sample fit of the BEST model -> residuals (actual - predicted).
# A strongly NEGATIVE residual = district does WORSE on menstrual hygiene than its
# socio-economic profile predicts -> an access/awareness gap NayePankh can close.
best = MODELS[best_model_name]().fit(Xf, y)
df["predicted_menstrual"] = best.predict(Xf).round(1)
df["residual"] = (df[TARGET] - df["predicted_menstrual"]).round(1)

# ----------------------------------------------------------------------------
# 7. EXPORT  results.json  (everything the dashboard needs)
# ----------------------------------------------------------------------------
districts = []
for i, r in df.iterrows():
    districts.append({
        "state": r["state"], "district": r["district"],
        "female_literacy": r["female_literacy"], "menstrual_hygiene": r["menstrual_hygiene"],
        "sanitation": r["sanitation"], "child_marriage": r["child_marriage"],
        "child_stunting": r["child_stunting"],
        # normalised deprivations (0-100) so the dashboard can re-weight live:
        "dep": {c: round(float(dep.iloc[i][c + "_dep"]), 1) for c in INDICATORS},
        "need_index": float(r["need_index"]), "tier": r["tier"], "cluster": int(r["cluster"]),
        "predicted_menstrual": float(r["predicted_menstrual"]), "residual": float(r["residual"]),
    })
districts.sort(key=lambda d: d["need_index"], reverse=True)
for rank, d in enumerate(districts, 1): d["rank"] = rank

tier_summary = []
for t in ["High priority", "Medium priority", "Lower priority"]:
    sub = df[df["tier"] == t]
    tier_summary.append({
        "tier": t, "n": int(len(sub)),
        "avg_need": round(float(sub["need_index"].mean()), 1),
        "avg_literacy": round(float(sub["female_literacy"].mean()), 1),
        "avg_menstrual": round(float(sub["menstrual_hygiene"].mean()), 1),
        "avg_marriage": round(float(sub["child_marriage"].mean()), 1),
        "avg_stunting": round(float(sub["child_stunting"].mean()), 1),
    })

results = {
    "meta": {
        "title": "Where to Help Next — District Need-Targeting Model",
        "source": "NFHS-5 (2019-21) district fact sheets, Govt. of India / IIPS",
        "n_districts": int(len(df)), "n_states": int(df["state"].nunique()),
        "states": sorted(df["state"].unique().tolist()),
        "indicators": [LABELS[c] for c in INDICATORS],
        "weights": WEIGHTS, "best_model": best_model_name,
    },
    "districts": districts,
    "tier_summary": tier_summary,
    "model_results": model_results,
    "drivers": drivers,
    "target_label": LABELS[TARGET],
    "feature_labels": LABELS,
    "indicator_orientation": INDICATORS,
}

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
df.to_csv("nfhs5_districts_scored.csv", index=False)

# ----------------------------------------------------------------------------
# 8. CONSOLE SUMMARY (for verification)
# ----------------------------------------------------------------------------
print(f"Districts: {len(df)}  |  States: {df['state'].nunique()}  |  Seed: 42")
print("\n=== MODEL COMPARISON (leave-one-out CV, predicting menstrual hygiene) ===")
print(f"{'Model':<24}{'R2':>8}{'RMSE':>8}{'MAE':>8}")
for n, m in model_results.items():
    star = "  <- best" if n == best_model_name else ""
    print(f"{n:<24}{m['r2']:>8}{m['rmse']:>8}{m['mae']:>8}{star}")

print("\n=== DRIVERS of menstrual-hygiene access (standardised OLS coef, corr) ===")
for d in drivers:
    print(f"{d['label']:<28} coef={d['coef']:>6}   corr={d['corr']:>6}")

print("\n=== PRIORITY TIERS (k-means, k=3) ===")
for t in tier_summary:
    print(f"{t['tier']:<18} n={t['n']:<3} avg need={t['avg_need']:<6} "
          f"lit={t['avg_literacy']}  menstrual={t['avg_menstrual']}  stunting={t['avg_stunting']}")

print("\n=== TOP 8 HIGHEST-NEED DISTRICTS ===")
for d in districts[:8]:
    print(f"{d['rank']:>2}. {d['district']+', '+d['state']:<28} need={d['need_index']:<6} {d['tier']}")

print("\n=== BIGGEST 'ACCESS GAP' DISTRICTS (worse than model predicts) ===")
gaps = sorted(districts, key=lambda d: d["residual"])[:5]
for d in gaps:
    print(f"{d['district']+', '+d['state']:<28} actual={d['menstrual_hygiene']:<6} "
          f"predicted={d['predicted_menstrual']:<6} gap={d['residual']}")
print("\nWrote results.json and nfhs5_districts_scored.csv")
