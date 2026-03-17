# ShipmentSure — Predicting On-Time Delivery Using Supplier Data
### Branch: ShipmentSure-Rahel-Benjamin

> Can we predict whether a shipment will arrive on time — before it even leaves the warehouse?  
> This project explores that question using real supplier data, step by step.

---

## What This Branch Contains

| Folder | Contents |
|---|---|
| `Notebook/` | All analysis and model notebooks |
| `data/` | Raw dataset (`Train.csv`) |

---

## The Dataset at a Glance

- **Source:** `data/Train.csv`
- **Size:** 10,999 shipments × 12 features
- **Target:** `Reached.on.Time_Y.N` → 1 = Delayed, 0 = On Time

**Features include:** warehouse block, shipment mode, customer care calls, customer rating, product cost, prior purchases, product importance, gender, discount offered, and weight.

---

## Notebook Walkthrough

### `EDA.ipynb` — Getting to Know the Data
Before building any model, it helps to simply look at the data. This notebook examines the shape and structure of the dataset, checks for missing values and duplicates, studies how features are distributed, and begins to ask: *which factors seem to influence delivery timing?*

### `Categorical Encoding.ipynb` — Turning Words into Numbers
Machine learning models only understand numbers. This notebook converts text-based columns like `Mode_of_Shipment` (Ship/Flight/Road) and `Product_importance` (Low/Medium/High) into numeric form using one-hot encoding and ordinal encoding, depending on whether the category has a natural order.

### `Cyclic Encoding and Discretization.ipynb` — Smarter Encoding
Standard encoding misses certain patterns — for example, features that wrap around (like hours or months). This notebook uses sine and cosine transforms to handle circular features correctly. It also discretizes continuous values like `Cost_of_the_Product` into meaningful bins (Low / Medium / High / Premium) using equal-width, equal-frequency, and KBins approaches.

### `Data Visualization.ipynb` — Seeing the Patterns
Numbers alone rarely tell the full story. This notebook builds scatter plots, box plots, histograms, heatmaps, and count plots to visualize relationships between features and the delivery outcome. Key finding: higher discounts are strongly associated with on-time deliveries.

### `OLAP.ipynb` — Exploring from Different Angles
OLAP (Online Analytical Processing) lets us look at the data from multiple dimensions at once. Using slice, dice, roll-up, drill-down, and pivot operations, this notebook answers business questions like: *Which warehouse has the best delivery record?* and *Does shipment mode interact with product importance to affect delays?*

### `KMeans Clustering (ANOVA).ipynb` — Grouping Shipments by Similarity
This notebook uses KMeans clustering to group shipments into natural segments based on features like cost and weight. ANOVA (Analysis of Variance) is then applied to statistically validate whether the clusters are meaningfully different from each other — confirming that the groupings are not just random.

### `KMeans (LogTransform).ipynb` — Better Clusters with Log Transformation
Features like `Discount_offered` and `Cost_of_the_Product` are right-skewed, which can distort clustering results. This notebook first applies a log transformation (`np.log1p`) to reduce skewness, then scales the data with StandardScaler before running KMeans. The result is cleaner, more balanced cluster separation, visualized using boxplots.

### `Logistic Regression & Random Forest.ipynb` — Comparing Classification Models
Two classification models are trained and compared side by side. Logistic Regression provides a simple linear baseline, while Random Forest builds an ensemble of decision trees for a more powerful prediction. The notebook evaluates both using accuracy, precision, recall, and confusion matrices — helping identify which model generalizes better to unseen shipments.

### `FeatureUnion & TransformedTargetRegressor.ipynb` — Advanced Pipeline Design
This notebook demonstrates a production-style ML pipeline. `FeatureUnion` runs multiple feature transformation steps in parallel (e.g., PCA and SelectKBest simultaneously) and combines their outputs. `TransformedTargetRegressor` wraps the model to automatically apply log transformation to the target variable during training and reverse it during prediction — keeping the workflow clean and leak-free.

### `XGBoost.ipynb` — Building the Final Prediction Model
The final notebook brings everything together. After preprocessing and encoding, an XGBoost classifier is trained to predict whether a shipment will be delayed. Results include accuracy score, classification report, confusion matrix, and a feature importance chart showing which variables drive the prediction most.

**Model result:** ~67% accuracy with XGBoost (200 estimators, learning rate 0.05, max depth 6)

---

## Key Findings

- Shipments with **higher discounts** are significantly more likely to arrive on time
- **Lighter packages** (avg ~3,272g) tend to arrive on time vs heavier ones (avg ~4,168g) that are often delayed
- **Product importance** matters — High importance products show a better on-time rate than Low importance ones
- The `ID` column has zero predictive value and is excluded from all models
- Log-transforming skewed features before clustering produces noticeably better-separated groups

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/mailech/ShipmentSure-Predicting-On-Time-Delivery-Using-Supplier-Data.git

# 2. Switch to this branch
git checkout ShipmentSure-Rahel-Benjamin

# 3. Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn xgboost

# 4. Open Jupyter and navigate to Notebook/
jupyter notebook
```

> All notebooks load data using `pd.read_csv("../data/Train.csv")`

---

## Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Scikit-learn` · `XGBoost` · `Jupyter Notebook`

---

**Student:** Rahel Benjamin  
**Project:** ShipmentSure — Infosys Springboard  
**Last Updated:** March 2026
