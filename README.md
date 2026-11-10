# IBM Applied Data Science Capstone: SpaceX Falcon 9 Landing Prediction

Can we predict whether a Falcon 9 first stage will land successfully? SpaceX prices a launch at about $62M, against $165M+ elsewhere, largely because it reuses the first stage. So predicting the landing helps estimate what a launch will cost.

**Final presentation:** [`Data Science Capstone Project Report.pdf`](Data%20Science%20Capstone%20Project%20Report.pdf) (editable `.pptx` alongside it)

## Key results
- 90 Falcon 9 launches (after removing Falcon 1); overall landing success 66.7%
- Landing success went from 0% (2010–2013) to 90% (2019) and 84% (2020)
- KSC LC-39A has the best site record (76.9%); SSO and VLEO orbits are reliable, while GTO is about 50/50
- Logistic Regression, SVM, Decision Tree and KNN all reach **83.3% test accuracy** (15/18). Decision Tree has the best 10-fold CV score (86.3%). The main error type is false positives.

## Repository layout
| Path | Contents |
|---|---|
| `notebooks/` | IBM lab notebooks: API collection, web scraping, data wrangling, ML prediction |
| `src/` | Scripts that reproduce every number, chart and map in the deck |
| `data/` | IBM course datasets: `p2.csv` = dataset_part_2, `p3.csv` = dataset_part_3 (one-hot features), `sql.csv` = Spacex.csv (SQL table), `dash.csv` = spacex_launch_dash.csv |
| `outputs/charts/` | EDA, Dash and ML charts |
| `outputs/maps/` | Folium maps (HTML + screenshots) |
| `outputs/ml.json` | Best CV score, test accuracy, best parameters and confusion matrix for each model |
| `outputs/prox.json` | Distances from CCAFS SLC-40 to the nearest coastline, railway, highway and city (OpenStreetMap + haversine) |

## Reproduce
```bash
pip install pandas numpy scikit-learn matplotlib seaborn folium python-pptx requests
cd <folder containing data/ files and an img/ folder>
python src/summary_stats.py data            # wrangling / SQL / Dash summary numbers
python src/ml_models.py data                # GridSearchCV for LR, SVM, Decision Tree, KNN
python src/eda_dash_ml_charts.py data       # charts
python src/folium_outcomes_proximity.py data   # Folium maps
python src/build_deck.py data               # PowerPoint deck
```
The scripts expect the CSVs, `ml.json`, `prox.json` and an `img/` folder inside the folder you pass in.

## Methods
SpaceX REST API v4 + BeautifulSoup scraping of Wikipedia → pandas wrangling (Class label, one-hot encoding) → EDA with Matplotlib/Seaborn and SQLite → Folium map and Plotly Dash → GridSearchCV (cv=10) on LR, SVM, Decision Tree and KNN with an 80/20 split (`random_state=2`).
