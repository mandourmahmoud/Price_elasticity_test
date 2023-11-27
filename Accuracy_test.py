import pandas as pd
import numpy as np

model_data = pd.read_csv("Model_data.csv")
actual_data = pd.read_csv("Actual_data.csv")

# Merging the actual data with model data on 'product_sku'
merged_data = pd.merge(actual_data, model_data, on='product_sku', how='left')
merged_data = merged_data.dropna()

# Calculate the absolute difference between model's active price and actual avg low price
merged_data['abs_diff_price'] = abs(merged_data['active_price_12m'] - merged_data['avg_m12_low_price'])
merged_data = merged_data.sort_values(['product_sku','abs_diff_price'])

# Finding the closest predictions for each product_sku
# Group by product_sku and find the row with the minimum absolute difference in price
closest_predictions = merged_data.loc[merged_data.groupby('product_sku')['abs_diff_price'].idxmin()]

closest_predictions['orders_diff'] = closest_predictions.total_submitted_orders - merged_data.total_preds

# Define the bucket ranges: from -50 to 55 in steps of 5
buckets = list(range(-50, 60, 5))  # Generates [-50, -45, -40, ..., 50, 55]
bucket_labels = [f'{buckets[i]} to {buckets[i+1]}' for i in range(len(buckets)-1)]

# Extend the range to include orders above 55
buckets.append(np.inf)
bucket_labels.append('More than 55')

# Categorize 'orders_diff' into buckets
closest_predictions['orders_diff_bucket'] = pd.cut(closest_predictions['orders_diff'], buckets, labels=bucket_labels, right=False)

# Group by 'category_name' and 'orders_diff_bucket', then count the number of products in each group
grouped_buckets = closest_predictions.groupby(['category_name', 'orders_diff_bucket']).size().reset_index(name='count')

# Define the bucket ranges: create a range with 2-euro intervals
max_price_diff = closest_predictions['abs_diff_price'].max()
buckets = list(np.arange(0, max_price_diff + 2, 2))  # Generates [0, 2, 4, ..., max_price_diff]
bucket_labels = [f'{buckets[i]} to {buckets[i+1]}' for i in range(len(buckets)-1)]

# Extend the range to include price differences above the last bucket
buckets.append(np.inf)
bucket_labels.append(f'More than {max_price_diff}')

# Categorize 'abs_diff_price' into buckets
closest_predictions['price_diff_bucket'] = pd.cut(closest_predictions['abs_diff_price'], buckets, labels=bucket_labels, right=False)

# Optionally, group by 'category_name' and 'price_diff_bucket'
grouped_price_buckets = closest_predictions.groupby(['category_name', 'price_diff_bucket']).size().reset_index(name='count')

# Output the grouped data
#print(grouped_price_buckets)

test = closest_predictions[closest_predictions['abs_diff_price'] == 0 ]