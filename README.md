# Where to Help Next — Targeting Dashboard for NayePankh Foundation

This project is a decision-support tool that uses official government survey data (NFHS-5, 2019–21) to prioritize districts for NayePankh's education, menstrual hygiene, and nutrition campaigns. 

The primary deliverable is `index.html` — an interactive, self-contained dashboard showing where resources will create the highest impact.

---

## What the Dashboard Does

1. **Calculates a Need Index (0–100):** Combines female literacy, sanitation, child stunting, child marriage, and menstrual hygiene usage into an overall need score.
2. **Dynamic Prioritization:** Volunteers can adjust campaign weights live or use presets (e.g. prioritizing literacy for education drives) to re-rank districts instantly.
3. **Groups by Priority Tiers:** Uses a k-means clustering model (unsupervised ML) to split districts into High, Medium, and Lower priority tiers.
4. **Highlights "Awareness Gaps":** Runs a Ridge Regression model to predict expected menstrual hygiene access. Districts performing significantly worse than predicted (negative residuals) are flagged as high-opportunity targets for workshops.

---

## File Structure

*   **`index.html`** - The interactive dashboard. Double-click to open in any web browser.
*   **`ml_pipeline.py`** - The backend machine learning code. Standardizes data, runs K-Means, trains 4 regression models (all written from scratch in NumPy), and outputs `results.json`.
*   **`build_dashboard.py`** - Combines the HTML/CSS template with the JSON output to generate `index.html`.
*   **`nfhs5_districts.csv`** - Input dataset of 50 districts from 8 states across 5 key development indicators.
*   **`nfhs5_districts_scored.csv`** - The final ranked spreadsheet containing Need Index scores and tier classifications (open in Excel).
*   **`results.json`** - Structured calculations serving as the data feed for the front-end.

---

## Running the Pipeline

If you edit the district data in the CSV or modify the ML models, re-run the pipeline to rebuild the dashboard:

```bash
python ml_pipeline.py      # Computes scores, runs models, and writes results.json
python build_dashboard.py  # Injects results into the template and updates index.html
```

---

## Hosting Online (Free)

To get a public link to share with donors or supervisors:
*   **Netlify Drop:** Drag and drop `index.html` onto [app.netlify.com/drop](https://app.netlify.com/drop) to launch it instantly.
*   **GitHub Pages:** Upload `index.html` to a public repository and enable Pages in the repository Settings.

*Data source: National Family Health Survey (NFHS-5, 2019–21), Ministry of Health & Family Welfare, Govt. of India.*
