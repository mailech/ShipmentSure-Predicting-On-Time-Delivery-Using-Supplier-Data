# ShipmentSure: Concepts Overview

ShipmentSure is a machine learning project that predicts on-time delivery using supplier data. Here's an overview of all the key concepts used in this project.

---

## 1. **Exploratory Data Analysis (EDA)**
EDA is about getting to know your data before doing anything complex. We look at distributions, patterns, and relationships to understand what we're working with. Charts, statistics, and simple questions like "What does this feature look like?" help us spot issues early.

## 2. **Full Dataset Study**
Before diving into individual techniques, we do a holistic study of the entire dataset. This includes inspecting data types, checking shape and structure, computing summary statistics (`.describe()`), identifying categorical vs. numeric columns, and profiling value distributions. It sets the foundation for every step that follows.

## 3. **OLAP Analysis**
OLAP is like looking at your data from different angles. You can drill down from "total deliveries" to "deliveries by warehouse" to "deliveries by each mode of shipment." It helps answer business questions like: "Which warehouse performs best?" or "Which shipping mode is most reliable?"

## 4. **Data Preprocessing**
This is preparation work. We clean our raw data, fix issues, transform it into the right format, and organize it so it's ready for machine learning. Good preprocessing = good models.

## 5. **Data Cleaning**
Real-world data is messy. We handle missing values, remove duplicates, fix inconsistencies, remove outliers, and correct invalid data.

## 6. **Handling Missing Values**
When data is missing, we have options:
- **Delete it**: Simple but loses information
- **Mean/Median fill (`SimpleImputer`)**: Quick and easy
- **KNN impute (`KNNImputer`)**: Use similar records to fill gaps (better)
- **MICE/Iterative (`IterativeImputer`)**: Fancy methods for complex patterns (best)

## 7. **Outlier Detection**
Some data points are weirdly different from others. We use **Isolation Forest** to spot these outliers. It's like finding the one person in a crowd who doesn't fit the pattern.

## 8. **Feature Scaling & Normalization**
Imagine comparing a person's height (180 cm) with their weight (80 kg). The numbers are on different scales! We use methods like:
- **Robust Scaling**: Perfect for data with outliers
- **Standardization (`StandardScaler`)**: Centers data to mean 0 and std 1, essential before clustering or PCA
- **Min-Max Scaling**: Bounds values 0–1
- **Quantile Transform**: Handles extreme values
- **Power Transform**: Fixes skewness mathematically

## 9. **Skewness Analysis**
Some data is lopsided (skewed). If cost data has a long tail on the right (most cheap, few expensive), that's positive skew. We transform skewed data to make distributions more balanced for better model performance.

## 10. **Feature Encoding**
Machines don't understand words like "Flight" or "Male". We convert categories to numbers:
- **One-Hot Encoding**: Create binary columns (1 if matches, 0 if not)
- **Ordinal Encoding**: Assign numbers if there's an order (low=0, medium=1, high=2)
- **Binary Encoding**: For simple two-value categories (M=1, F=0)

## 11. **Cyclic Encoding**
Some features are circular — hour 23 is close to hour 0, December is close to January. Standard encoding misses this! We use **sine and cosine transforms** to capture the circular nature:
- `sin_feature = sin(2π × value / period)`
- `cos_feature = cos(2π × value / period)`

This way, the model correctly understands that Rating 5 and Rating 1 can be neighbors on a cycle.

## 12. **Feature Hashing**
When a categorical feature has **many unique values** (high cardinality), one-hot encoding creates too many columns. **Feature Hashing** (the "hashing trick") maps categories into a fixed-size numeric vector using a hash function:
- Uses `FeatureHasher` from scikit-learn
- Controls output dimensionality (e.g., 6 columns instead of hundreds)
- Works for single or multi-column categorical combinations (e.g., `Mode_of_Shipment` + `Warehouse_block`)

Trade-off: some hash collisions can occur, but it's efficient and memory-friendly.

## 13. **Discretization (Binning)**
Sometimes converting continuous numbers into categories (bins) helps models find patterns. We use three approaches:
- **Equal-width binning (`pd.cut`)**: Divides the range into equal-sized intervals
- **Equal-frequency binning (`pd.qcut`)**: Each bin gets roughly the same number of data points
- **KBinsDiscretizer**: Scikit-learn's flexible binning with strategies like `uniform`, `quantile`, and `kmeans`

Example: Turning `Cost_of_the_Product` into "Low", "Medium", "High", "Premium" bins.

## 14. **Feature Generation & Engineering**
Creating **new features** from existing ones can dramatically improve models:

**Manual feature creation:**
- **Cost per gram**: `Cost_of_the_Product / (Weight_in_gms + 1)` — value density
- **Discount ratio**: `Discount_offered / (Cost_of_the_Product + 1)` — relative discount
- **Customer engagement**: `Customer_care_calls × Customer_rating` — interaction signal

**Automated feature creation:**
- **Polynomial Features (`PolynomialFeatures`)**: Automatically generates interaction terms (e.g., `Cost × Discount`) for non-linear relationships

## 15. **Data Transformation**
We transform features to improve them:
- **Quantile Transform**: Force uniform or normal distributions
- **Power Transform**: Fix skewness mathematically
- **Log Transform (`np.log1p`)**: Handle right-skewed data like costs and discounts
- **Polynomial Features**: Create new features for non-linear relationships

## 16. **KMeans Clustering**
KMeans is an **unsupervised learning** technique that groups data points into clusters based on similarity. We use it in two ways:

**For data exploration:**
- Segment products/shipments into natural groups (e.g., cluster by `Cost_of_the_Product` and `Weight_in_gms`)
- Profile each cluster using `.groupby('Cluster').mean()` and `.describe()`

**Combined with Log Transform:**
- Apply `np.log1p` to skewed features first to improve cluster separation
- Scale with `StandardScaler`, then run KMeans
- Visualize clusters with boxplots to interpret the groupings

Key parameters: `n_clusters=3`, `random_state=42`, `n_init=10`

## 17. **Feature Selection**
Not all features are useful. We identify and keep only the important ones using multiple approaches:

**SelectKBest (Univariate Selection):**
- Uses ANOVA F-test (`f_classif`) to score each feature against the target `Reached.on.Time_Y.N`
- Selects the top-k most statistically significant features (e.g., k=5)
- Quick, interpretable, and effective for classification tasks

**General benefits:**
- Speed up training
- Improve model accuracy
- Reduce complexity
- Make better predictions

## 18. **Dimensionality Reduction (PCA)**
Having many features can be overkill. **PCA** reduces dimensions while keeping important information. It's like summarizing a book without losing the plot!
- `StandardScaler()` before PCA (required)
- `PCA(n_components=2)` for 2D visualization
- `explained_variance_ratio_` shows how much information is retained

## 19. **FeatureUnion**
`FeatureUnion` combines **complementary feature views** into a single feature set:
- **PCA path**: captures variance-based structure
- **SelectKBest path**: captures label-signal-based features
- Both paths are run in parallel and their results concatenated

## 20. **Statistical Analysis**
We use correlations, mean/median values, and distribution tests to understand relationships between variables. Does customer rating affect delivery time? Statistics tell us!

## 21. **Data Visualization**
Pictures are worth 1000 words:
- **Histograms**: See distributions (before/after transforms)
- **Box Plots**: Spot outliers, compare groups and clusters
- **Scatter Plots**: Find relationships
- **Heatmaps**: Show correlations and OLAP summaries
- **KDE Plots**: Smooth distribution curves
- **Bar Charts**: Compare cluster profiles and feature scores
- **Count Plots**: Show category and bin distributions

## 22. **Pipeline Architecture**
We build a "recipe" that combines all our preprocessing steps:
1. Handle missing values (`SimpleImputer`)
2. Scale numeric features (`StandardScaler`)
3. Encode categories (`OneHotEncoder`)
4. Engineer new features (ratios, interactions)
5. Select best features (`SelectKBest` / PCA)
6. Feed into machine learning model

Same recipe for train and test data = consistent, reliable results.

---

## The Big Picture

All these concepts work together in a single journey:
1. **Study** your full dataset (profiling, structure, types)
2. **Explore** your data (EDA, OLAP analysis)
3. **Clean** it up (handle missing values, outliers, inconsistencies)
4. **Transform** it (log transform, scaling, cyclic encoding, discretization)
5. **Engineer** new features (ratios, interactions, polynomial features)
6. **Encode** categories (one-hot, feature hashing, ordinal)
7. **Cluster** for insight (KMeans on transformed data)
8. **Select** the best features (SelectKBest, PCA, FeatureUnion)
9. **Combine** everything in a pipeline
10. **Train** your machine learning model (Logistic Regression, Random Forest, XGBoost)
11. **Predict** on-time delivery!

---

## Notebook-Wise Concepts Summary

| Notebook | Key Methods |
|----------|-------------|
| `Data_Clean.ipynb` | `describe()`, `info()`, `isnull().sum()`, `corr()`, `sns.heatmap()`, `sns.boxplot()` |
| `EDA.ipynb` | `read_csv()`, `head()`, `describe()`, `sns.countplot()` |
| `Full_Dataset_Study.ipynb` | `shape`, `info()`, `skew()`, `value_counts()`, `groupby().agg()`, `plt.pie()` |
| `Data_Analysis.ipynb` | `groupby().mean()`, `pivot_table()`, `sns.scatterplot()`, `sns.barplot()` |
| `OLAP_Data_Analysis.ipynb` | Boolean filtering, `groupby().agg()`, `pivot_table()`, `sns.heatmap(annot=True)` |
| `Data_Skewness_Statistical_Analysis.ipynb` | `skew()`, `mean()`, `median()`, `sns.histplot(kde=True)`, `np.log1p()` |
| `Categorical_Encoding.ipynb` | Custom `RareLabelEncoder`, `OneHotEncoder`, `OrdinalEncoder` |
| `Cyclic_Encoding_And_Discretization.ipynb` | `np.sin()`, `np.cos()`, `pd.cut()`, `pd.qcut()`, `KBinsDiscretizer` |
| `Feature_Hashing_Generation.ipynb` | `FeatureHasher`, `PolynomialFeatures`, manual feature creation |
| `Feature_Selection_PCA.ipynb` | `SelectKBest(f_classif)`, `PCA(n_components=2)`, `RandomForestClassifier` |
| `KMeans_KBest_FeatureSelection.ipynb` | `StandardScaler`, `KMeans`, `SelectKBest` |
| `KMeans_LogTransform.ipynb` | `np.log1p()`, `KMeans(n_init=10)`, `sns.boxplot()` |
| `Data_Preprocessing.ipynb` | `KNNImputer`, `IterativeImputer`, `IsolationForest`, all scalers |
| `Data_Pipeline_Preprocessing.ipynb` | `Pipeline`, `ColumnTransformer`, saves `preprocessor.pkl` |
| `PreprocessingEngine_AnomalyDetection.ipynb` | Custom engine class, `IsolationForest` |
| `FeatureUnion_TargetTransform.ipynb` | `FeatureUnion` PCA + KBest, `TransformedTargetRegressor` |
| `LogisticRegression_RandomForest.ipynb` | `LogisticRegression`, `RandomForestClassifier`, `GridSearchCV`, metrics |
| `XgBoost_Model.ipynb` | `XGBClassifier`, `GridSearchCV`, feature importance |
| `Data_Visualization.ipynb` | `countplot`, `boxplot`, heatmap, KDE, bar charts |

---

**Last Updated**: March 2026 | **Project**: ShipmentSure — Predicting On-Time Delivery
