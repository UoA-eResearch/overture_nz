# overture_nz
Python script to extract all Overture POIs, deck.gl to plot it

From https://overturemaps.org/  
Places are licensed under CDLA Permissive v 2.0, see https://cdla.dev/permissive-2-0/

### Downloading

Run:

```docker run -it -v `pwd`:/opt/workspace apache/sedona:latest python3 download.py```

to download to POIs for NZ, and export to CSV format in the current working directory