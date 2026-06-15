# 🌸 Where to Help Next: Data-Driven Need Targeting for NayePankh Foundation

[![HTML/CSS/JS](https://img.shields.io/badge/Front--End-HTML%20%7C%20CSS%20%7C%20JS-teal.svg)](#)
[![Python](https://img.shields.io/badge/Language-Python%203-blue.svg)](#)
[![ML](https://img.shields.io/badge/ML--Algorithms-From%20Scratch-orange.svg)](#)
[![Data Source](https://img.shields.io/badge/Data--Source-NFHS--5%20%28Govt.%20of%20India%29-red.svg)](#)

A decision-support system built with empathy and mathematical rigour to help **NayePankh Foundation** maximize the impact of its education, menstrual-hygiene, and nutrition drives. By combining official **Government of India survey data (NFHS-5, 2019-21)** with custom machine learning models, this tool turns raw district-level statistics into an **actionable, interactive prioritization dashboard**.

---

## 📌 The Core Problem: Resource Constraints at the Grassroots

As a growing, youth-led NGO, NayePankh operates under real-world constraints:
*   **Limited volunteer hours** and **finite financial resources**.
*   Choosing where to run the next drive (e.g., distributing sanitary pads, building sanitation units, or holding literacy workshops) is often based on guesswork or geographical convenience.
*   **The stakes are high:** Visiting a district that is relatively well-off means resources are diverted away from communities experiencing severe, hidden deprivation.

This project solves this challenge by making outreach decisions **evidence-based, transparent, and optimized for maximum human impact**.

---

## 🛠️ The Solution: "Where to Help Next"

This system takes **50 districts across 8 Indian states** and processes 5 critical indicators of development:
1.  **Female Literacy Rate** (for education drives)
2.  **Menstrual Hygiene Product Usage** (for sanitary pad distribution)
3.  **Household Sanitation Access** (for sanitation & health drives)
4.  **Underage Marriage Rates** (for social awareness campaigns)
5.  **Child Stunting under 5 years** (for nutrition & feeding drives)

### How the Machine Learning Pipeline Works:
```
  [Raw NFHS-5 Survey Data] 
            │
            ▼
 1. Composite Need Index (0-100) ──────► (Adjust weights live on the dashboard!)
            │
            ▼
 2. Unsupervised K-Means Tiering ──────► (Groups districts into High/Medium/Low priority waves)
            │
            ▼
 3. Supervised Regression Analysis ────► (Compares 4 custom models to find "Access Gaps")
```

1.  **Dynamic Need Index (0–100):** Raw statistics are normalized into a "deprivation score" from `0` (performing well) to `100` (highest need in the sample). These scores are weighted and combined. **The dashboard lets volunteers re-weight these live** depending on the specific drive (e.g. prioritize literacy for school drives).
2.  **Strategic Priority Tiers (K-Means Clustering):** An unsupervised K-Means clustering algorithm automatically groups districts into three operational phases: **High Priority** (first wave), **Medium Priority** (second wave), and **Lower Priority** (third wave).
3.  **Access-Gap Discovery (Ridge Regression):** The pipeline trains and compares **4 regression models** to predict menstrual hygiene access based on other socio-economic factors. The best-performing model flags **districts where menstrual hygiene is significantly lower than predicted** (negative residuals). These "Access Gaps" represent cultural or logistical bottlenecks where NayePankh's awareness workshops can create the fastest change.

---

## 🖥️ The Interactive Dashboard (`index.html`)

The ultimate deliverable is a **single, self-contained, interactive HTML dashboard** ([index.html](file:///c:/Users/abhil/OneDrive/Desktop/nayepankh%20ml%20project/index.html)). It requires no backend server, database, or technical setup—volunteers can open it by double-clicking it on any laptop or phone.

### Key Features:
*   **Live Weighted Recalculation:** Use interactive sliders to dynamically adjust indicator weights. The table instantly re-sorts and updates the ranking list.
*   **Advanced Visualizations:** 
    *   *Interactive Scatter Plot:* Shows the development landscape (Literacy vs. Menstrual Hygiene, sized by child stunting and colored by priority tier).
    *   *Tier Summary & Donut Chart:* Breaks down averages for High/Medium/Low tiers.
    *   *Model Performance:* Visually displays and compares $R^2$ accuracy for OLS, Ridge, k-NN, and Decision Tree.
*   **Actionable Narrative Prompts:** Dynamically displays the top 3 high-need districts and top 3 access-gap districts based on current weight settings.

---

## 📁 Repository Structure

| File / Folder | Purpose |
| :--- | :--- |
| **`index.html`** | The ready-to-use interactive dashboard. Double-click to open. |
| **`ml_pipeline.py`** | The core ML pipeline. Standardizes data, runs K-Means, trains 4 regression models, and generates scored metrics. |
| **`build_dashboard.py`** | Injector script that combines `results.json` with the HTML template to compile the dashboard. |
| **`nfhs5_districts.csv`** | Input dataset of 50 districts across 8 states with their raw NFHS-5 percentages. |
| **`results.json`** | Model calculations and results, serving as the bridge between Python and JS. |
| **`nfhs5_districts_scored.csv`** | The final scored and prioritized district list, readable in Excel or Google Sheets. |

---

## 🧪 Mathematical Rigour (Built from Scratch)

To demonstrate a complete, ground-up understanding of data science principles and ensure full transparency, **all machine learning models were coded from scratch using NumPy and Pandas** (no scikit-learn wrapper dependencies):

*   **Custom K-Means:** Implemented with Z-score standardization and **K-Means++ initialization** to guarantee stable cluster boundaries.
*   **Linear & Ridge Regression:** Solved via the Normal Equation $(X^T X + \lambda I)^{-1} X^T y$ in standardized space.
*   **k-Nearest Neighbors (k-NN):** A non-parametric distance-weighted regressor ($k=5$).
*   **Decision Tree Regressor (CART):** Recursively splits features to minimize sum-of-squared-errors (SSE).
*   **Leave-One-Out Cross-Validation (LOOCV):** Given the sample size of 50 districts, a standard train-test split is unstable. LOOCV trains the models on 49 districts and tests on the 1 held out, repeating this 50 times to get an honest, unbiased estimation of model generalization error (RMSE, MAE, and $R^2$).

---

## 🚀 How to Run and Extend

### 1. View the Dashboard Instantly
Simply double-click **`index.html`** in your browser. 
To share a live public link with the NGO in 60 seconds (completely free):
1.  Go to [Netlify Drop](https://app.netlify.com/drop).
2.  Drag and drop your `index.html` file onto the page.
3.  You will get a public link (e.g. `https://nayepankh-targeting.netlify.app`) to share with team members and donors.

### 2. Extend the Pipeline
To update the model with new districts (e.g. scaling up to all 707 districts in India):
1.  Add new rows with NFHS-5 indicator data to `nfhs5_districts.csv`.
2.  Run the ML pipeline:
    ```bash
    python ml_pipeline.py
    ```
3.  Rebuild the dashboard:
    ```bash
    python build_dashboard.py
    ```

---

## 💡 How this Project Benefits NayePankh Foundation

*   **Evidence-Backed Grant Proposals:** Presenting this tool in corporate CSR pitches proves that NayePankh allocates donor capital using high-integrity, data-driven decisions.
*   **Optimal Campaign Planning:** Program directors can target districts labeled "High priority" or locate high "Access Gaps" for immediate, high-yield interventions.
*   **Data-Driven NGO Culture:** Bridging the gap between advanced analytical models and non-technical grassroots volunteers, establishing a culture of measurement and optimization.

---

*Data compiled from the official Ministry of Health and Family Welfare / IIPS compilation, available at [github.com/pratapvardhan/NFHS-5](https://github.com/pratapvardhan/NFHS-5).*
