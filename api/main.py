from fastapi import FastAPI
from v1.routers import router
from mangum import Mangum

app = FastAPI(title='Data Discovery API',
              description='API on top of AWS Glue to provide '
                          'programming-language-agnostic metadata catalog')
app.include_router(router, prefix="/v1")


@app.get("/")
def read_root():
    return {"Hello": "from FastAPI & API Gateway Data Discovery API"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
