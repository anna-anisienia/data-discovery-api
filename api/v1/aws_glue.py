from fastapi import APIRouter
from typing import Optional
import awswrangler as wr
import boto3
import json
import datetime

router = APIRouter()
session = boto3.Session(region_name='eu-central-1')


@router.get("/schemas")
async def list_databases():
    return wr.catalog.databases(boto3_session=session).to_dict(orient='records')


@router.get("/tables")
async def list_tables_for_specific_schema(schema: Optional[str] = 'ecommerce'):
    return wr.catalog.tables(database=schema, boto3_session=session).to_dict(orient='records')


@router.get("/table_prefix")
async def list_tables_with_prefix(prefix: str):
    return wr.catalog.tables(name_prefix=prefix, boto3_session=session).to_dict(orient='records')


@router.get("/table_suffix")
async def list_tables_with_suffix(suffix: str):
    return wr.catalog.tables(name_suffix=suffix, boto3_session=session).to_dict(orient='records')


@router.get("/table_search")
async def list_tables_with_name(search_text: str):
    return wr.catalog.tables(name_contains=search_text, boto3_session=session).to_dict(orient='records')


@router.get("/table-definition")
async def get_table_definition(table: str, database: Optional[str] = 'ecommerce'):
    return wr.catalog.table(database=database, table=table, boto3_session=session).to_dict(orient='records')


@router.get("/preview")
def preview_x_rows(table: str, database: Optional[str] = 'ecommerce', nr_rows: Optional[int] = 10):
    query = f'SELECT * FROM {table} LIMIT {nr_rows};'
    data = wr.athena.read_sql_query(sql=query, database=database, ctas_approach=False, boto3_session=session)
    return json.loads(data.to_json(orient='records'))


@router.get("/partitions")
async def list_partitions(table: str, database: Optional[str] = 'ecommerce'):
    return wr.catalog.get_partitions(database=database,
                                     table=table, boto3_session=session)


@router.get("/ddl")
async def show_create_table_statement(table: str, database: Optional[str] = 'ecommerce'):
    return dict(ddl=wr.athena.show_create_table(database=database,
                                                table=table, boto3_session=session))


@router.get("/comments")
async def get_tables_with_comment(comment: str,
                                  database: Optional[str] = 'ecommerce'):
    query = f"""SELECT table_name, column_name, data_type, comment 
                FROM information_schema.columns WHERE comment LIKE '%{comment}%'"""
    return wr.athena.read_sql_query(sql=query, database=database,
                                    boto3_session=session).to_dict(orient='records')


@router.get("/describe-table")
async def get_athena_table(table: str, database: Optional[str] = 'ecommerce'):
    return wr.athena.describe_table(database=database, table=table,
                                    boto3_session=session).to_dict(orient='records')


@router.get("/columns")
async def get_tables_with_column(column: str, database: Optional[str] = 'ecommerce'):
    query = f"""SELECT table_name, column_name, data_type, comment 
                FROM information_schema.columns WHERE column_name LIKE '%{column}%'"""
    return wr.athena.read_sql_query(sql=query, database=database,
                                    boto3_session=session).to_dict(orient='records')


@router.get("/list_dir", tags=['s3'])
async def list_s3_directory(s3_path: str = 's3://ecommerce-marketplace/orders_partitioned/'):
    return wr.s3.list_directories(path=s3_path, boto3_session=session)


@router.get("/list_objects", tags=['s3'])
async def list_s3_objects(s3_path: str = 's3://ecommerce-marketplace/orders_partitioned/',
                          suffix: Optional[str] = None,
                          last_modified_begin: Optional[datetime.datetime] = None,
                          last_modified_end: Optional[datetime.datetime] = None):
    return wr.s3.list_objects(path=s3_path, suffix=suffix,
                              last_modified_begin=last_modified_begin,
                              last_modified_end=last_modified_end, boto3_session=session)
