from fastapi import APIRouter
from v1 import aws_glue

router = APIRouter()
router.include_router(aws_glue.router, tags=["AWS Glue Metadata Catalog"])
