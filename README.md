# overture_nz
Python script to extract all Overture POIs, deck.gl to plot it

From https://overturemaps.org/  
Places are licensed under CDLA Permissive v 2.0, see https://cdla.dev/permissive-2-0/

## Installation

`pip install geopandas`

### Downloading

Run:

`overturemaps download --bbox 163.08,-50.12,180,-31.31 -f geoparquet -o overture_NZ.geoparquet -t place`  
`python geoparquet2csv.py`

to download to POIs for NZ, and export to CSV format in the current working directory