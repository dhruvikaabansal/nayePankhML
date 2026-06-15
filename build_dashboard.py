# Builds a single self-contained index.html from results.json (data injected inline).
import json

results = json.load(open("results.json"))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NayePankh · Where to Help Next — District Need Targeting (ML)</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    --teal:#0d8a72; --teal-d:#0a5f50; --amber:#f2a23c;
    --high:#e0564f; --med:#eaa53d; --low:#2fa37a;
    --ink:#13302b; --muted:#5d726c; --line:#e3ebe8; --bg:#f4f8f6; --card:#ffffff;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.55}
  h1,h2,h3,.brand{font-family:Poppins,sans-serif;margin:0}
  a{color:var(--teal-d)}
  .wrap{max-width:1120px;margin:0 auto;padding:0 20px}
  /* header */
  header{background:linear-gradient(135deg,var(--teal-d),var(--teal));color:#fff;padding:30px 0 90px}
  .nav{display:flex;align-items:center;gap:12px}
  .logo{width:38px;height:38px;border-radius:9px;background:#fff;display:grid;place-items:center;color:var(--teal-d);font-weight:700;font-family:Poppins}
  .brand{font-size:19px;font-weight:600;color:#fff}
  .brand small{display:block;font-size:11px;font-weight:400;opacity:.85;letter-spacing:.04em;font-family:Inter}
  .hero{margin-top:34px;max-width:760px}
  .tagchip{display:inline-block;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.25);
           padding:5px 12px;border-radius:30px;font-size:12.5px;font-weight:500;margin-bottom:14px}
  .hero h1{font-size:34px;line-height:1.18;font-weight:700}
  .hero p{font-size:16.5px;opacity:.94;margin-top:12px}
  /* kpi cards */
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:-62px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:0 6px 20px rgba(13,80,66,.06)}
  .kpi .v{font-family:Poppins;font-size:26px;font-weight:700;color:var(--teal-d)}
  .kpi .l{font-size:12.5px;color:var(--muted);margin-top:3px}
  /* sections */
  section{margin:46px 0}
  .eyebrow{color:var(--teal);font-weight:600;font-size:12.5px;letter-spacing:.08em;text-transform:uppercase}
  h2{font-size:24px;margin:6px 0 4px}
  .lead{color:var(--muted);font-size:15px;max-width:760px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 4px 16px rgba(13,80,66,.05)}
  .grid2{display:grid;grid-template-columns:1.15fr .85fr;gap:20px}
  .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .step{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
  .step .n{width:30px;height:30px;border-radius:8px;background:var(--teal);color:#fff;display:grid;place-items:center;font-weight:700;font-family:Poppins;margin-bottom:10px}
  .step h3{font-size:15.5px} .step p{font-size:13.5px;color:var(--muted);margin:6px 0 0}
  /* controls */
  .controls{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end}
  .slider{flex:1;min-width:150px}
  .slider label{font-size:12.5px;font-weight:600;display:flex;justify-content:space-between}
  .slider input{width:100%;accent-color:var(--teal)}
  .formula{font-size:12.5px;color:var(--muted);margin-top:10px}
  select{padding:8px 10px;border:1px solid var(--line);border-radius:9px;font-family:Inter;font-size:13.5px;background:#fff}
  .btn{background:var(--teal);color:#fff;border:0;padding:8px 14px;border-radius:9px;font-weight:600;cursor:pointer;font-family:Inter}
  /* table */
  table{width:100%;border-collapse:collapse;font-size:13.5px}
  th,td{padding:9px 10px;text-align:left;border-bottom:1px solid var(--line)}
  th{font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);cursor:pointer;user-select:none;white-space:nowrap}
  td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
  tr:hover td{background:#f7faf9}
  .pill{display:inline-block;padding:2px 9px;border-radius:20px;font-size:11.5px;font-weight:600;color:#fff}
  .pill.High{background:var(--high)} .pill.Medium{background:var(--med)} .pill.Lower{background:var(--low)}
  .bar{height:7px;border-radius:5px;background:linear-gradient(90deg,var(--low),var(--med),var(--high));position:relative}
  .gap-neg{color:var(--high);font-weight:600} .gap-pos{color:var(--low);font-weight:600}
  .chartbox{position:relative;height:300px}
  .note{font-size:12.5px;color:var(--muted)}
  .tablewrap{max-height:430px;overflow:auto;border:1px solid var(--line);border-radius:12px}
  .legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;margin-top:8px}
  .dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle}
  footer{background:var(--ink);color:#cfe0db;padding:26px 0;margin-top:50px;font-size:13px}
  footer a{color:#9fe0cf}
  .twocol{columns:2;column-gap:26px}
  .preset-btn{background:var(--card);border:1px solid var(--line);color:var(--muted);padding:6px 14px;border-radius:20px;font-weight:600;cursor:pointer;font-family:Inter;font-size:12.5px;transition:all .2s}
  .preset-btn:hover{border-color:var(--teal);color:var(--teal)}
  .preset-btn.active{background:var(--teal);color:#fff;border-color:var(--teal)}
  .warning-box{background:#fff8f0;border-left:4px solid var(--amber);border-radius:0 8px 8px 0;padding:12px 16px;font-size:13px;margin-top:16px;color:#7a531e}
  .grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
  .guide-col{border-right:1px solid var(--line);padding-right:16px}
  @media(max-width:860px){
    .kpis{grid-template-columns:repeat(2,1fr)}.grid2{grid-template-columns:1fr}
    .steps,.grid3,.grid4{grid-template-columns:1fr !important}.hero h1{font-size:27px}.twocol{columns:1}
    .guide-col{border-right:none !important;padding-right:0 !important;border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:16px}
  }
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="nav">
      <div class="logo">NP</div>
      <div class="brand">NayePankh Foundation<small>BADALTE BHARAT KI NAYI TASVEER · Govt. Reg. NGO</small></div>
    </div>
    <div class="hero">
      <span class="tagchip">Data project · Machine Learning for impact</span>
      <h1>Where to Help Next</h1>
      <p>A machine-learning model that reads real government survey data and tells NayePankh
         <b>which districts most need its education, menstrual-hygiene and nutrition drives</b> — so limited
         volunteers and funds go where they change the most lives.</p>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="kpis" id="kpis"></div>

  <!-- How to Read card -->
  <div class="card" style="margin-top: 24px;">
    <h3 style="font-size: 15px; color: var(--teal-d); margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
      📖 How to Read This Dashboard
    </h3>
    <div class="grid4">
      <div style="font-size: 12.5px; line-height: 1.45;">
        <strong style="color: var(--teal-d); display: block; margin-bottom: 3px;">1. Need Index</strong>
        Overall deprivation score (0–100) combining all 5 indicators. Higher = greater need.
      </div>
      <div style="font-size: 12.5px; line-height: 1.45;">
        <strong style="color: var(--teal-d); display: block; margin-bottom: 3px;">2. Tier</strong>
        High, Medium, or Lower priority waves determined by the k-means clustering model.
      </div>
      <div style="font-size: 12.5px; line-height: 1.45;">
        <strong style="color: var(--teal-d); display: block; margin-bottom: 3px;">3. Awareness Gap</strong>
        Menstrual hygiene performing worse than predicted. Negative values point to awareness/access barriers.
      </div>
      <div style="font-size: 12.5px; line-height: 1.45;">
        <strong style="color: var(--teal-d); display: block; margin-bottom: 3px;">4. Campaign Presets</strong>
        Pre-configured weight settings to immediately re-rank districts based on NayePankh's target intervention.
      </div>
    </div>
  </div>

  <section>
    <div class="eyebrow">How it works</div>
    <h2>From raw survey numbers to an action list</h2>
    <div class="steps" style="margin-top:16px">
      <div class="step"><div class="n">1</div><h3>Score the need</h3>
        <p>Every district gets a 0–100 <b>Need Index</b> built from 5 indicators that match NayePankh's
           programmes: female literacy, menstrual-hygiene use, sanitation, child marriage and child stunting.</p></div>
      <div class="step"><div class="n">2</div><h3>Group into tiers</h3>
        <p>A <b>k-means</b> clustering model (unsupervised ML) sorts districts into High / Medium / Lower
           priority tiers, so outreach can be planned in waves.</p></div>
      <div class="step"><div class="n">3</div><h3>Predict &amp; find gaps</h3>
        <p>Four prediction models compete to forecast menstrual-hygiene access. The best one flags districts
           doing <b>worse than expected</b> — a sign of an access gap a pad drive can close.</p></div>
    </div>
  </section>

  <section>
    <div class="eyebrow">The need landscape</div>
    <h2>50 districts, 8 states — coloured by priority tier</h2>
    <p class="lead">Each bubble is a district. Bottom-left (low literacy, low menstrual-hygiene use) is where need
       is greatest; bubble size shows child stunting. The model learns this structure automatically.</p>
    <div class="grid2" style="margin-top:16px">
      <div class="card"><div class="chartbox"><canvas id="scatter"></canvas></div>
        <div class="legend">
          <span><span class="dot" style="background:var(--high)"></span>High priority</span>
          <span><span class="dot" style="background:var(--med)"></span>Medium priority</span>
          <span><span class="dot" style="background:var(--low)"></span>Lower priority</span>
          <span class="note">· bubble size = child stunting</span>
        </div>
      </div>
      <div class="card">
        <h3 style="font-size:16px">Priority tiers at a glance</h3>
        <div class="chartbox" style="height:180px"><canvas id="donut"></canvas></div>
        <div id="tierStats" style="margin-top:8px"></div>
      </div>
    </div>
  </section>

  <section>
    <div class="eyebrow">Interactive · try it</div>
    <h2>Choose a Campaign Focus</h2>
    <p class="lead">The rankings below update based on the type of intervention NayePankh plans to run.</p>
    <div class="card" style="margin-top:16px">
      <div style="font-size:13px; font-weight:600; margin-bottom:10px; color:var(--teal-d); text-transform:uppercase; letter-spacing:0.04em">Quick Campaign Presets:</div>
      <div class="presets" style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px" id="presets">
        <button class="preset-btn active" data-preset="balanced" onclick="selectPreset('balanced')">Balanced View</button>
        <button class="preset-btn" data-preset="education" onclick="selectPreset('education')">Education Drive</button>
        <button class="preset-btn" data-preset="hygiene" onclick="selectPreset('hygiene')">Menstrual Hygiene Drive</button>
        <button class="preset-btn" data-preset="sanitation" onclick="selectPreset('sanitation')">Sanitation Drive</button>
        <button class="preset-btn" data-preset="nutrition" onclick="selectPreset('nutrition')">Nutrition Drive</button>
      </div>
      <div class="controls" id="sliders"></div>
      <div class="formula" id="formula"></div>
    </div>

    <div class="warning-box">
      ⚠️ <b>Balanced View</b> should be used for overall district prioritization.<br>
      Campaign-specific weights should only be used when planning a focused intervention such as menstrual hygiene, education, nutrition, or sanitation drives.
    </div>

    <!-- Recommended Actions card -->
    <div class="card" style="margin-top: 24px; border-top: 4px solid var(--teal);">
      <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid var(--line); padding-bottom: 12px; margin-bottom: 20px;">
        <div>
          <span class="eyebrow" style="font-size: 11px;">Decision Guidance</span>
          <h3 style="font-size: 18px; font-family: Poppins; font-weight: 700; margin-top: 2px;">Recommended Actions</h3>
        </div>
        <span class="note" style="font-size: 12px;">Updated dynamically based on focus</span>
      </div>
      
      <div class="grid3" style="gap: 20px;">
        <!-- Column 1: Absolute Top Targets -->
        <div class="guide-col">
          <h4 style="font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin: 0 0 12px;">🚨 Top Targets</h4>
          <div style="margin-bottom: 14px;">
            <strong style="font-size: 11px; color: var(--muted); display: block; margin-bottom: 2px;">Highest Need District:</strong>
            <div style="display: flex; align-items: baseline; gap: 8px; margin: 2px 0;">
              <span id="recNeedName" style="font-size: 15px; font-weight: 700; font-family: Poppins;">-</span>
              <span class="pill High" id="recNeedTier" style="font-size: 10px; padding: 1px 5px;">-</span>
            </div>
            <p class="note" style="margin: 0; font-size: 11.5px; line-height: 1.45;">Need: <b id="recNeedIndex">-</b> · <span id="recNeedReason">-</span></p>
          </div>
          <div>
            <strong style="font-size: 11px; color: var(--muted); display: block; margin-bottom: 2px;">Menstrual Hygiene Opportunity:</strong>
            <div style="display: flex; align-items: baseline; gap: 8px; margin: 2px 0;">
              <span id="recGapName" style="font-size: 15px; font-weight: 700; font-family: Poppins;">-</span>
              <span id="recGapValue" style="font-weight: 700; color: var(--high); font-size: 12.5px;">-</span>
            </div>
            <p class="note" id="recGapReason" style="margin: 0; line-height: 1.45; font-size: 11.5px;">-</p>
          </div>
        </div>

        <!-- Column 2: Top by Operational Tier -->
        <div class="guide-col">
          <h4 style="font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin: 0 0 12px;">🎯 Top by Operational Tier</h4>
          <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; border-bottom: 1px dashed var(--line); padding-bottom: 6px;">
              <span><span class="pill High" style="margin-right: 6px; padding: 1px 6px; font-size: 10px;">High</span> <span id="tierTopHighName">-</span></span>
              <strong id="tierTopHighVal" class="note" style="font-size:11.5px; color:var(--ink)">-</strong>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; border-bottom: 1px dashed var(--line); padding-bottom: 6px;">
              <span><span class="pill Medium" style="margin-right: 6px; padding: 1px 6px; font-size: 10px;">Medium</span> <span id="tierTopMedName">-</span></span>
              <strong id="tierTopMedVal" class="note" style="font-size:11.5px; color:var(--ink)">-</strong>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; padding-bottom: 2px;">
              <span><span class="pill Lower" style="margin-right: 6px; padding: 1px 6px; font-size: 10px;">Lower</span> <span id="tierTopLowName">-</span></span>
              <strong id="tierTopLowVal" class="note" style="font-size:11.5px; color:var(--ink)">-</strong>
            </div>
          </div>
        </div>

        <!-- Column 3: State Need Rankings -->
        <div>
          <h4 style="font-size: 12.5px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin: 0 0 12px;">🗺️ State Need Rankings</h4>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <div>
              <strong style="color: var(--high); font-size: 11px; display: block; text-transform: uppercase; letter-spacing: 0.02em; margin-bottom: 3px;">🚨 High Need</strong>
              <div id="stateListHigh" style="display: flex; flex-direction: column; gap: 3px; font-size: 11.5px;">-</div>
            </div>
            <div>
              <strong style="color: var(--amber); font-size: 11px; display: block; text-transform: uppercase; letter-spacing: 0.02em; margin-bottom: 3px; margin-top: 2px;">⚠️ Medium Need</strong>
              <div id="stateListMed" style="display: flex; flex-direction: column; gap: 3px; font-size: 11.5px;">-</div>
            </div>
            <div>
              <strong style="color: var(--low); font-size: 11px; display: block; text-transform: uppercase; letter-spacing: 0.02em; margin-bottom: 3px; margin-top: 2px;">✅ Lower Need</strong>
              <div id="stateListLow" style="display: flex; flex-direction: column; gap: 3px; font-size: 11.5px;">-</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div style="display:flex;gap:12px;align-items:center;margin:16px 0 8px;flex-wrap:wrap">
      <strong>District priority ranking</strong>
      <select id="stateFilter"><option value="">All states</option></select>
      <span class="note">Click any column to sort · ranked by your live Need Index</span>
    </div>
    <div class="tablewrap">
      <table id="tbl">
        <thead><tr>
          <th data-k="rank" class="num">#</th>
          <th data-k="district">District</th>
          <th data-k="state">State</th>
          <th data-k="liveNeed" class="num">Need Index</th>
          <th data-k="tier">Tier</th>
          <th data-k="female_literacy" class="num">Lit %</th>
          <th data-k="menstrual_hygiene" class="num">Menstr %</th>
          <th data-k="child_marriage" class="num">Marr %</th>
          <th data-k="child_stunting" class="num">Stunt %</th>
          <th data-k="residual" class="num" title="Negative values indicate districts where menstrual hygiene use is lower than expected and may benefit from awareness campaigns.">Awareness Gap ⓘ</th>
        </tr></thead>
        <tbody></tbody>
      </table>
    </div>
    <p class="note" style="margin-top:8px">“Awareness Gap” = actual menstrual-hygiene use minus what the model predicts
       from the district's profile. <span class="gap-neg">Red (negative)</span> = worse than expected → a likely
       awareness/access problem NayePankh can address directly.</p>
  </section>

  <section>
    <div class="eyebrow">Model comparison</div>
    <h2>Four models, tested fairly — the best one wins</h2>
    <p class="lead">Each model predicts a district's menstrual-hygiene use from its other indicators, scored with
       leave-one-out cross-validation (trained on 49 districts, tested on the 1 held out, repeated 50×).</p>
    
    <div class="card" style="margin-top: 16px; margin-bottom: 16px; border-left: 4px solid var(--teal);">
      <h3 style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin-bottom: 6px;">🏆 Best Model Selected</h3>
      <div style="font-size: 19px; font-weight: 700; font-family: Poppins; color: var(--teal-d);">Ridge Regression</div>
      <p class="note" style="margin-top: 4px; margin-bottom: 0; line-height: 1.45;"><b>Reason:</b> Lowest RMSE (Root Mean Squared Error) of 8.9 during Leave-One-Out Cross Validation. We compared multiple models (Linear Regression, Ridge Regression, k-Nearest Neighbours, and Decision Tree) and dynamically selected the best-performing one to ensure predictions are robust and generalize well to unseen districts without overfitting.</p>
    </div>

    <div class="grid2">
      <div class="card"><div class="chartbox"><canvas id="models"></canvas></div>
        <p class="note">R² = share of variation explained (1.0 is perfect). The winner is highlighted.</p></div>
      <div class="card">
        <h3 style="font-size:16px">What drives menstrual-hygiene access?</h3>
        <p class="note">How each factor moves with menstrual-hygiene use across districts. Green = higher access, red = lower.</p>
        <div class="chartbox" style="height:230px"><canvas id="drivers"></canvas></div>
      </div>
    </div>
  </section>

  <section>
    <div class="eyebrow">For NayePankh</div>
    <h2>How to use this</h2>
    <div class="grid3" style="margin-top:16px">
      <div class="card"><h3 style="font-size:15.5px;color:var(--teal-d)">🎯 Target new districts</h3>
        <p class="note" id="useTop"></p></div>
      <div class="card"><h3 style="font-size:15.5px;color:var(--teal-d)">🩸 Prioritise pad drives</h3>
        <p class="note" id="useGap"></p></div>
      <div class="card"><h3 style="font-size:15.5px;color:var(--teal-d)">📊 Brief donors &amp; partners</h3>
        <p class="note">Share this link in grant applications and CSR pitches to show decisions are evidence-led —
           a strong differentiator for a youth-run NGO.</p></div>
    </div>
  </section>

  <section>
    <div class="card">
      <div class="eyebrow">Methodology &amp; data</div>
      <h2 style="margin-bottom:8px">Built to be trusted</h2>
      <div class="twocol note">
        <p><b>Data.</b> National Family Health Survey (NFHS-5, 2019–21) district fact sheets — official Government
           of India / IIPS statistics, compiled openly on GitHub. This demo uses a 50-district sample across 8
           states spanning the full need spectrum; the identical pipeline scales to all 707 Indian districts.</p>
        <p><b>Need Index.</b> Each indicator is min-max normalised to a 0–100 “deprivation” score (relative to the
           sample) and combined with adjustable weights — fully transparent, no black box.</p>
        <p><b>Models.</b> Clustering (k-means) and four regressors (Linear, Ridge, k-NN, Decision Tree) were
           implemented from scratch in NumPy and validated with leave-one-out cross-validation for an honest read
           on a small sample.</p>
        <p><b>Honesty.</b> The best model explains roughly half the variation (R²&nbsp;≈&nbsp;0.5) — useful for
           prioritisation, not a crystal ball. Indicators are correlates of need, not proof of causation.</p>
      </div>
    </div>
  </section>
</div>

<footer><div class="wrap">
  <b>NayePankh Foundation</b> · Where to Help Next — a data &amp; ML demonstration ·
  Data: NFHS-5 (2019–21), Govt. of India / IIPS ·
  <a href="https://nayepankh.com">nayepankh.com</a><br>
  <span style="opacity:.7">Built as a student data-science project. Indicators are need correlates; figures are survey estimates.</span>
</div></footer>

<script>
const DATA = __DATA__;
const TIERKEY = t => t.split(" ")[0]; // "High priority" -> "High"
const INDS = ["female_literacy","menstrual_hygiene","sanitation","child_marriage","child_stunting"];
const SHORT = {female_literacy:"Literacy",menstrual_hygiene:"Menstrual hygiene",sanitation:"Sanitation",
               child_marriage:"Child marriage",child_stunting:"Child stunting"};
const tierColor = {High:"#e0564f",Medium:"#eaa53d",Lower:"#2fa37a"};
let weights = {female_literacy:20,menstrual_hygiene:20,sanitation:20,child_marriage:20,child_stunting:20};
let sortKey="liveNeed", sortDir=-1, stateF="";

/* ---------- KPIs ---------- */
function renderKPIs(){
  const m=DATA.meta, high=DATA.tier_summary.find(t=>t.tier=="High priority");
  const best=DATA.model_results[m.best_model];
  const topDriver=DATA.drivers[0];
  const cards=[
    [m.n_districts+" districts", "analysed across "+m.n_states+" states"],
    [high.n+" high-priority", "districts flagged for first action"],
    [m.best_model.split(" ")[0]+" · R² "+best.r2, "best model (±"+best.rmse+" pts error)"],
    [SHORT[topDriver.feature], "strongest driver of menstrual hygiene"],
  ];
  document.getElementById("kpis").innerHTML = cards.map(c=>
    `<div class="kpi"><div class="v">${c[0]}</div><div class="l">${c[1]}</div></div>`).join("");
}

/* ---------- live Need Index ---------- */
function liveNeed(d){
  let sw=INDS.reduce((s,k)=>s+weights[k],0)||1;
  return INDS.reduce((s,k)=>s+d.dep[k]*weights[k],0)/sw;
}
function recompute(){
  DATA.districts.forEach(d=>d.liveNeed=+liveNeed(d).toFixed(1));
  const fw=INDS.map(k=>`${(weights[k]/(INDS.reduce((s,j)=>s+weights[j],0)||1)*100).toFixed(0)}% ${SHORT[k]}`);
  document.getElementById("formula").innerHTML="Need Index = "+fw.join("  +  ");
  renderTable();
}

/* ---------- presets ---------- */
const presets = {
  balanced: {female_literacy: 20, menstrual_hygiene: 20, sanitation: 20, child_marriage: 20, child_stunting: 20},
  education: {female_literacy: 60, menstrual_hygiene: 10, sanitation: 10, child_marriage: 10, child_stunting: 10},
  hygiene: {female_literacy: 10, menstrual_hygiene: 60, sanitation: 10, child_marriage: 10, child_stunting: 10},
  sanitation: {female_literacy: 10, menstrual_hygiene: 10, sanitation: 60, child_marriage: 10, child_stunting: 10},
  nutrition: {female_literacy: 10, menstrual_hygiene: 10, sanitation: 10, child_marriage: 10, child_stunting: 60}
};

function selectPreset(name){
  weights = {...presets[name]};
  INDS.forEach(k=>{
    const inp = document.querySelector(`#sliders input[data-k="${k}"]`);
    if(inp) inp.value = weights[k];
    const span = document.getElementById("w_"+k);
    if(span) span.textContent = weights[k];
  });
  document.querySelectorAll('#presets .preset-btn').forEach(btn=>{
    btn.classList.toggle('active', btn.dataset.preset === name);
  });
  recompute();
}

/* ---------- dynamic reasoning helpers ---------- */
function getReasonText(depObj) {
  const items = [];
  if (depObj.female_literacy >= 50) items.push("low literacy");
  if (depObj.sanitation >= 50) items.push("poor sanitation");
  if (depObj.child_marriage >= 50) items.push("high child marriage");
  if (depObj.child_stunting >= 50) items.push("high stunting");
  if (depObj.menstrual_hygiene >= 50) items.push("poor menstrual hygiene use");
  
  if (items.length === 0) {
    const key = Object.keys(depObj).reduce((a, b) => depObj[a] > depObj[b] ? a : b);
    const labelMap = {
      female_literacy: "literacy challenges",
      sanitation: "sanitation deficits",
      child_marriage: "child marriage issues",
      child_stunting: "nutritional stunting",
      menstrual_hygiene: "menstrual hygiene barriers"
    };
    return "Moderate challenges driven by " + labelMap[key] + ".";
  }
  
  if (items.length === 1) return items[0].charAt(0).toUpperCase() + items[0].slice(1) + ".";
  if (items.length === 2) return items[0].charAt(0).toUpperCase() + items[0].slice(1) + " and " + items[1] + ".";
  return items[0].charAt(0).toUpperCase() + items[0].slice(1) + ", " + items.slice(1, -1).join(", ") + " and " + items[items.length - 1] + ".";
}

function updateRecommended(rows) {
  if (!rows || rows.length === 0) {
    document.getElementById("recNeedName").textContent = "-";
    document.getElementById("recNeedTier").style.display = "none";
    document.getElementById("recNeedIndex").textContent = "-";
    document.getElementById("recNeedReason").textContent = "No data available.";
    document.getElementById("recGapName").textContent = "-";
    document.getElementById("recGapValue").textContent = "-";
    document.getElementById("recGapReason").textContent = "No data available.";
    document.getElementById("tierTopHighName").textContent = "-";
    document.getElementById("tierTopHighVal").textContent = "-";
    document.getElementById("tierTopMedName").textContent = "-";
    document.getElementById("tierTopMedVal").textContent = "-";
    document.getElementById("tierTopLowName").textContent = "-";
    document.getElementById("tierTopLowVal").textContent = "-";
    document.getElementById("stateListHigh").innerHTML = "-";
    document.getElementById("stateListMed").innerHTML = "-";
    document.getElementById("stateListLow").innerHTML = "-";
    return;
  }
  
  // 1. Highest Need
  const topNeed = rows[0];
  document.getElementById("recNeedName").textContent = `${topNeed.district} (${topNeed.state})`;
  const tier = TIERKEY(topNeed.tier);
  const tierEl = document.getElementById("recNeedTier");
  tierEl.style.display = "inline-block";
  tierEl.className = `pill ${tier}`;
  tierEl.textContent = tier;
  document.getElementById("recNeedIndex").textContent = topNeed.liveNeed.toFixed(1);
  document.getElementById("recNeedReason").textContent = getReasonText(topNeed.dep);
  
  // 2. Biggest Opportunity
  const opps = [...rows].sort((a, b) => a.residual - b.residual);
  const topOpp = opps[0];
  document.getElementById("recGapName").textContent = `${topOpp.district} (${topOpp.state})`;
  document.getElementById("recGapValue").textContent = topOpp.residual.toFixed(1);
  document.getElementById("recGapReason").textContent = 
    `Menstrual hygiene use (${topOpp.menstrual_hygiene}%) is significantly lower than predicted (${topOpp.predicted_menstrual}%) based on socio-economic indicators.`;

  // 3. Highest Need by Tier
  const highTierRows = rows.filter(d => TIERKEY(d.tier) === "High");
  const medTierRows = rows.filter(d => TIERKEY(d.tier) === "Medium");
  const lowTierRows = rows.filter(d => TIERKEY(d.tier) === "Lower");

  if (highTierRows.length > 0) {
    document.getElementById("tierTopHighName").textContent = `${highTierRows[0].district} (${highTierRows[0].state})`;
    document.getElementById("tierTopHighVal").textContent = `Need: ${highTierRows[0].liveNeed.toFixed(1)}`;
  } else {
    document.getElementById("tierTopHighName").textContent = "N/A";
    document.getElementById("tierTopHighVal").textContent = "-";
  }

  if (medTierRows.length > 0) {
    document.getElementById("tierTopMedName").textContent = `${medTierRows[0].district} (${medTierRows[0].state})`;
    document.getElementById("tierTopMedVal").textContent = `Need: ${medTierRows[0].liveNeed.toFixed(1)}`;
  } else {
    document.getElementById("tierTopMedName").textContent = "N/A";
    document.getElementById("tierTopMedVal").textContent = "-";
  }

  if (lowTierRows.length > 0) {
    document.getElementById("tierTopLowName").textContent = `${lowTierRows[0].district} (${lowTierRows[0].state})`;
    document.getElementById("tierTopLowVal").textContent = `Need: ${lowTierRows[0].liveNeed.toFixed(1)}`;
  } else {
    document.getElementById("tierTopLowName").textContent = "N/A";
    document.getElementById("tierTopLowVal").textContent = "-";
  }

  // 4. State Need Rankings
  const stateNeeds = {};
  rows.forEach(d => {
    if (!stateNeeds[d.state]) {
      stateNeeds[d.state] = { sum: 0, count: 0 };
    }
    stateNeeds[d.state].sum += d.liveNeed;
    stateNeeds[d.state].count++;
  });

  const stateList = Object.entries(stateNeeds).map(([name, data]) => ({
    name: name,
    avg: data.sum / data.count
  })).sort((a, b) => b.avg - a.avg);

  const highStates = [];
  const medStates = [];
  const lowStates = [];

  stateList.forEach(s => {
    if (s.avg >= 55) {
      highStates.push(s);
    } else if (s.avg >= 35) {
      medStates.push(s);
    } else {
      lowStates.push(s);
    }
  });

  const renderStateItem = s => `
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px dashed var(--line); padding: 3px 0;">
      <span><b>${s.name}</b></span>
      <span class="note" style="font-weight:600; color:var(--ink)">Avg: ${s.avg.toFixed(1)}</span>
    </div>
  `;

  document.getElementById("stateListHigh").innerHTML = highStates.length > 0 
    ? highStates.map(renderStateItem).join("") 
    : `<div style="color:var(--muted); font-style:italic; font-size:12px;">No states in this tier</div>`;

  document.getElementById("stateListMed").innerHTML = medStates.length > 0 
    ? medStates.map(renderStateItem).join("") 
    : `<div style="color:var(--muted); font-style:italic; font-size:12px;">No states in this tier</div>`;

  document.getElementById("stateListLow").innerHTML = lowStates.length > 0 
    ? lowStates.map(renderStateItem).join("") 
    : `<div style="color:var(--muted); font-style:italic; font-size:12px;">No states in this tier</div>`;
}

/* ---------- sliders ---------- */
function renderSliders(){
  document.getElementById("sliders").innerHTML = INDS.map(k=>
    `<div class="slider"><label>${SHORT[k]} <span id="w_${k}">${weights[k]}</span></label>
     <input type="range" min="0" max="100" value="${weights[k]}" data-k="${k}"></div>`).join("");
  document.querySelectorAll('#sliders input').forEach(inp=>{
    inp.addEventListener('input',e=>{
      const k=e.target.dataset.k; weights[k]=+e.target.value;
      document.getElementById("w_"+k).textContent=e.target.value;
      document.querySelectorAll('#presets .preset-btn').forEach(btn=>btn.classList.remove('active'));
      recompute();
    });
  });
}

/* ---------- table ---------- */
function renderTable(){
  let rows=DATA.districts.filter(d=>!stateF||d.state==stateF);
  rows.sort((a,b)=>{
    let va=a[sortKey],vb=b[sortKey];
    if(typeof va=="string") return sortDir*va.localeCompare(vb);
    return sortDir*(va-vb);
  });
  rows.forEach((d,i)=>d._r=i+1);
  const tb=document.querySelector("#tbl tbody");
  tb.innerHTML=rows.map(d=>{
    const gap=d.residual, gcls=gap<0?"gap-neg":"gap-pos";
    const w=Math.max(2,Math.min(100,d.liveNeed));
    return `<tr>
      <td class="num">${d._r}</td>
      <td><b>${d.district}</b></td><td>${d.state}</td>
      <td class="num"><div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">
          <span>${d.liveNeed.toFixed(1)}</span>
          <div class="bar" style="width:46px"><div style="position:absolute;left:0;top:0;height:100%;width:${w}%;background:rgba(0,0,0,.18);border-radius:5px"></div></div></div></td>
      <td><span class="pill ${TIERKEY(d.tier)}">${TIERKEY(d.tier)}</span></td>
      <td class="num">${d.female_literacy}</td>
      <td class="num">${d.menstrual_hygiene}</td>
      <td class="num">${d.child_marriage}</td>
      <td class="num">${d.child_stunting}</td>
      <td class="num ${gcls}">${gap>0?"+":""}${gap}</td>
    </tr>`;}).join("");
  
  updateRecommended(rows);
}
function setupTableUI(){
  document.querySelectorAll("#tbl th").forEach(th=>th.addEventListener("click",()=>{
    const k=th.dataset.k; if(sortKey==k) sortDir*=-1; else {sortKey=k; sortDir=(k=="district"||k=="state")?1:-1;}
    renderTable();
  }));
  const sel=document.getElementById("stateFilter");
  DATA.meta.states.forEach(s=>{let o=document.createElement("option");o.value=o.textContent=s;sel.appendChild(o);});
  sel.addEventListener("change",e=>{stateF=e.target.value;renderTable();});
}

/* ---------- charts ---------- */
function charts(){
  // scatter
  new Chart(document.getElementById("scatter"),{type:"bubble",
    data:{datasets:["High priority","Medium priority","Lower priority"].map(t=>({
      label:t,backgroundColor:tierColor[TIERKEY(t)]+"cc",borderColor:tierColor[TIERKEY(t)],
      data:DATA.districts.filter(d=>d.tier==t).map(d=>({x:d.female_literacy,y:d.menstrual_hygiene,
        r:4+d.child_stunting/5,district:d.district,state:d.state}))}))},
    options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>
      `${c.raw.district}, ${c.raw.state}: lit ${c.raw.x}%, menstrual ${c.raw.y}%`}}},
      scales:{x:{title:{display:true,text:"Female literacy (%)"},grid:{color:"#eef3f1"}},
              y:{title:{display:true,text:"Menstrual-hygiene use (%)"},grid:{color:"#eef3f1"}}}}});
  // donut
  const ts=DATA.tier_summary;
  new Chart(document.getElementById("donut"),{type:"doughnut",
    data:{labels:ts.map(t=>TIERKEY(t.tier)),datasets:[{data:ts.map(t=>t.n),
      backgroundColor:ts.map(t=>tierColor[TIERKEY(t.tier)])}]},
    options:{cutout:"62%",plugins:{legend:{position:"bottom",labels:{boxWidth:12,font:{size:11}}}}}});
  document.getElementById("tierStats").innerHTML=ts.map(t=>
    `<div style="display:flex;justify-content:space-between;font-size:12.5px;padding:3px 0;border-bottom:1px solid var(--line)">
      <span><span class="dot" style="background:${tierColor[TIERKEY(t.tier)]}"></span>${TIERKEY(t.tier)} (${t.n})</span>
      <span class="note">avg need ${t.avg_need} · menstrual ${t.avg_menstrual}%</span></div>`).join("");
  // models
  const mr=DATA.model_results, names=Object.keys(mr);
  new Chart(document.getElementById("models"),{type:"bar",
    data:{labels:names,datasets:[{label:"R² (higher = better)",data:names.map(n=>mr[n].r2),
      backgroundColor:names.map(n=>n==DATA.meta.best_model?"#0d8a72":"#a9d2c8")}]},
    options:{plugins:{legend:{display:false},tooltip:{callbacks:{afterLabel:c=>
      `RMSE ${mr[c.label].rmse} · MAE ${mr[c.label].mae}`}}},
      scales:{y:{beginAtZero:true,max:1,title:{display:true,text:"R²"}}}}});
  // drivers (shown as correlation with the target — intuitive; model weight in tooltip)
  const dr=[...DATA.drivers].sort((a,b)=>Math.abs(b.corr)-Math.abs(a.corr));
  new Chart(document.getElementById("drivers"),{type:"bar",
    data:{labels:dr.map(d=>SHORT[d.feature]),datasets:[{data:dr.map(d=>d.corr),
      backgroundColor:dr.map(d=>d.corr>=0?"#2fa37a":"#e0564f")}]},
    options:{indexAxis:"y",plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>
      `correlation ${c.raw>=0?"+":""}${c.raw} · model weight ${dr[c.dataIndex].coef}`}}},
      scales:{x:{min:-1,max:1,title:{display:true,text:"← lower access   correlation   higher access →"},grid:{color:"#eef3f1"}}}}});
}

/* ---------- narrative text ---------- */
function narrative(){
  const top=[...DATA.districts].sort((a,b)=>b.need_index-a.need_index).slice(0,3)
    .map(d=>d.district).join(", ");
  document.getElementById("useTop").innerHTML=
    `The model's highest-need districts right now are <b>${top}</b>. Start outreach in the High-priority tier and expand outward.`;
  const gaps=[...DATA.districts].sort((a,b)=>a.residual-b.residual).slice(0,3)
    .map(d=>`${d.district} (${d.residual})`).join(", ");
  document.getElementById("useGap").innerHTML=
    `Districts under-performing their predicted menstrual-hygiene level — <b>${gaps}</b> — likely face an
     access/awareness gap that pad distribution + workshops can close fast.`;
}

renderKPIs(); renderSliders(); setupTableUI(); recompute(); charts(); narrative();
</script>
</body>
</html>"""

out = HTML.replace("__DATA__", json.dumps(results))
open("index.html","w",encoding="utf-8").write(out)
print("Wrote index.html (",len(out),"bytes )")
