
import pandas as pd

# Load dataset
df = pd.read_csv("./Train.csv")

# Display first 5 rows
print("Head:")
print(df.head())

# Display last 5 rows
print("\nTail:")
print(df.tail())

# Dataset information
print("\nInfo:")
print(df.info())

#description
print("\nDescribe:")
print(df.describe())

# Mean, Median, Mode
print("\nMean:")
print(df.mean(numeric_only=True))

print("\nMedian:")
print(df.median(numeric_only=True))

print("\nMode:")
print(df.mode().iloc[0])

# Check null values
print("\nNull Values:")
print(df.isnull().sum())

# Check total missing values
print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

# Fill missing values with mean
df_filled = df.fillna(df.mean(numeric_only=True))

# Drop missing values
df_dropped = df.dropna()

# Unique values count
print("\nUnique Values:")
print(df.nunique())

# Value counts (for first column)
first_col = df.columns[0]
print(f"\nValue Counts of {first_col}:")
print(df[first_col].value_counts())

# Correlation matrix
print("\nCorrelation Matrix:")
print(df.corr(numeric_only=True))

# Shape of dataset
print("\nShape:")
print(df.shape)

# Column names
print("\nColumns:")
print(df.columns)

# Check duplicates
print("\nDuplicate Rows:")
print(df.duplicated().sum())
