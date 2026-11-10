import sys, json, csv
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

d = sys.argv[1]; I = d + '/img/'
ml = json.load(open(d + '/ml.json')); pr = json.load(open(d + '/prox.json'))
NAVY = RGBColor(0x0b, 0x23, 0x40); BLUE = RGBColor(0x2e, 0x86, 0xab); GREY = RGBColor(0x33, 0x33, 0x33)
LIGHT = RGBColor(0xee, 0xf3, 0xf8); WHITE = RGBColor(255, 255, 255); PALE = RGBColor(0x9f, 0xc5, 0xe8)
p = Presentation(); p.slide_width = Inches(13.333); p.slide_height = Inches(7.5); B = p.slide_layouts[6]


def txt(s, x, y, w, h, lines, size=18, color=GREY, bold=False, align=None, font='Calibri'):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame; tf.word_wrap = True
    for i, l in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = para.add_run(); r.text = l
        r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
        para.space_after = Pt(6)
        if align: para.alignment = align


def slide(title, notes, sec=None):
    s = p.slides.add_slide(B)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, p.slide_width, Inches(1.0))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    txt(s, 0.5, 0.15, 10.0, 0.75, [title], 28, WHITE, True)
    if sec: txt(s, 10.3, 0.3, 2.8, 0.5, [sec], 12, PALE, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    txt(s, 0.5, 7.05, 6, 0.35, ['IBM Applied Data Science Capstone · SpaceX Falcon 9'], 10, RGBColor(0x88, 0x88, 0x88))
    return s


def bullets(s, items, x=0.5, y=1.3, w=12.3, h=5.6, size=18):
    txt(s, x, y, w, h, [('      – ' + i.strip()) if i.startswith('  ') else ('• ' + i) for i in items], size)


def img(s, f, x, y, w=None, h=None):
    s.shapes.add_picture(I + f, Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)


def flow(s, steps, y=1.4, x0=0.5, w=12.3):
    n = len(steps); bw = (w - 0.35 * (n - 1)) / n
    for i, t in enumerate(steps):
        x = x0 + i * (bw + 0.35)
        b = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(bw), Inches(1.3))
        b.fill.solid(); b.fill.fore_color.rgb = BLUE if i % 2 == 0 else NAVY; b.line.fill.background()
        tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pa = tf.paragraphs[0]; pa.alignment = PP_ALIGN.CENTER
        r = pa.add_run(); r.text = t; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = WHITE
        if i < n - 1:
            a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + bw + 0.04), Inches(y + 0.5), Inches(0.27), Inches(0.3))
            a.fill.solid(); a.fill.fore_color.rgb = GREY; a.line.fill.background()


def code(s, q, x, y, w, h):
    b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    b.fill.solid(); b.fill.fore_color.rgb = LIGHT; b.line.color.rgb = RGBColor(0xcc, 0xcc, 0xcc)
    tf = b.text_frame; tf.word_wrap = True; tf.margin_left = Inches(0.2); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, l in enumerate(q.split('\n')):
        pa = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); pa.alignment = PP_ALIGN.LEFT
        r = pa.add_run(); r.text = l; r.font.name = 'Consolas'; r.font.size = Pt(15); r.font.color.rgb = NAVY


def table(s, rows, x, y, w, colw=None, size=14):
    t = s.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(0.4 * len(rows))).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = t.cell(i, j); c.text = str(v); run = c.text_frame.paragraphs[0].runs[0]
            run.font.size = Pt(size); run.font.bold = (i == 0)
            if i == 0: c.fill.solid(); c.fill.fore_color.rgb = NAVY; run.font.color.rgb = WHITE
    if colw:
        for j, cw in enumerate(colw): t.columns[j].width = Inches(cw)


def dark(title, sub, notes=''):
    s = p.slides.add_slide(B)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, p.slide_width, p.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
    txt(s, 0.8, 2.6, 11.5, 1.2, [title], 40, WHITE, True); txt(s, 0.8, 3.8, 11.5, 1, [sub], 20, PALE)
    s.notes_slide.notes_text_frame.text = notes
    return s


def result(title, f, pts, notes, sec):
    s = slide(title, notes, sec); img(s, f, 0.4, 1.3, w=8.3); bullets(s, pts, 8.9, 1.35, 4.1, 5.5, 16)


def sql(title, q, pts, notes):
    s = slide(title, notes, 'SQL results'); h = 0.5 + 0.35 * q.count('\n')
    code(s, q, 0.5, 1.35, 12.3, h); bullets(s, pts, 0.5, 1.6 + h, 12.3, 3.6, 20); return s


# 1 Title
s = dark('Data Science Capstone Project Report', 'Predicting SpaceX Falcon 9 First-Stage Landing Success',
         'Good day. This is my IBM Applied Data Science Capstone. I predict whether a Falcon 9 first stage will land successfully, because that drives the cost of a launch.')
txt(s, 0.8, 5.0, 11.5, 1.6, ['Luqman Syahrulnizam  ·  10 November 2026', 'GitHub: https://github.com/Downey112/ibm-ds-capstone-spacex'], 18, WHITE)

s = slide('Outline', 'I will go from the problem, through how I collected and prepared the data, to what the analysis and models found.')
bullets(s, ['Executive Summary', 'Introduction', 'Methodology', 'Results', '  Exploratory data analysis (visualisation and SQL)',
            '  Interactive analytics (Folium map, Plotly Dash)', '  Predictive analysis (classification)', 'Conclusion', 'Appendix'], size=22)

s = slide('Executive Summary', 'I combined API and scraped data on 90 Falcon 9 launches. Landing success improved sharply over time. All four tuned models predict the outcome with 83% accuracy on held-out data; their main weakness is being too optimistic about failed landings.')
bullets(s, ['Methods: SpaceX REST API + Wikipedia web scraping → data wrangling → EDA with charts and SQL → Folium map + Plotly Dash → 4 classifiers tuned with GridSearchCV',
            'Data: 90 Falcon 9 launches (Falcon 1 removed); overall landing success 66.7% (60/90)',
            'Trend: landing success rose from 0% (2010–2013) to 90% (2019) and 84% (2020)',
            'Drivers: flight experience, orbit type, launch site and booster version',
            'Models: Logistic Regression, SVM, Decision Tree and KNN all reach 83.3% test accuracy (15/18); Decision Tree has the best cross-validation score (86.3%)',
            'Main error type: false positives (predicting a landing that failed)'], size=19)

s = slide('Introduction', "Reusing the first stage is SpaceX's cost advantage. Predicting the landing therefore tells us the likely launch price, which is what an alternative launch company bidding against SpaceX would want to know.")
bullets(s, ['Background: SpaceX advertises Falcon 9 launches at ~$62 million; other providers charge upward of $165 million. Much of the saving comes from reusing the first stage.',
            'Why it matters: if we can predict whether the first stage will land, we can estimate the cost of a launch. That helps a competitor bidding against SpaceX.',
            'Problem: can mission features (payload mass, orbit, launch site, flight number, booster details) predict a successful first-stage landing?',
            'Questions:', '  Which factors drive landing success?', '  Which sites and orbits have the best record?', '  Which classification model predicts best?'], size=20)

dark('Methodology', 'Data collection · wrangling · EDA · interactive analytics · predictive analysis')

s = slide('Methodology Overview', 'The project follows the standard data science pipeline, from collection through to modelling.', 'Methodology')
flow(s, ['Data collection\nSpaceX API + web scraping', 'Data wrangling\nclean, label, encode', 'EDA\nvisualisation + SQL', 'Interactive analytics\nFolium + Plotly Dash', 'Predictive analysis\n4 tuned classifiers'], y=1.5)
bullets(s, ['Data collection: SpaceX REST API v4 and BeautifulSoup scraping of Wikipedia', 'Data wrangling: filtering, missing values, binary Class label, one-hot encoding',
            'EDA: Matplotlib/Seaborn charts and SQL queries in SQLite', 'Interactive visual analytics: Folium map and Plotly Dash dashboard',
            'Predictive analysis: StandardScaler → train/test split → GridSearchCV (LR, SVM, Decision Tree, KNN) → evaluate'], 0.5, 3.2, 12.3, 3.6, 18)

s = slide('Data Collection – SpaceX API', 'The API gives IDs rather than names, so I made extra calls to get booster, site, payload and landing details. After filtering out Falcon 1, 90 Falcon 9 launches remained.', 'Methodology')
flow(s, ['GET /v4/launches/past', 'json_normalize → DataFrame', 'ID lookups: rockets, launchpads, payloads, cores', 'Filter: 1 core, 1 payload, date ≤ 2020-11-13', 'Remove Falcon 1 → 90 launches', 'Impute PayloadMass (mean) → CSV'], y=1.5)
bullets(s, ['Request: requests.get("https://api.spacexdata.com/v4/launches/past") → response.json()',
            'Helper functions turn IDs into BoosterVersion, LaunchSite + coordinates, PayloadMass + Orbit, and core details (Outcome, Flights, GridFins, Reused, Legs, LandingPad, Block, Serial)',
            'Missing PayloadMass replaced with the mean; LandingPad keeps None (26 rows) to mean "no landing pad used"'], 0.5, 3.2, 12.3, 3.6, 18)

s = slide('Data Collection – Web Scraping', 'I scraped a fixed revision of the Wikipedia page so the results are reproducible. The launch tables were parsed into a DataFrame as a second data source.', 'Methodology')
flow(s, ['requests.get(URL)\noldid=1027686922', 'BeautifulSoup\n(html)', 'soup.find_all\n("table")', 'Column names from <th>', 'Parse each row → dict', 'pd.DataFrame → CSV'], y=1.5)
bullets(s, ['Page: "List of Falcon 9 and Falcon Heavy launches"; soup.title = List of Falcon 9 and Falcon Heavy launches - Wikipedia',
            'Third table = launch records; header cells cleaned with extract_column_from_header()',
            'Columns: Flight No., Date, Time, Version Booster, Launch site, Payload, Payload mass, Orbit, Customer, Launch outcome, Booster landing'], 0.5, 3.2, 12.3, 3.6, 18)

s = slide('Data Wrangling', 'The raw outcome mixes landing type with success or failure. I turned it into one binary label, then one-hot encoded the categorical columns for the models.', 'Methodology')
bullets(s, ['Launches per site: CCAFS SLC 40 = 55 · KSC LC 39A = 22 · VAFB SLC 4E = 13',
            'Orbits: GTO 27 · ISS 21 · VLEO 14 · PO 9 · LEO 7 · SSO 5 · MEO 3 · ES-L1, HEO, SO, GEO 1 each',
            'Class label: 1 = landed (True ASDS / True RTLS / True Ocean), 0 = otherwise → 60 vs 30 → 66.7% success',
            'One-hot encoding of Orbit, LaunchSite, LandingPad, Serial → 83 features, cast to float64'], 0.5, 1.3, 6.8, 5.6, 18)
table(s, [['Outcome', 'Count', 'Class'], ['True ASDS', '41', '1'], ['None None', '19', '0'], ['True RTLS', '14', '1'], ['False ASDS', '6', '0'],
          ['True Ocean', '5', '1'], ['False Ocean', '2', '0'], ['None ASDS', '2', '0'], ['False RTLS', '1', '0']], 7.7, 1.4, 5.1, [2.5, 1.3, 1.3], 15)

s = slide('EDA with Data Visualization', 'Scatter plots show how two features together relate to the outcome. The bar chart compares orbits, and the line chart shows the improvement over time.', 'Methodology')
bullets(s, ['Scatter plots, coloured by landing outcome (Class), to see how two variables together relate to success:',
            '  Flight Number vs Launch Site · Payload Mass vs Launch Site', '  Flight Number vs Orbit · Payload Mass vs Orbit · Flight Number vs Payload',
            'Bar chart: success rate by orbit, to compare categories', 'Line chart: yearly success rate, to show the trend over time',
            'Outcome: these patterns informed which features to keep for modelling'], size=20)

s = slide('EDA with SQL', 'SQL was used for exact counts, totals and rankings. The SQL table has 101 rows and slightly different site names from the 90-row modelling dataset.', 'Methodology')
bullets(s, ['Loaded Spacex.csv into SQLite (table SPACEXTBL, 101 rows) and queried with %sql', 'Unique launch site names · 5 records where the site begins with "CCA"',
            'Total payload for NASA (CRS) · Average payload for booster F9 v1.1', 'Date of the first successful ground-pad landing',
            'Boosters with a drone-ship success and payload 4,000–6,000 kg', 'Count of successful vs failed mission outcomes',
            'Boosters that carried the maximum payload (subquery)', '2015 drone-ship landing failures (month, booster, site)',
            'Ranking of landing outcomes between 2010-06-04 and 2017-03-20'], size=19)

s = slide('Interactive Map with Folium', 'The map adds geography: where the sites are, how each site performed, and what infrastructure is nearby.', 'Methodology')
bullets(s, ['folium.Circle + label marker for each of the 4 launch sites (coordinates from the dataset)', 'MarkerCluster of every launch: green = landed (Class 1), red = failed (Class 0)',
            'MousePosition to read coordinates of nearby features', 'Haversine distance + PolyLine from a launch site to the nearest coastline, railway, highway and city',
            'Purpose: are sites near the equator and the coast? Are they close to transport links but far from cities?'], size=20)

s = slide('Dashboard with Plotly Dash', 'The dashboard lets anyone filter by site and payload, and the charts update instantly through callbacks.', 'Methodology')
bullets(s, ['Dropdown: All Sites or a single launch site', 'Pie chart: share of successes by site (All Sites), or success vs failure for the selected site',
            'RangeSlider: payload mass 0–10,000 kg', 'Scatter plot: payload vs outcome, coloured by booster version category', 'Two callbacks link the inputs to the charts',
            'Purpose: explore how site, payload and booster version affect success interactively'], size=20)

s = slide('Predictive Analysis (Classification)', 'Each model was tuned with 10-fold cross-validation on the training data, then scored on the same 18-launch test set.', 'Methodology')
flow(s, ['X = 83 features\nY = Class', 'StandardScaler', 'train_test_split\n80/20, random_state=2', 'GridSearchCV cv=10\nLR · SVM · Tree · KNN', 'Test accuracy +\nconfusion matrix', 'Pick best model'], y=1.5)
bullets(s, ['72 training and 18 test launches', 'Logistic Regression: C, penalty, solver · SVM: kernel, C, gamma',
            'Decision Tree: criterion, splitter, max_depth, max_features, min_samples_leaf/split · KNN: n_neighbors, algorithm, p',
            'Compare best CV score, test accuracy and confusion matrix'], 0.5, 3.2, 12.3, 3.6, 18)

dark('Results', 'Exploratory data analysis · SQL · interactive analytics · predictive analysis')

result('Flight Number vs Launch Site', 'flight_site.png', ['Most early flights launched from CCAFS SLC 40, which also has the most failures', 'VAFB SLC 4E was used from flight 4 to 66; KSC LC 39A from flight 27', 'Success rises with flight number at every site', 'Experience is a strong predictor'],
       'Most early launches, and most failures, came from CCAFS SLC 40. As the flight count grows, landings become far more reliable everywhere.', 'EDA results')
result('Payload vs Launch Site', 'payload_site.png', ['CCAFS SLC 40: 350–15,600 kg', 'KSC LC 39A: 2,490–15,600 kg', 'VAFB SLC 4E: no launches above 10,000 kg (max 9,600 kg)', 'Heavy payloads (>10,000 kg) mostly landed'],
       'VAFB handles only lighter payloads, while the Florida sites take the heaviest missions, which mostly landed.', 'EDA results')
result('Success Rate by Orbit Type', 'orbit_rate.png', ['100%: ES-L1, GEO, HEO (1 launch each), SSO (5/5)', 'VLEO 85.7% · LEO 71.4% · PO 66.7% · MEO 66.7% · ISS 61.9%', 'GTO lowest of the common orbits: 51.9% of 27', 'SO 0% (1 launch)', 'Orbits with 1 launch say little'],
       'SSO and VLEO are reliable with a meaningful number of launches. GTO, the most common orbit, is close to a coin flip. The 100% orbits with one launch tell us little.', 'EDA results')
result('Flight Number vs Orbit Type', 'flight_orbit.png', ['Early flights: LEO, ISS and GTO', 'VLEO (Starlink) appears from flight 65 and mostly lands', 'LEO: success appears related to flight number', 'GTO: no clear relationship with flight number'],
       'The mission mix shifted toward VLEO, which lands reliably, so part of the later success comes from what was being launched.', 'EDA results')
result('Payload vs Orbit Type', 'payload_orbit.png', ['Payloads above 10,000 kg: almost all VLEO (plus one ISS at 12,259 kg)', 'Heavy payloads land more often for PO, LEO and ISS', 'GTO (3,000–7,076 kg): mixed, no clear pattern', 'SSO ≤ 4,000 kg, all landed'],
       'Heavy payload alone does not mean failure. For GTO, payload mass does not separate successes from failures.', 'EDA results')
result('Launch Success Yearly Trend', 'yearly.png', ['2010–2013: 0%', '2014–2015: 33%', '2016: 62% · 2017: 83%', '2018: 61% (a dip)', '2019: 90% · 2020: 84%', 'Clear upward trend since 2013'],
       'Success rose steadily from 2013, with one dip in 2018, and reached 84 to 90 percent in 2019 and 2020.', 'EDA results')

s = slide('All Launch Site Names', 'There are four distinct site names. Cape Canaveral appears under two names.', 'SQL results')
code(s, 'SELECT DISTINCT Launch_Site FROM SPACEXTBL;', 0.5, 1.35, 12.3, 0.8)
table(s, [['Launch_Site', 'Launches in table'], ['CCAFS LC-40', '26'], ['CCAFS SLC-40', '34'], ['KSC LC-39A', '25'], ['VAFB SLC-4E', '16']], 0.5, 2.5, 7, [4, 3], 18)

s = slide("Launch Sites Beginning with 'CCA'", "LIKE 'CCA%' filters all Cape Canaveral records. The first five are the earliest Falcon 9 flights.", 'SQL results')
code(s, "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;", 0.5, 1.35, 12.3, 0.8)
rows = list(csv.DictReader(open(d + '/sql.csv')))[:5]
table(s, [['Date', 'Booster', 'Site', 'Payload', 'kg', 'Orbit', 'Customer', 'Landing']] +
      [[r['Date'], ' '.join(r['Booster_Version'].split()), r['Launch_Site'], r['Payload'][:34], r['PAYLOAD_MASS__KG_'], r['Orbit'], r['Customer'], r['Landing_Outcome']] for r in rows],
      0.3, 2.5, 12.7, [1.3, 1.5, 1.4, 3.0, 0.7, 1.1, 1.6, 2.1], 11)

sql('Total Payload Mass – NASA (CRS)', "SELECT SUM(PAYLOAD_MASS__KG_) AS total_payload\nFROM SPACEXTBL WHERE Customer = 'NASA (CRS)';",
    ['Result: 45,596 kg', "Total payload carried for NASA's Commercial Resupply Services missions"], 'NASA resupply missions carried 45,596 kg in total.')
sql('Average Payload Mass – F9 v1.1', "SELECT AVG(PAYLOAD_MASS__KG_) AS avg_payload\nFROM SPACEXTBL WHERE Booster_Version = 'F9 v1.1';",
    ['Result: 2,928.4 kg', 'Average payload for the F9 v1.1 booster version'], 'The F9 v1.1 booster carried 2,928.4 kg on average.')
sql('First Successful Ground-Pad Landing', "SELECT MIN(Date) AS first_success\nFROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';",
    ['Result: 2015-12-22', 'Orbcomm OG2 mission from CCAFS LC-40'], 'The first successful ground-pad landing was on 22 December 2015.')
sql('Drone-Ship Success with Payload 4,000–6,000 kg', "SELECT Booster_Version FROM SPACEXTBL\nWHERE Landing_Outcome = 'Success (drone ship)'\n  AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;",
    ['F9 FT B1022 · F9 FT B1026 · F9 FT B1021.2 · F9 FT B1031.2', 'All four are Full Thrust boosters; two are re-flown cores (.2)'], 'All four boosters are Full Thrust versions, two of them re-flown cores.')
sql('Total Successful and Failed Mission Outcomes', "SELECT Mission_Outcome, COUNT(*) AS total\nFROM SPACEXTBL GROUP BY Mission_Outcome;",
    ['Success: 98 · "Success " (trailing space in source): 1 · Success (payload status unclear): 1 · Failure (in flight): 1', '→ 100 successful missions, 1 failure', 'Mission success is near-perfect; landing the booster is the harder problem'],
    'Mission success, meaning the payload reached orbit, is nearly perfect. Landing the booster is the harder problem.')
sql('Boosters Carrying the Maximum Payload', "SELECT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ =\n  (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);",
    ['Maximum payload: 15,600 kg', 'F9 B5 B1048.4 · B1049.4 · B1051.3 · B1056.4 · B1048.5 · B1051.4', 'F9 B5 B1049.5 · B1060.2 · B1058.3 · B1051.6 · B1060.3 · B1049.7', 'Only Block 5 boosters, mostly re-flown, carried the maximum payload'],
    'Only Block 5 boosters, many of them re-flown, carried the maximum payload.')
s = sql('2015 Drone-Ship Landing Failures', "SELECT substr(Date,6,2) AS month, Landing_Outcome, Booster_Version, Launch_Site\nFROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)'\n  AND substr(Date,1,4) = '2015';",
        [], 'Both 2015 drone-ship failures were v1.1 boosters launched from CCAFS LC-40.')
table(s, [['Month', 'Landing outcome', 'Booster', 'Launch site'], ['01 (January)', 'Failure (drone ship)', 'F9 v1.1 B1012', 'CCAFS LC-40'], ['04 (April)', 'Failure (drone ship)', 'F9 v1.1 B1015', 'CCAFS LC-40']], 0.5, 3.3, 12.3, None, 18)
s = slide('Landing Outcomes Ranked (2010-06-04 to 2017-03-20)', 'In the early years, no attempt was the most common outcome. Drone-ship successes and failures were level at 5 each.', 'SQL results')
code(s, "SELECT Landing_Outcome, COUNT(*) AS n FROM SPACEXTBL\nWHERE Date BETWEEN '2010-06-04' AND '2017-03-20'\nGROUP BY Landing_Outcome ORDER BY n DESC;", 0.5, 1.35, 7.2, 1.6)
table(s, [['Rank', 'Landing outcome', 'Count'], ['1', 'No attempt', '10'], ['2', 'Success (drone ship)', '5'], ['3', 'Failure (drone ship)', '5'], ['4', 'Success (ground pad)', '3'],
          ['5', 'Controlled (ocean)', '3'], ['6', 'Uncontrolled (ocean)', '2'], ['7', 'Failure (parachute)', '2'], ['8', 'Precluded (drone ship)', '1']], 8.0, 1.35, 4.9, [0.8, 3.1, 1.0], 14)

dark('Launch Site Proximity Analysis', 'Folium interactive map')


def mapslide(t, f, pts, n):
    s = slide(t, n, 'Folium results'); img(s, f, 0.4, 1.3, w=9.0); bullets(s, pts, 9.6, 1.3, 3.5, 5.6, 15)


mapslide('All Launch Sites on a Map', 'map_all.png', ['3 sites in Florida (CCAFS LC-40, CCAFS SLC-40, KSC LC-39A), 1 in California (VAFB SLC-4E)', 'All sites are on the coast, so rockets fly over the ocean',
                                                  'All are in the far south of the US (Florida ≈ 28.5° N), as close to the equator as the mainland allows'],
         "Sites sit by the coast so rockets fly over water. They are in the south because launching closer to the equator gives extra speed from Earth's rotation.")
mapslide('Colour-Labelled Launch Outcomes', 'map_ksc.png', ['Each launch is a marker: green = landed, red = failed', 'KSC LC-39A (shown): 10 of 13 landed, the best record of any site',
                                                            'CCAFS LC-40: 7 of 26 landed (many early flights)', 'VAFB SLC-4E: 4 of 10 · CCAFS SLC-40: 3 of 7'],
         'The colour markers show at a glance which sites have the best landing record. KSC LC-39A is mostly green.')
mapslide('Distances to Coastline, Railway, Highway and City', 'map_prox.png', ['From CCAFS SLC-40:', f"  Coastline: {pr['coast'][0]:.2f} km", f"  Railway: {pr['rail'][0]:.2f} km (rail line runs to the pad)",
                                                                              f"  Highway (NASA Pkwy East): {pr['road'][0]:.2f} km", f"  Nearest city (Titusville): {pr['city:city'][0]:.2f} km",
                                                                              'Close to coast, rail and road (logistics); far from cities (safety)'],
         'Sites are close to transport links for moving hardware, but kept away from cities for safety.')

dark('Build a Dashboard with Plotly Dash', 'Interactive dashboard results')
s = slide('Launch Success Count for All Sites', 'KSC LC-39A accounts for the largest share of successful landings.', 'Dash results'); img(s, 'dash_pie_all.png', 0.6, 1.25, h=5.6)
bullets(s, ['KSC LC-39A: 41.7% of all successful launches', 'CCAFS LC-40: 29.2%', 'VAFB SLC-4E: 16.7%', 'CCAFS SLC-40: 12.5%', 'KSC LC-39A leads the success count'], 7.6, 1.6, 5.3, 5, 19)
s = slide('Launch Site with the Highest Success Ratio', 'Selecting KSC LC-39A shows about 77% of its launches landed successfully, the best of all sites.', 'Dash results'); img(s, 'dash_pie_ksc.png', 0.6, 1.25, h=5.6)
bullets(s, ['KSC LC-39A: 76.9% success (10 of 13)', '23.1% failure (3 of 13)', 'The highest success ratio of any site'], 7.6, 1.6, 5.3, 5, 19)
result('Payload vs Launch Outcome (All Sites)', 'dash_scatter.png', ['Success by booster: v1.0 0% (0/5) · v1.1 7% (1/15) · FT 67% (16/24) · B4 55% (6/11) · B5 100% (1/1)',
                                                                    'Success by payload: 0–2k kg 23% · 2–4k kg 62% · 4–6k kg 38% · 6–10k kg 33%', 'FT has the best rate among well-used boosters; 2,000–4,000 kg is the best payload range'],
       'Newer boosters land far more often. Payloads of 2,000 to 4,000 kg have the best record in this dashboard dataset.', 'Dash results')

dark('Predictive Analysis (Classification)', 'Model results')
s = slide('Classification Accuracy', 'All four models score 83.3% on the 18-launch test set. Decision Tree has the best cross-validation score, so I select it as the best model, with the caveat that differences are within noise for such a small test set.', 'ML results')
img(s, 'ml_acc.png', 0.4, 1.3, w=7.6)
table(s, [['Model', 'Best CV', 'Test']] + [[k, f"{int(v['cv']*1000+0.5)/10:.1f}%", f"{v['test'] * 100:.1f}%"] for k, v in ml.items()], 8.3, 1.4, 4.6, [2.4, 1.1, 1.1], 15)
bullets(s, ['All four tie on test accuracy (15/18)', 'Best model: Decision Tree, with the highest CV score (86.3%)', 'With 18 test launches, one prediction = 5.6 points, so the models are effectively equal'], 8.3, 3.7, 4.7, 3.2, 15)
s = slide('Confusion Matrix', 'The model never misses a landing, but half the failures are predicted as landings. For a bidder, that means sometimes expecting a cheaper launch than reality. All four models produce this same matrix on the test set.', 'ML results')
img(s, 'cm.png', 0.6, 1.25, h=5.6)
bullets(s, ['All four models give the same matrix on the test set', '12 landings correctly predicted, 0 missed (recall 100%)', '3 failures correctly predicted',
            '3 failures wrongly predicted as landings (false positives)', 'The model is optimistic: false positives are the main weakness'], 7.6, 1.5, 5.3, 5.4, 18)

s = slide('Conclusions', "Experience, orbit, site and booster version drive landing success, and a simple model captures this at 83% accuracy. A bidder can use it to estimate SpaceX's likely launch cost, while staying cautious about over-optimistic predictions.")
bullets(s, ['Landing success follows a learning curve: 0% (2010–13) → 84–90% (2019–20)', 'KSC LC-39A has the highest success rate (76.9%); newer boosters (FT, B5) land far more often',
            'Orbit matters: SSO and VLEO are reliable, GTO is about 50/50', 'Tuned classifiers reach 83.3% test accuracy; Decision Tree is selected (best CV score, 86.3%)',
            'Insight for a competitor: recent, non-GTO missions on newer boosters → expect a reused (cheaper) first stage. Treat landing predictions for GTO cautiously because of false positives.',
            'Next steps: post-2020 launches, a larger test set, and features such as booster reuse count and weather'], size=19)

s = slide('Appendix', 'All code is on GitHub. The three datasets differ in size, which is why some percentages differ between slides.')
bullets(s, ['GitHub repository: https://github.com/Downey112/ibm-ds-capstone-spacex', '  Notebooks: SpaceX API, web scraping, data wrangling, EDA visualisation, EDA SQL, Folium map, Plotly Dash app (.py), ML prediction',
            'Datasets: modelling dataset 90 rows · SQL table 101 rows · Dash dataset 56 rows', 'Best hyperparameters:'] +
        ['  ' + k + ': ' + ', '.join(f'{a}={(round(b, 4) if isinstance(b, float) else b)}' for a, b in v['params'].items()) for k, v in ml.items()] +
        ['Proximity distances: OpenStreetMap features + haversine formula'], size=17)

p.save(d + '/Data Science Capstone Project Report.pptx'); print(len(p.slides), 'slides')
