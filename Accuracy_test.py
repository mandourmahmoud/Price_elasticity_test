import pandas as pd
import numpy as np

model_data = pd.read_csv("Model_data.csv")
actual_data = pd.read_csv("Actual_data.csv")

# Merging the actual data with model data on 'product_sku'
merged_data = pd.merge(actual_data, model_data, on='product_sku', how='left')

merged_data = merged_data.dropna()

# Calculate the absolute difference between model's active price and actual avg low price
merged_data['abs_diff_price'] = abs(merged_data['active_price_12m'] - merged_data['avg_m12_low_price'])

# Finding the closest predictions for each product_sku
# Group by product_sku and find the row with the minimum absolute difference in price
closest_predictions = merged_data.loc[merged_data.groupby('product_sku')['abs_diff_price'].idxmin()]

# Display the first few rows of the closest predictions for inspection
closest_predictions_head = closest_predictions.head()
closest_predictions_head

merged_data['orders_diff'] = merged_data.total_submitted_orders - merged_data.total_preds

# Finding the index of the row with the minimum 'abs_diff_price' for each 'product_sku'
min_diff_indices = merged_data.groupby('product_sku')['orders_diff'].idxmin()

# Filtering the original dataframe to include only these rows
unique_min_diff_data = merged_data.loc[min_diff_indices]

#unique_min_diff_data.to_csv("unique_min_diff_data.csv")
