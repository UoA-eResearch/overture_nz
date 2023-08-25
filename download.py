# Run with docker run --rm -it -v `pwd`:/opt/workspace apache/sedona:latest python3 download.py

import time
from sedona.spark import *
config = SedonaContext.builder().config("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider").getOrCreate()
sedona = SedonaContext.create(config)

df = sedona.read.format("parquet").load("s3a://overturemaps-us-west-2/release/2023-07-26-alpha.0/theme=places/type=place")
nz = df.filter("ST_Contains(ST_GeomFromWKT('Polygon((160 -30.5,187 -30.5,187 -49.5,160 -49.5, 160 -30.5))'), ST_GeomFromWKB(geometry)) = true")

def geomTypeConverter(df, df_name):
    new_columns = []
    # Find the geometry column and convert it to a Sedona geometry type column
    for col_name in df.schema.names:
        if col_name == "geometry":
            new_columns.append("ST_GeomFromWKB(geometry) AS geometry")
        else:
            new_columns.append(col_name)
    cols =','.join(new_columns)
    df.createOrReplaceTempView(df_name)
    df = sedona.sql("SELECT " + cols + " FROM "+df_name)
    df.createOrReplaceTempView(df_name)
    return df

tbl_name = "df_place"
nz = geomTypeConverter(nz, tbl_name)

print("Downloading...")
s = time.time()
nz = nz.toPandas()
print(f"Took {round(time.time() - s)}s") # Takes about 121s

nz["lng"] = nz.geometry.apply(lambda p: p.x)
nz["lat"] = nz.geometry.apply(lambda p: p.y)

nz["name"] = nz.names.apply(lambda d: d["common"][0]["value"])
nz["main_category"] = nz.categories.apply(lambda c: c.main)
nz["alternate_categories"] = nz.categories.apply(lambda c: c.alternate)

nz[["name", "main_category", "alternate_categories", "lat", "lng"]].to_csv("overture_nz.csv", index=False)
