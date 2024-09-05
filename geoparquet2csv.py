#!/usr/bin/env python3

import geopandas as gpd

df = gpd.read_parquet("overture_NZ.geoparquet")
df["lng"] = df.geometry.apply(lambda p: p.x)
df["lat"] = df.geometry.apply(lambda p: p.y)
df["name"] = df.names.apply(lambda c: c["primary"])
df["main_category"] = df.categories.apply(lambda c: c["primary"] if type(c) is dict else None)
df["alternate_categories"] = df.categories.apply(lambda c: ",".join(c["alternate"]) if type(c) is dict and c["alternate"] is not None else None)
df[["name", "main_category", "alternate_categories", "lat", "lng"]].to_csv("overture_NZ.csv", index=False)
