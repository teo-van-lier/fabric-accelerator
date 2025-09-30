# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0d4e2539-fb8a-4d9e-83db-68df719e9561",
# META       "default_lakehouse_name": "lh_silver",
# META       "default_lakehouse_workspace_id": "4385015c-08f1-4b2d-a43b-ceb37791dba3",
# META       "known_lakehouses": [
# META         {
# META           "id": "0d4e2539-fb8a-4d9e-83db-68df719e9561"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df_actuals = spark.sql(f"select * from bronze.accounting_actuals")
df_crm = spark.sql(f"select * from bronze.crm")
df_customers = spark.sql("select distinct CustomerID from bronze.crm")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col

# Define the columns and their target types
actuals_columns_to_cast = {
    "TransactionID": "int",
    "Date": "timestamp",
    "AccountCode": "int",
    "Amount": "double",
    "Currency": "string",
    "CustomerID": "string"
}

# Apply the cast
for c, t in actuals_columns_to_cast.items():
    df_actuals = df_actuals.withColumn(c, col(c).cast(t))

df_crm = df_crm.drop(col("__filepath__"))

crm_columns_to_cast = {
    "OpportunityID": "string",
    "CustomerID": "string",
    "OpportunityName": "string",
    "Stage": "string",
    "ExpectedCloseDate": "timestamp",
    "ExpectedRevenue": "double",
    "Owner": "string",
    "probability": "int",

}

# Apply the cast
for c, t in crm_columns_to_cast.items():
    df_crm = df_crm.withColumn(c, col(c).cast(t))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
start_date = "2019-01-01"
end_date = "2030-12-31"

df_date = (
    spark.sql(f"SELECT sequence(to_date('{start_date}'), to_date('{end_date}'), interval 1 day) as date_seq")
    .withColumn("Date", F.explode(F.col("date_seq")))
    .drop("date_seq")
)

df_date = (
    df_date
    .withColumn("Year", F.year("Date"))
    .withColumn("Month", F.month("Date"))
    .withColumn("Day", F.dayofmonth("Date"))
    .withColumn("Quarter", F.quarter("Date"))
    .withColumn("YearMonth", F.date_format("Date", "yyyy-MM"))
    .withColumn("MonthName", F.date_format("Date", "MMM"))
    .withColumn("DayOfWeek", F.date_format("Date", "E"))
    .withColumn("WeekOfYear", F.weekofyear("Date"))
    .withColumn("IsWeekend", F.when(F.col("DayOfWeek").isin(["Sat","Sun"]), F.lit(1)).otherwise(F.lit(0)))
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_crm)
display(df_actuals)
display(df_customers)
display(df_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_crm.write.mode("overwrite").format("delta").saveAsTable("dbo.fact_crm")
df_actuals.write.mode("overwrite").format("delta").saveAsTable("dbo.fact_actuals")
df_customers.write.mode("overwrite").format("delta").saveAsTable("dbo.dim_customers")
df_date.write.mode("overwrite").format("delta").saveAsTable("dbo.dim_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
