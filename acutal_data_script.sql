select  dwh.product_sku
,sum(dwh.completed_orders) total_submitted_orders
--,dwh.fact_day
--,dwh.store_id
,AVG(CASE WHEN apgs.rental_plan_price_12_months LIKE '%,%'
         THEN SPLIT_PART(apgs.rental_plan_price_12_months, ',', 1)::FLOAT
         ELSE apgs.rental_plan_price_12_months::FLOAT
    END) AS avg_m12_low_price
,AVG(CASE WHEN apgs.rental_plan_price_12_months LIKE '%,%'
         THEN SPLIT_PART(apgs.rental_plan_price_12_months, ',', 2)::FLOAT
         ELSE apgs.rental_plan_price_12_months::FLOAT
    END) AS avg_m12_high_price
from dwh.product_reporting dwh
left join pricing.all_pricing_grover_snapshots apgs
on apgs.product_sku = dwh.product_sku and dwh.fact_day = apgs.snapshot_date
where fact_day between '2023-11-01' and '2023-11-07' and store_id != 621
group by dwh.product_sku
