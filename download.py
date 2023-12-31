# Run with docker run --rm -it -v `pwd`:/opt/workspace apache/sedona:latest python3 download.py

import time
from sedona.spark import *
config = SedonaContext.builder().config("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider").getOrCreate()
sedona = SedonaContext.create(config)

df = sedona.read.format("parquet").load("s3a://overturemaps-us-west-2/release/2023-07-26-alpha.0/theme=places/type=place")
# NZ
#df = df.filter("ST_Contains(ST_GeomFromWKT('Polygon((160 -30.5,187 -30.5,187 -49.5,160 -49.5, 160 -30.5))'), ST_GeomFromWKB(geometry)) = true")
# Switzerland
df = df.filter("ST_Contains(ST_GeomFromWKT('POLYGON((5.9559 47.8084, 10.4921 47.8084, 10.4921 45.818, 5.9559 45.818, 5.9559 47.8084))'), ST_GeomFromWKB(geometry)) = true")

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
df = geomTypeConverter(df, tbl_name)

print("Downloading...")
s = time.time()
df = df.toPandas()
print(f"Took {round(time.time() - s)}s") # Takes about 121s

df["lng"] = df.geometry.apply(lambda p: p.x)
df["lat"] = df.geometry.apply(lambda p: p.y)

df["name"] = df.names.apply(lambda d: d["common"][0]["value"])
df["main_category"] = df.categories.apply(lambda c: c.main)
df["alternate_categories"] = df.categories.apply(lambda c: c.alternate)

df[["name", "main_category", "alternate_categories", "lat", "lng"]].to_csv("overture_CH.csv", index=False)
