select product_sku
,total_preds
,discount_12m
,high_price_12m
,active_price_12m
,snapshot_date::date
from pricing.price_elasticity_forecast
where snapshot_date::date = '2023-10-30'
