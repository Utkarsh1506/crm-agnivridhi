# Production Database Check Commands

## For PythonAnywhere MySQL:

```bash
# Login to PythonAnywhere Bash Console
# Then run:

mysql -u agnivridhicrm -p'<password>' agnivridhicrm_db -e "
SELECT 
  id, company_name, total_pitched_amount, gst_percentage, gst_amount, 
  total_with_gst, received_amount, pending_amount,
  CASE 
    WHEN total_with_gst = 0 THEN 'NO_REVENUE'
    WHEN received_amount = 0 THEN 'UNPAID'
    WHEN received_amount >= total_with_gst THEN 'PAID'
    ELSE 'PARTIAL'
  END as status
FROM clients_client 
ORDER BY id;
"
```

## To see summary:

```bash
mysql -u agnivridhicrm -p'<password>' agnivridhicrm_db -e "
SELECT 
  COUNT(*) as total,
  COUNT(CASE WHEN total_with_gst > 0 AND received_amount >= total_with_gst THEN 1 END) as paid,
  COUNT(CASE WHEN total_with_gst > 0 AND received_amount > 0 AND received_amount < total_with_gst THEN 1 END) as partial,
  COUNT(CASE WHEN total_with_gst > 0 AND received_amount = 0 THEN 1 END) as unpaid,
  COUNT(CASE WHEN total_with_gst = 0 THEN 1 END) as no_revenue
FROM clients_client;
"
```

## If all showing as "PAID" - likely issue:

The `received_amount` field mein probably ₹0 ho aur check `total_with_gst = 0` condition mein issue hogi. 

Check if pending_amount is being calculated wrongly:

```bash
mysql -u agnivridhicrm -p'<password>' agnivridhicrm_db -e "
SELECT id, company_name, total_with_gst, received_amount, pending_amount FROM clients_client LIMIT 10;
"
```

