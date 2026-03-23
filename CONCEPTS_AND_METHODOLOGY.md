# ShipmentSure: Concepts Overview

ShipmentSure is a machine learning project that predicts on-time delivery using supplier data. Here's a friendly overview of all the key concepts we use.

---

## 1. **Exploratory Data Analysis (EDA)**
Think of EDA as getting to know your data. We look at distributions, patterns, and relationships to understand what we're working with before we do anything fancy. Charts, statistics, and simple questions like "What does this feature look like?" help us spot issues early.



## 2. **Full Dataset Study**
Before diving into individual techniques, we do a holistic study of the entire dataset. This includes inspecting data types, checking shape and structure, computing summary statistics (`.describe()`), identifying categorical vs. numeric columns, and profiling value distributions. It sets the foundation for every step that follows.



## 3. **OLAP Analysis**
OLAP is like looking at your data from different angles. You can drill down from "total deliveries" to "deliveries by warehouse" to "deliveries by each mode of shipment." It helps answer business questions like: "Which warehouse performs best?" or "Which shipping mode is most reliable?"



## 4. **Data Preprocessing**
This is preparation work. We clean our raw data, fix issues, transform it into the right format, and organize it so it's ready for machine learning. Good preprocessing = good models. Bad preprocessing = garbage results.

## 5. **Data Cleaning**
Real-world data is messy. We handle missing values, remove duplicates, fix inconsistencies (like "M" vs "Male"), remove outliers, and correct invalid data. It's like tidying up your room before inviting guests!

## 6. **Handling Missing Values**
When data is missing, we have options:
- **Delete it**: Simple but lose information
- **Mean/Median fill**: Quick and easy
- **KNN impute**: Use similar records to fill gaps (better)
- **MICE/Iterative**: Fancy methods for complex patterns (best)

## 7. **Outlier Detection**
Some data points are weirdly different from others. We use **Isolation Forest** to spot these outliers. It's like finding the one person in a crowd who doesn't fit the pattern.

## 8. **Feature Scaling & Normalization**
Imagine comparing a person's height (180 cm) with their weight (80 kg). The numbers are on different scales! We use methods like:
- **Robust Scaling**: Perfect for data with outliers
- **Standardization (StandardScaler)**: Centers data to mean 0 and std 1, essential before clustering or PCA
- **Min-Max Scaling**: Bounds values 0-1
- **Quantile Transform**: Handles extreme values

## 9. **Skewness Analysis**
Some data is lopsided (skewed). If cost data has a long tail on the right (most cheap, few expensive), that's positive skew. We transform skewed data to make distributions more balanced for better model performance.

## 10. **Feature Encoding**
Machines don't understand words like "Flight" or "Male". We convert categories to numbers:
- **One-Hot Encoding**: Create binary columns (1 if matches, 0 if not)
- **Ordinal Encoding**: Assign numbers if there's an order (low=0, medium=1, high=2)

## 11. **Cyclic Encoding**
Some features are circular — hour 23 is close to hour 0, December is close to January. Standard encoding misses this! We use **sine and cosine transforms** to capture the circular nature:
- `sin_feature = sin(2π × value / period)`
- `cos_feature = cos(2π × value / period)`

This way, the model correctly understands that 11 PM and midnight are neighbours, not opposites. We apply this to time-based features like `Order_Hour`.

## 12. **Feature Hashing**
When a categorical feature has **many unique values** (high cardinality), one-hot encoding creates too many columns. **Feature Hashing** (the "hashing trick") maps categories into a fixed-size numeric vector using a hash function:
- Uses `FeatureHasher` from scikit-learn
- Controls output dimensionality (e.g., 4 or 6 columns instead of hundreds)
- Works for single or multi-column categorical combinations (e.g., `Mode_of_Shipment` + `Warehouse_block`)

Trade-off: some hash collisions can occur, but it's efficient and memory-friendly.

## 13. **Discretization (Binning)**
Sometimes converting continuous numbers into categories (bins) helps models find patterns. We use three approaches:
- **Equal-width binning** (`pd.cut`): Divides the range into equal-sized intervals
- **Equal-frequency binning** (`pd.qcut`): Each bin gets roughly the same number of data points
- **KBinsDiscretizer**: Scikit-learn's flexible binning with strategies like `uniform`, `quantile`, and `kmeans`

Example: Turning `Cost_of_the_Product` into "Low", "Medium", "High", "Premium" bins.

## 14. **Feature Generation & Engineering**
Creating **new features** from existing ones can dramatically improve models. We engineer features in two ways:

**Manual feature creation:**
- **Cost per gram**: `Cost_of_the_Product / (Weight_in_gms + 1)` — value density
- **Discount ratio**: `Discount_offered / (Cost_of_the_Product + 1)` — relative discount
- **Customer engagement**: `Customer_care_calls × Customer_rating` — interaction signal

**Automated feature creation:**
- **Polynomial Features** (`PolynomialFeatures`): Automatically generates interaction terms (e.g., `Cost × Discount`) and squared terms for non-linear relationships

## 15. **Data Transformation**
We transform features to improve them:
- **Quantile Transform**: Force uniform or normal distributions
- **Power Transform**: Fix skewness mathematically
- **Log Transform** (`np.log1p`): Handle right-skewed data like costs and discounts — reduces the pull of large values while preserving order
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

## 18. **Dimensionality Reduction**
Having 100 features can be overkill. **PCA** is our tool to reduce dimensions while keeping important information. It's like summarizing a book without losing the plot!

## 19. **Statistical Analysis**
We use correlations, mean/median values, and distribution tests to understand relationships between variables. Does customer rating affect delivery time? Statistics tell us!

## 20. **Data Visualization**
Pictures are worth 1000 words:
- **Histograms**: See distributions (before/after transforms)
- **Box Plots**: Spot outliers, compare groups and clusters
- **Scatter Plots**: Find relationships (great for cyclic encoding visualization)
- **Heatmaps**: Show correlations
- **KDE Plots**: Smooth distribution curves
- **Bar Charts**: Compare cluster profiles and feature scores
- **Count Plots**: Show category and bin distributions

## 21. **Pipeline Architecture**
We build a "recipe" that combines all our preprocessing steps:
1. Handle missing values (KNN Imputer)
2. Scale numeric features (Robust Scaler / Standard Scaler)
3. Encode categories (One-Hot / Feature Hashing / Cyclic Encoding)
4. Engineer new features (ratios, interactions)
5. Select best features (SelectKBest / PCA)
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
8. **Select** the best features (SelectKBest, PCA)
9. **Combine** everything in a pipeline
10. **Train** your machine learning model
11. **Predict** on-time delivery!

---

## Notebook-Wise Concepts and Methods (With Unique Project Purpose)

This section explains **why each function/method was used in this project workflow**, not just what it does in general.

### 1. `Data_Clean.ipynb`
- `describe()`, `info()`, `dtypes`, `select_dtypes()`: Used to build the first reliability baseline of the dataset before any transformation decision.
- `isnull().sum()`, `duplicated().sum()`, `nunique()`: Used to detect operational data quality risks (missingness, repeated shipments, high-cardinality columns).
- `corr(numeric_only=True)`, `sns.heatmap()`, `sns.boxplot()`: Used to identify correlated and outlier-sensitive variables that could distort model behavior later.

### 2. `EDA.ipynb`
- `read_csv()`, `head()`, `describe()`, `isnull().sum()`: Used for rapid dataset orientation and quick validation that source data loaded correctly.
- `sns.countplot()`: Used to inspect target imbalance in `Reached.on.Time_Y.N` early, which informs model evaluation strategy.

### 3. `Full_Dataset_Study.ipynb`
- `shape`, `info()`, `describe()`: Used to create a complete structural profile before deeper engineering.
- `skew()`, `value_counts(normalize=True)`: Used to decide which features need transformation and which categories dominate shipment behavior.
- `groupby().agg()`, `groupby().mean()`, `plt.pie()`, `plt.plot()`, `sns.histplot()`: Used to convert raw columns into business-facing summaries (mode-wise, warehouse-wise, delivery-rate-wise).

### 4. `Data_Analysis.ipynb`
- `groupby().mean()`, `pivot_table()`: Used for cross-dimensional operational comparisons (warehouse x shipment mode x rating/delivery behavior).
- `plt.scatter()`, `sns.scatterplot()`, `sns.barplot()`, `sns.heatmap()`: Used to visualize relationship strength and segment-level performance patterns.

### 5. `OLAP_Data_Analysis.ipynb`
- Boolean filtering (`df[condition]`, multi-condition dice): Used for OLAP-style slice and dice analysis on specific operational scenarios.
- `groupby().agg()`, `pivot_table()`: Used for roll-up/drill-down style metric aggregation across multiple logistics dimensions.
- `sns.heatmap(annot=True)`: Used to make matrix-level performance differences visible for stakeholder interpretation.

### 6. `Data_Skewness_Statistical_Analysis.ipynb`
- `skew()`, `mean()`, `median()`, `mode()`: Used to measure non-normality and decide transformation urgency for cost/discount variables.
- `sns.histplot(kde=True)`, `sns.boxplot()`: Used to validate skewness and outlier behavior visually before transformation.
- `sns.histplot(..., hue='Reached.on.Time_Y.N')`: Used to check if distribution shifts align with delivery outcomes.

### 7. `Categorical_Encoding.ipynb`
- Custom `CategoryReducer` and `RareLabelEncoder` (with `BaseEstimator`, `TransformerMixin`): Used to merge low-frequency labels into `Other`, reducing sparse noise before encoding.
- `fit/transform` pattern: Used to maintain consistent category treatment between training and inference contexts.

### 8. `Cyclic_Encoding_And_Discretization(26.2).ipynb`
- `np.sin()`, `np.cos()`, `np.pi`: Used to encode `Order_Hour` cyclically so hour 23 and hour 0 are treated as neighbors.
- `pd.cut()`, `pd.qcut()`, `KBinsDiscretizer(...)`: Used to compare three binning strategies and select discretization aligned with distribution shape.

### 9. `Feature_Hashing_Generation(25.2).ipynb`
- `FeatureHasher(n_features=...)`: Used to compress high-cardinality categorical information into fixed-width numeric space.
- `agg(' '.join, axis=1)`, `split()`: Used to create combined categorical tokens and capture cross-category interactions through hashing.
- `PolynomialFeatures(degree=2, interaction_only=True)`: Used to generate interaction signals (e.g., cost x discount) without exploding squared terms.
- `concat(axis=1)`: Used to merge engineered blocks into one model-ready feature table.

### 10. `Feature_Selection_PCA(3.3).ipynb`
- `get_dummies(drop_first=True)`: Used to convert categories while controlling multicollinearity in linear-style setups.
- `SelectKBest(f_classif, k=...)`, `get_support()`: Used to keep statistically strongest predictors for on-time delivery classification.
- `StandardScaler()` + `PCA(n_components=2)`: Used to reduce dimensional complexity while preserving dominant variance structure.
- `RandomForestClassifier()`, `feature_importances_`: Used to validate useful signal even after dimensionality reduction.

### 11. `KMeans_KBest_FeatureSelection(2.3).ipynb`
- `StandardScaler()`, `KMeans(...).fit_predict()`: Used to segment shipment profiles into natural operational clusters.
- `groupby().mean()`, `sns.countplot()`: Used to profile cluster characteristics and cluster size balance.
- `SelectKBest(f_classif, k=5)`: Used to identify top supervised features alongside unsupervised cluster exploration.

### 12. `KMeans_LogTransform(28.2).ipynb`
- `np.log1p()`: Used to stabilize heavily right-skewed cost/discount features before clustering.
- `StandardScaler()`, `KMeans(n_init=10)`: Used to produce stable and comparable cluster partitions.
- `describe()`, `sns.boxplot()`, `sns.histplot()`: Used to compare pre/post transformation behavior and interpret each resulting cluster.

### 13. `Data_Preprocessing(24.2).ipynb`
- `KNNImputer`, `IterativeImputer`, `SimpleImputer`: Used as a comparative imputation study to handle different missingness patterns.
- `RobustScaler`, `MinMaxScaler`, `PowerTransformer`, `QuantileTransformer`: Used to benchmark multiple normalization/transformation choices under outliers and skewness.
- `IsolationForest(contamination=...)`: Used to remove anomaly-driven noise before major transformations.
- `OrdinalEncoder`, `FeatureHasher`, `PolynomialFeatures`, `KBinsDiscretizer`: Used to encode categories, build compact features, create interactions, and discretize continuous predictors.
- `VarianceThreshold`, `SelectKBest`, `PCA`: Used to reduce redundant dimensions and retain predictive structure.

### 14. `Data_Pipeline_Preprocessing.ipynb`
- `Pipeline`, `ColumnTransformer`: Used to enforce reproducible, column-wise preprocessing for train/test consistency.
- `SimpleImputer(strategy='median'/'most_frequent')`: Used to apply type-specific imputation rules for numeric vs categorical columns.
- `StandardScaler`, `OneHotEncoder(handle_unknown='ignore')`: Used to standardize numeric distributions and safely encode unseen categories in inference.

### 15. `PreprocessingEngine_(16.3)AnamolyDetection.ipynb`
- Preprocessing engine structure (pipeline-driven transforms): Used to centralize reusable preprocessing logic.
- Anomaly detection methods (IsolationForest-style workflow): Used to flag rare shipment behavior that can degrade general model performance.

### 16. `FeatureUnion_TargetTransform(6.3).ipynb`
- `FeatureUnion` with PCA path + SelectKBest path: Used to combine complementary feature views (variance-based + label-signal-based).
- `TransformedTargetRegressor(LinearRegression, func=np.log1p, inverse_func=np.expm1)`: Used to train in log-space and predict on original scale for skewed targets.
- `train_test_split(...)`: Used to evaluate this hybrid feature strategy with a reproducible holdout split.

### 17. `LogisticRegression_(9.3)RandomForest.ipynb`
- `LogisticRegression`: Used as a linear, interpretable baseline for delivery classification.
- `RandomForestClassifier`: Used as a non-linear benchmark to capture interactions and non-linear boundaries.
- Classification metrics workflow (accuracy/precision/recall/confusion-matrix style): Used to compare model behavior beyond one single score.

### 18. `XgBoost(11.3)Model.ipynb`
- `XGBClassifier`/XGBoost training workflow: Used for boosted-tree modeling to capture complex feature interactions at high predictive strength.
- Evaluation and feature importance checks: Used to validate both performance and practical feature contribution.

### 19. `Data_Visualization.ipynb`
- `sns.countplot(...)` with and without `hue`: Used to compare class distribution across shipment and warehouse categories.
- `sns.boxplot(...)`: Used to detect continuous-feature behavior shifts between on-time and delayed shipments.
- Subplot grid patterns: Used to standardize side-by-side EDA comparisons for faster insight review.

---

## Methodology Flow Across Notebooks

1. **Profile and audit data quality** (`Data_Clean`, `EDA`, `Full_Dataset_Study`)
2. **Analyze business patterns and OLAP views** (`Data_Analysis`, `OLAP_Data_Analysis`)
3. **Diagnose skewness/outliers and transform distributions** (`Data_Skewness_Statistical_Analysis`, `Data_Preprocessing`)
4. **Encode/engineer/select features** (`Categorical_Encoding`, `Cyclic_Encoding...`, `Feature_Hashing_Generation`, `Feature_Selection_PCA`, `FeatureUnion_TargetTransform`)
5. **Cluster for segmentation insight** (`KMeans_KBest_FeatureSelection`, `KMeans_LogTransform`)
6. **Train supervised models and compare** (`LogisticRegression...`, `XgBoost...`)
7. **Maintain reproducibility through pipelines** (`Data_Pipeline_Preprocessing`, `PreprocessingEngine...`)

**Last Updated**: March 2026 | **Project**: ShipmentSure-Aanchal Yadav
