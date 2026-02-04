# Import the fimeval package you installed in your virtual environment
import fimeval as fe

# User inputs: either model FIM raster, boundary AOI, or both
raster_path = "resources/PSS_3_0m_20240623T172354_955825W430019N_BM.tif"
boundary_path = "resources/PSS_3_0m_20240623T172354_955825W430019N_AOI.gpkg"

"""
Supports multiple combinations of filters. Choose ONE pattern and set the
others to None:

a) AOI-only search (raster or boundary), optional overlap stats.
b) AOI + exact date.
c) AOI + date range (with optional download).
d) Direct filename to download (no AOI/dates) – usually once you know
   the exact benchmark FIM name.
NOTE: if no date: returns all available benchmark FIMs for the AOI.

Common parameters
-----------------
raster_path:
    Optional path to user raster (e.g., model FIM).
boundary_path:
    Optional vector AOI file (can be used with or without raster).
huc8:
    Optional HUC8 filter (mainly for US basins).
event_date:
    Exact event date (optionally with hour).
start_date, end_date:
    Inclusive date range filter.
file_name:
    Exact benchmark FIM filename from the catalog.
area:
    If True and AOI given, return % overlap and km² vs benchmark AOI.
download:
    If True, download matched rasters/GPKGs to ``out_dir``.
out_dir:
    Directory for downloads (required if ``download=True``).
"""

# a) AOI-only search (no dates, no filename)
log_aoi_only = fe.benchFIMquery(
    raster_path = raster_path,   # or None, if you only have boundary
    boundary_path = None,        # or boundary_path
    huc8 = None,
    event_date = None,
    start_date = None,
    end_date = None,
    file_name = None,
    area = True,                 # returns overlap stats vs benchmark AOI
    download = False,
    out_dir = None,
)
print("AOI-only search:", log_aoi_only)

# b) AOI + exact date
log_aoi_exact_date = fe.benchFIMquery(
    raster_path = raster_path,
    boundary_path = None,
    huc8 = None,
    event_date = "2024-06-23T17",   # YYYY-MM-DD or YYYY-MM-DD HH:MM
    start_date = None,
    end_date = None,
    file_name = None,
    area = True,
    download = False,
    out_dir = None,
)
print("AOI + exact date:", log_aoi_exact_date)

# c) AOI + date range (with optional download)
log_aoi_daterange = fe.benchFIMquery(
    raster_path = raster_path,
    boundary_path = None,
    huc8 = None,
    event_date = None,
    start_date = "2017-04-01",
    end_date = "2017-05-01",
    file_name = None,
    area = True,
    download = True,              # download all matches in this range
    out_dir = "./benchmark_downloads",
)
print("AOI + date range:", log_aoi_daterange)

# d) Direct filename download (no AOI, no dates)
log_by_filename = fe.benchFIMquery(
    raster_path = None,
    boundary_path = None,
    huc8 = None,
    event_date = None,
    start_date = None,
    end_date = None,
    file_name = "BENCHMARK_FIM_03020202_20170501.tif",  # example name
    area = False,               # ignored when no AOI is provided
    download = True,
    out_dir = "./benchmark_downloads",
)
print("Direct filename download:", log_by_filename)
