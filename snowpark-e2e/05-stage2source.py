import sys
import logging

from snowflake.snowpark import Session, DataFrame
from snowflake.snowpark.types import StructType, StringType, StructField, StringType,LongType,DecimalType,DateType,TimestampType
from snowflake.snowpark.functions import col,lit,row_number, rank
from snowflake.snowpark import Window

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')

# snowpark session
def get_snowpark_session() -> Session:
    connection_parameters = {
       "ACCOUNT":"ggrjtxv-rc04513",
        "USER":"snowpark_user",
        "PASSWORD":"Test@12$4",
        "ROLE":"SYSADMIN",
        "DATABASE":"SNOWFLAKE_SAMPLE_DATA",
        "SCHEMA":"TPCH_SF1",
        "WAREHOUSE":"SNOWPARK_ETL_WH"
    }
    # creating snowflake session object
    return Session.builder.configs(connection_parameters).create()   



def ingest_us_sales(session)-> None:
    session.sql(' \
            copy into sales_dwh.source.us_sales_order                \
            from                                    \
            (                                       \
                select                              \
                sales_dwh.source.us_sales_order_seq.nextval, \
                $1:"Order ID"::text as orde_id,   \
                $1:"Customer Name"::text as customer_name,\
                $1:"Mobile Model"::text as mobile_key,\
                to_number($1:"Quantity") as quantity,\
                to_number($1:"Price per Unit") as unit_price,\
                to_decimal($1:"Total Price") as total_price,\
                $1:"Promotion Code"::text as promotion_code,\
                $1:"Order Amount"::number(10,2) as order_amount,\
                to_decimal($1:"Tax") as tax,\
                $1:"Order Date"::date as order_dt,\
                $1:"Payment Status"::text as payment_status,\
                $1:"Shipping Status"::text as shipping_status,\
                $1:"Payment Method"::text as payment_method,\
                $1:"Payment Provider"::text as payment_provider,\
                $1:"Phone"::text as phone,\
                $1:"Delivery Address"::text as shipping_address,\
                metadata$filename as stg_file_name,\
                metadata$file_row_number as stg_row_numer,\
                metadata$file_last_modified as stg_last_modified\
                from                                \
                    @sales_dwh.source.my_internal_stg/sales/source=US/format=Parquet/\
                    (file_format => sales_dwh.common.my_parquet_format)\
                    ) on_error = continue \
            '
            ).collect()
    
def ingest_fr_sales(session)-> None:
    session.sql(' \
        copy into sales_dwh.source.fr_sales_order                                \
        from                                                    \
        (                                                       \
            select                                              \
            sales_dwh.source.fr_sales_order_seq.nextval,         \
            $1:"Order ID"::text as orde_id,                   \
            $1:"Customer Name"::text as customer_name,          \
            $1:"Mobile Model"::text as mobile_key,              \
            to_number($1:"Quantity") as quantity,               \
            to_number($1:"Price per Unit") as unit_price,       \
            to_decimal($1:"Total Price") as total_price,        \
            $1:"Promotion Code"::text as promotion_code,        \
            $1:"Order Amount"::number(10,2) as order_amount,    \
            to_decimal($1:"Tax") as tax,                        \
            $1:"Order Date"::date as order_dt,                  \
            $1:"Payment Status"::text as payment_status,        \
            $1:"Shipping Status"::text as shipping_status,      \
            $1:"Payment Method"::text as payment_method,        \
            $1:"Payment Provider"::text as payment_provider,    \
            $1:"Phone"::text as phone,                          \
            $1:"Delivery Address"::text as shipping_address ,    \
            metadata$filename as stg_file_name,\
            metadata$file_row_number as stg_row_numer,\
            metadata$file_last_modified as stg_last_modified\
            from                                                \
            @sales_dwh.source.my_internal_stg/sales/source=FR/format=JSON/\
            (file_format => sales_dwh.common.my_json_format)\
            ) on_error=continue\
        '
        ).collect()

def main():

    #get the session object and get dataframe
    session = get_snowpark_session()

   

    #ingest in sales data
    ingest_us_sales(session) 

    #ingest in sales data
    ingest_fr_sales(session)   

if __name__ == '__main__':
    main()