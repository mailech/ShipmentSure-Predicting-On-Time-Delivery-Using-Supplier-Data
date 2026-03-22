ShipmentSure: Concepts Overview

DeliverySure is a machine learning project that predicts whether a shipment will be delivered on time or delayed using logistics and customer data.

This project is designed to demonstrate a complete end-to-end ML pipeline, covering everything from raw data understanding to advanced modeling techniques.

 The Big Picture

All concepts in this project follow a clear journey:

 Study data → Explore → Clean → Transform → Engineer → Select → Model → Predict

Each step builds intelligence into the system.

 1. Exploratory Data Analysis (EDA)

EDA is about understanding your data before modeling.

We analyze:

Distributions
Relationships
Patterns

 Key findings:

Higher discounts → higher delays
Shipment mode impacts delivery
Heavier products → more on-time deliveries
 2. Full Dataset Study

Before applying techniques, we analyze the dataset structure:

Shape: 10,999 × 12
Mixed data types (categorical + numerical)
Summary statistics using .describe()
Unique values and distributions

 This step defines how we approach preprocessing

 3. Data Cleaning

Real-world data is usually messy, but here:

No missing values 
No duplicates 
Clean categorical values 

 Clean data helps build reliable models

 4. OLAP & Business Analysis

We analyze data from different perspectives:

Warehouse performance
Shipment mode efficiency
Discount vs delivery

 Insight:
 High discounts strongly increase delay probability

 5. Data Preprocessing

Preprocessing prepares raw data for ML models.

Techniques used:
StandardScaler
RobustScaler
QuantileTransformer
OneHotEncoder

 Ensures:

Proper scaling
Consistent feature representation
 6. Handling Missing Values

Even though dataset is clean, techniques implemented:

Mean / Median
KNN Imputer
Iterative Imputer (MICE)

 Shows real-world readiness

 7. Outlier Detection

Outliers can distort models.

Methods used:
Isolation Forest
One-Class SVM

 Insight:

Isolation Forest → fewer anomalies
SVM → more sensitive
 8. Feature Scaling & Normalization

Different features have different scales.

We used:

StandardScaler → normalization
RobustScaler → handles outliers
MinMaxScaler → range scaling
Quantile Transform → handles skew
9. Skewness Analysis

Some features are skewed:

Discount → highly skewed
Prior purchases → skewed

 Solution:

Log transform
Quantile transform
 10. Feature Encoding

Convert categorical data into numerical form:

One-Hot Encoding
Feature Hashing

 Helps models understand categories

 11. Cyclic Encoding

Time-based features are circular.

We use:

sin()
cos()

Example:

Hour 23 ≈ Hour 0
 12. Feature Hashing

Used for efficient encoding of categorical data.

 Benefits:

Reduces dimensionality
Memory efficient
Handles large datasets
 13. Discretization (Binning)

Convert continuous values into categories:

Equal-width binning
Quantile binning
KBinsDiscretizer

 Helps models detect patterns

 14. Feature Engineering

We create new meaningful features:

Manual:
Cost per gram
Discount ratio
Customer engagement
Automatic:
Polynomial features (Cost × Discount)

 Improves model performance
 15. Data Transformation

Used to improve distributions:

Log transform
Quantile transform
Power transform

 Reduces skewness

 16. Clustering (Unsupervised Learning)
Methods used:
Gaussian Mixture Model (GMM)
Agglomerative Clustering

 Created new feature:

Cluster_Group

 Helps discover hidden patterns

 17. Feature Selection

Not all features are useful.

Methods:
SelectKBest (ANOVA)
Mutual Information

Keeps only important features

 18. Dimensionality Reduction

Used PCA to reduce feature space.

 Benefits:

Reduces complexity
Improves performance


 19. Statistical Analysis

Used:

Correlation analysis
Mean / median comparisons
Group-based insights

 Helps understand relationships

 20. Data Visualization

Used multiple plots:

Histograms
Boxplots
Scatter plots
Heatmaps
Count plots

 Helps interpret data visually

 
 21. Pipeline Architecture

Built reusable pipelines:

Preprocessing
Feature selection
Modeling

Ensures:

No data leakage
Consistency
 22. Models Used
Logistic Regression
Accuracy: ~65%
Baseline model
FeatureUnion Pipeline
PCA + SelectKBest
Accuracy: ~64.8%

 Random Forest 
Accuracy: 67.32% (Best)
Handles non-linearity
XGBoost
Accuracy: ~65.5%
Feature importance extracted


Model saved using pickle
Final Model Comparison
Model	Accuracy
Logistic Regression	65.18%
FeatureUnion	64.81%
XGBoost	65.54%
 Random Forest	67.32%

 
 Key Learnings
Feature engineering is crucial
Tree models outperform linear models
Discount is the strongest predictor
Preprocessing impacts accuracy heavily
Clustering improves understanding


 Complete Workflow
Dataset Study → EDA → Cleaning → Preprocessing →
Feature Engineering → Feature Selection →
Clustering → Modeling → Prediction


 Tech Stack
Python
Pandas, NumPy
Matplotlib, Seaborn
Scikit-learn
XGBoost
