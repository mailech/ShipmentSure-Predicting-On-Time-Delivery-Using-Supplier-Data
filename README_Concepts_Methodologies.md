# ShipmentSure: Machine Learning Concepts and Methodologies

This guide provides a detailed analysis of the concepts, tools, and methodologies implemented across the project's machine learning notebooks. Use this as a reference for revision and understanding the technical workflow.

---

## 1. Feature Engineering & Target Transformation
**Notebook**: [feature_union_target_transform.ipynb](./feature_union_target_transform.ipynb)

### Concepts
- **FeatureUnion**: A Scikit-Learn tool that allows you to combine multiple transformer objects into a single transformer. It applies each transformer in parallel to the input data and concatenates the results. 
    - *Benefit*: Useful for extracting different types of features (e.g., PCA components and univariate selection) simultaneously.
- **TransformedTargetRegressor**: A meta-regressor that transforms the target variable ($y$) before fitting the model and applies the inverse transformation after prediction.
    - *Benefit*: Simplifies working with targets that require scaling or log-transformation (e.g., to handle skewness) without manual bookkeeping.

### Methodology
1. **Pipeline Construction**: Individual pipelines were created for Scaling/PCA and Univariate Selection.
2. **Parallel Processing**: `FeatureUnion` combined these pipelines into a single step.
3. **Target Scaling**: Applied `np.log1p` during training and `np.expm1` during prediction to stabilize the target distribution.

---

## 2. Feature Selection & PCA Analysis
**Notebook**: [feature_selection_PCA.ipynb](./feature_selection_PCA.ipynb)

### Concepts
- **SelectKBest**: A univariate feature selection method that selects the top $k$ features based on statistical tests. In this project, `f_classif` (ANOVA F-value) was used to measure the relationship between features and the target.
- **Principal Component Analysis (PCA)**: A dimensionality reduction technique that transforms features into a new coordinate system (Principal Components). It captures the directions of maximum variance in the data.
- **Standardization (StandardScaler)**: Centers the data (mean = 0) and scales it to unit variance (std = 1). 
    - *Critical Note*: PCA is sensitive to scales; always standardize before applying PCA.

### Methodology
1. **Data Cleaning**: Checked for missing values to ensure robustness.
2. **Filtering**: Used `SelectKBest` to discard low-impact features early ($k=2$).
3. **Compression**: Applied PCA to reduce the selected features into 2 principal components for compact representation.
4. **Validation**: Trained a Random Forest on components to verify predictive power.
5. **Visualization**: Used boxplots to inspect the distribution and outliers of the new PCA components.

---

## 3. Classification Model Comparison
**Notebook**: [logistic_regression_random_forest.ipynb](./logistic_regression_random_forest.ipynb)

### Concepts
- **Logistic Regression**: A linear model for binary classification. It estimates the probability of a class using the logistic function.
- **Random Forest Classifier**: An ensemble learning method that builds multiple decision trees and merges them together (bagging) to get a more accurate and stable prediction.
- **Confusion Matrix**: A table used to describe the performance of a classification model. It shows:
    - **True Positives (TP)**: Correctly predicted "On Time".
    - **True Negatives (TN)**: Correctly predicted "Delayed".
    - **False Positives (FP)**: Predicted "On Time" but was "Delayed".
    - **False Negatives (FN)**: Predicted "Delayed" but was "On Time".

### Methodology
1. **Stratification**: Split data ensuring a fair representation of classes in training and testing.
2. **Model Training**: Fitted both a linear model (Logistic) and a non-linear model (Random Forest).
3. **Evaluation**:
    - **Accuracy**: Overall correctness.
    - **Precision**: How many of the predicted "On Time" were actually "On Time".
    - **Recall**: How many of the actual "On Time" were correctly identified.
4. **Comparative Analysis**: Visualized the trade-offs between models using a bar chart and heatmaps.

---

## 4. Data Profiling & Statistical Analysis
**Notebooks**: [comprehensive_data_analysis.ipynb](./comprehensive_data_analysis.ipynb), [data_skewness_and_statistical_analysis.ipynb](./data_skewness_and_statistical_analysis.ipynb)

### Concepts
- **Skewness Analysis**: Quantification of the asymmetry of a feature's distribution. 
    - *Metric*: Uses Fisher-Pearson coefficient of skewness. 
    - *Insight*: Features like `Discount_offered` (1.79) and `Prior_purchases` (1.68) show high positive skewness, often requiring transformation (log or power) for linear models.
- **Multivariate Grouped Aggregation**: Calculating statistics (mean, min, max) for numerical features across categories.
    - *Insight*: Comparing delivery status against average cost/weight helps identify class separators. For example, lower average weight and higher average discounts are strongly associated with "On Time" labels ($y=1$).
- **Data Completeness & Cardinality**: Automated checks for missing values (`isnull().sum()`) and unique value counts (`nunique()`) to determine feature encoding strategies.

### Methodology
1. **Feature Audit**: Created a consolidated table of Data Type, Unique Values, Missingness, and Skewness.
2. **Class-Conditional Analysis**: Segmented the data by the target `Reached.on.Time_Y.N` to observe differences in feature behavior.
3. **Warehouse Benchmarking**: Analyzed average product performance metrics across different warehouse blocks to identify operational variance.

---

## 5. Exploratory Data Visualization
**Notebook**: [data_visualization.ipynb](./data_visualization.ipynb)

### Concepts
- **Univariate Distribution**: Identifying class imbalance in the target variable (`Reached.on.Time_Y.N`).
- **Segmented Bivariate Analysis**: 
    - *Categorical vs Target*: Using countplots with `hue` to see how delivery success varies by `Mode_of_Shipment` and `Warehouse_block`.
    - *Numerical vs Target*: Using boxplots to compare distributions of `Cost_of_the_Product` and `Discount_offered` across delivery outcomes.
- **Outlier Detection via Boxplots**: Visual identification of extreme values in the `Discount_offered` feature for on-time vs. delayed shipments.

### Methodology
1. **Class Distribution**: Plotted a countplot for `Reached.on.Time_Y.N` to confirm the baseline delivery rate (~60% on time).
2. **Operational Heatmaps/Bar Charts**: Visualized shipment modes to identify that "Ship" and "Flight" have high volumes, with similar delivery success ratios.
3. **Financial Correlation**: Boxplots revealed that higher discounts are almost exclusively tied to on-time deliveries, serving as a strong predictor.

---

## 6. Comprehensive Dataset Study & Summary
**Notebook**: [full_dataset_Study.ipynb](./full_dataset_Study.ipynb)

### Concepts
- **Bivariate Statistical Summary**: Generating a bird's-eye view of feature behavior by target class.
- **Hypothesis Grounding**: Using groupby results to validate assumptions (e.g., higher discounts leading to on-time delivery).
- **Categorical Proportions**: Calculating percentage distributions of categories to monitor frequency imbalance.

### Methodology
1. **Target Stratification**: Discovered that `Discount_offered` mean for on-time ($y=1$) is ~18.6 vs ~5.5 for delayed ($y=0$), confirming "high discount = high priority/on-time" trend.
2. **Product Importance Analysis**: Found that "High" importance products have a ~65% on-time rate, significantly better than "Low" (~59%).
3. **Weight Correlation**: On-time shipments showed a lower average weight (~3272g) compared to delayed ones (~4168g), suggesting lighter packages move faster.
4. **Data Audit Export**: Created a tabular summary indicating:
    - `Cost_of_the_Product`: Skewness -0.15 (Near Normal)
    - `Discount_offered`: Skewness 1.79 (Highly Positive)
    - `Weight_in_gms`: Skewness -0.25 (Slight Negative)

---

## 7. OLAP Data Analysis
**Notebook**: [olap_data_analysis.ipynb](./olap_data_analysis.ipynb)

### Concepts
- **Slice**: Filtering the data cube along a single dimension (e.g., only "Warehouse A").
- **Dice**: Defining a sub-cube by filtering multiple dimensions (e.g., "Warehouse A" AND "Flight Shipments").
- **Roll-Up**: Aggregating data to a higher level of granularity (e.g., total cost per warehouse).
- **Drill-Down**: Moving from high-level summaries to detailed raw data.
- **Pivot**: Creating cross-tabulations between dimensions to observe intersections (e.g., Weight vs. Product Importance).

### Methodology
1. **Multidimensional Assessment**: Used standard Pandas filtering and `groupby` to simulate OLAP operations.
2. **Intersection Discovery**: Identified that the combination of high cost and low discount in certain warehouses significantly increases delay risk.
3. **Pivot Table Synthesis**: Generated matrix views to compare average customer ratings against shipment modes, identifying operational weak points.

---

## 8. Gradient Boosting for Predictive Performance
**Notebook**: [xgboost_model.ipynb](./xgboost_model.ipynb)

### Concepts
- **XGBoost (Extreme Gradient Boosting)**: A high-performance ensemble learning algorithm based on gradient-boosted decision trees.
- **Regularization (L1 & L2)**: Built-in penalties to control model complexity and prevent overfitting, often superior to standard Gradient Boosting.
- **Handling Missing Values**: An "sparsity-aware" algorithm that automatically learns the best imputation direction for missing data during training.
- **Feature Importance**: Uses metrics like `Gain` (contribution of a feature to the model's accuracy) or `Weight` (number of times a feature is used in trees) to interpret the model.
- **Parallel Processing**: Optimized for system resource utilization, allowing for faster training on large datasets compared to traditional GBDT implementations.

### Methodology
1. **Targeted Preprocessing**: Focused on dropping non-predictive columns (`ID`) and implementing One-Hot Encoding for categorical features.
2. **Baseline Model Development**: Initialized an `XGBClassifier` with a low learning rate and moderate tree depth to establish a performance baseline.
3. **Hyperparameter Optimization**: Used `RandomizedSearchCV` to efficiently explore a large parameter space (learning rate, depth, subsample, gamma) without the computational cost of an exhaustive grid search.
4. **Performance Profiling**: Analyzed the model using Confusion Matrices and Feature Importance plots to ensure predictors like `Discount_offered` and `Weight_in_gms` were correctly prioritized.

---
