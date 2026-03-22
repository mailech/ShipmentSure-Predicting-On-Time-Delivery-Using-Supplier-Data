Delivery Time Prediction – Concepts Overview

This project predicts whether a shipment will be delivered on time or delayed using Machine Learning.

Instead of just building models, this project focuses on understanding every step of the ML pipeline deeply — from raw data to final predictions.

 The Big Idea

Think of this project as a journey:

Understand data → Clean it → Transform it → Engineer features → Build models → Improve performance

Each step builds on the previous one.
 1. Exploratory Data Analysis (EDA)

EDA is like getting to know your data first.

We analyze:

Distributions
Relationships
Patterns

Example insights:

Higher discounts → more delays
Shipment mode impacts delivery
Heavier products → more on-time
 2. Full Dataset Study

Before modeling, we deeply inspect the dataset:

Shape (10,999 × 12)
Data types (categorical vs numerical)
Summary statistics
Unique values

 This step builds the foundation for all decisions

 3. Data Cleaning

Real-world data is messy — but this dataset was clean:

No missing values 
No duplicates 
Column names standardized

 Clean data = reliable models

 4. Data Analysis (Business Insights)

We analyze data like a business problem:

Which warehouse performs best?
Which shipment mode is reliable?
How discount affects delivery?

 Key insight:
 High discount = high delay probability

 5. Skewness Analysis

Some features are not evenly distributed.

Example:

Discount → highly skewed
Prior purchases → skewed

 Why it matters:

Skewed data can mislead models

 Solution:

Log transform
Quantile transform
 6. Data Preprocessing

This is where raw data becomes model-ready.

Techniques used:
StandardScaler
RobustScaler
QuantileTransformer
OneHotEncoder

 Also:

KNN Imputation
Iterative Imputation
 7. Outlier Detection

Some data points don’t follow patterns.

Methods:
Isolation Forest
One-Class SVM

 Insight:

Isolation Forest → conservative
SVM → detects more anomalies
 8. Feature Encoding

Machines don’t understand text.

So we convert:

Flight / Ship / Road → numbers
Methods:
One-Hot Encoding
Feature Hashing
9. Cyclic Encoding

Time is circular (23 → close to 0)

We use:

sin(hour)
cos(hour)

👉 Helps model understand cyclic patterns

10. Discretization (Binning)

We convert numbers into categories:

Example:

Cost → Low / Medium / High
Methods:
Equal-width
Quantile
KBinsDiscretizer
 11. Feature Engineering

This is where models become powerful.

Created features:
Cost per gram
Discount ratio
Customer engagement
Polynomial Features:
Cost × Discount

 Helps capture non-linear relationships

 12. Feature Hashing

Used for high-cardinality categorical data.

 Benefits:

Reduces dimensionality
Faster than one-hot encoding
 13. Feature Selection

Not all features are useful.

Methods:
SelectKBest (ANOVA)
Mutual Information

 Keeps only important features

 14. Dimensionality Reduction (PCA)

Too many features → complex model

 PCA reduces features while keeping information

 15. Clustering (Unsupervised Learning)

We used:

 GMM (Gaussian Mixture Model)
Soft clustering
 Agglomerative Clustering
Hierarchical grouping

 Created new feature:

Cluster_Group
 16. Pipeline Architecture

We built pipelines to:

Ensure consistency
Avoid data leakage

 Example:

Preprocessing → Feature selection → Model

Key Learnings
Feature engineering > model complexity
Tree models outperform linear models
Discount is a strong predictor
Preprocessing is critical
Clustering improves feature understanding

Tech Stack
Python
Pandas, NumPy
Matplotlib, Seaborn
Scikit-learn
XGBoost
