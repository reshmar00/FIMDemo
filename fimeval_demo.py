# continuing from previous step, if user have intend to use FIM Evaluation Framework for evaluation
import fimeval as fe
from pathlib import Path
"""
01. Case Directory Structure
------------------------
The important understanding is for multi-case evaluation, the user need to have a main directory where each subfolder is a test case containing model FIMs to be evaluated.
For single case evaluation, user can provide the path to that single case folder.

Parameters
----------
Main_dir: root folder where each subfolder is a *test case*.
Example structure:
  Main_dir/
      HUC11110203_AR/
          model_fim_1.tif
          model_fim_2.tif
      HUC11110204_TX/
          model_fim_1.tif

For instance,
Main_dir = "path/to/your/Main_dir"

02. Positioning benchmark FIMs for evaluation
------------------------------
Now from Step 01, user will access the benchmark FIM for each case. Finding each case by running QUERY is precise way. However, the automation based on
area overlap, FIM tier and resolution priority is ongoing.

and finally make a dictionary mapping each test case folder to the benchmark FIM filename obtained from Step 01.

benchmark_dict = {
    "HUC11110203_AR": "benchmark_01.tif"
    "HUC11110204_TX": "benchmark_02.tif"
}

03. Evaluation methods
------------------------------
While accessing the benchmark FIM, It will get all the benchmark boundary along with this, and use this boundary as `AOI` method for evaluation.

However, If user explicitly mention other methods like `smallest_extent` or `convex_hull`, FIMeval will use that method instead of benchmark AOI.

Evaluation methods:
"smallest_extent"  -> intersection of all FIM extents
"convex_hull"      -> convex hull around all FIM extents
"AOI"              -> use AOI shapefile as evaluation domain

method_name = "smallest_extent"  #for example

04. Other parameters
------------------------------
output_dir = "./path/to/output" # Optional: Directory to save evaluation results

Optional: user PWB (Permanent Water Bodies) dataset if not using the default one for the US.
PWB_dir = "./path/to/PWB"

target_crs = "EPSG:5070" # Optional: Target CRS (e.g., EPSG code or proj string, here for example is Albers Equal Area)

Optional: Target resolution in meters. If not provided, FIMeval can use the coarsest resolution among the inputs.
target_resolution = 10
"""

# Evaluation usage examples
# Basic evaluation using default method & default PWB
fe.EvaluateFIM(
    Main_dir=Main_dir,
    benchmark_dict=benchmark_dict,
)

# Enforce target CRS / resolution and user AOI
fe.EvaluateFIM(
    Main_dir=Main_dir,
    method_name=method_name,
    target_resolution=target_resolution,
    target_crs=target_crs,
    PWB_dir=PWB_dir,
    output_dir=output_dir,
    benchmark_dict=benchmark_dict,
)

#Other results after evaluation

#For using default benchmark FIMs, method_name is AOI
#Print contingency maps (true/false positives, etc.)
fe.PrintContingencyMap(Main_dir, method_name, output_dir) 

#Plot evaluation metrics (CSI, POD, FAR, etc.)
fe.PlotEvaluationMetrics(Main_dir, method_name, output_dir)

#FIM evaluation with building footprints
countryISO = "US"  # e.g., "US" for United States
building_footprint = "./path/to/your/building_footprint.shp"

fe.EvaluationWithBuildingFootprint(
    Main_dir,
    method_name,
    output_dir,
    country=countryISO,
    geeprojectID="supathdh",
)
#OR use local building footprint, using benchmark FIM, We are working on automating this step.
fe.EvaluationWithBuildingFootprint(
    Main_dir,
    method_name,
    output_dir,
    building_footprint=building_footprint,
)
