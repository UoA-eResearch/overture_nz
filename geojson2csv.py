#!/usr/bin/env python3

# overturemaps download --bbox 163.08,-50.12,180,-31.31 -f geojson -o overture_NZ.geojson -t place

import geopandas as gpd

df = gpd.read_file("overture_NZ.geojson")
df["lng"] = df.geometry.apply(lambda p: p.x)
df["lat"] = df.geometry.apply(lambda p: p.y)
df["name"] = df.names.apply(lambda c: c["primary"])
df["main_category"] = df.categories.apply(lambda c: c["main"] if type(c) is dict else None)
df["alternate_categories"] = df.categories.apply(lambda c: c["alternate"] if type(c) is dict else None)
df[["name", "main_category", "alternate_categories", "lat", "lng"]].to_csv("overture_NZ.csv", index=False)