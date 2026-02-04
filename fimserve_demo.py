"""
Example documentation for using FIMSERV to:

1. Query and download the correct benchmark FIM (and optional HAND-FIM)
   for a given HUC8 and event date using `fim_lookup`.
2. Immediately run the FIM evaluation on the outputs using `run_evaluation`.

The typical workflow is:
- Choose a HUC8 and event datetime.
- Decide where results from `fim_lookup` should be written (`out_dir`).
- Call `fim_lookup` with `run_handfim=True` to generate OWP HAND-FIM.
- Pass the same `out_dir` as `Main_dir` into `run_evaluation`.
"""

#Check in FIMSERV is installed

import subprocess
import sys

try:
    import fimserve
    print("-----\n\nfimserve is already installed!\n\n-----\n\n")
except ImportError:
    print("-----\n\nfimserve not found. Installing now...\n\n-----\n\n")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fimserve", "--prefer-binary", "--use-deprecated=legacy-resolver"])
    import fimserve
    print("-----\n\nfimserve installed successfully!\n\n-----\n\n")


import fimserve as fm

"""
Query and optionally generate HAND-FIM if not generated already for a given HUC8 and event date.

This is usually the first step in a FIMSERV-based workflow.

Parameters
----------
HUCID : str
    8-digit HUC ID for the basin of interest. In this example, "10170203".
date_input : str
    Event datetime used to search for the correct benchmark FIM.
    Format should be "YYYY-MM-DD HH:MM:SS".
run_handfim : bool
    If True, FIMSERV will look for an OWP HAND-FIM for the given HUC8
    and date. If not found, it will download the necessary inputs and
    generate the HAND-FIM automatically.
date_input : str
    Event datetime used to search for the correct benchmark FIM.
    Format should be "YYYY-MM-DD HH:MM:SS" and incase of run_handfim is true this is required to generate HAND-FIM.
start_date : str, optional
    Start date for an optional date range filter when searching for
    benchmark FIMs. Format: "YYYY-MM-DD".
end_date : str, optional
    End date for an optional date range filter when searching for
    benchmark FIMs. Format: "YYYY-MM-DD".
file_name : str, optional
    If provided, FIMSERV will download this specific benchmark FIM file
    and assume it is the correct benchmark for the case. If omitted,
    the benchmark is selected based on HUCID + date filters.
out_dir : str, optional
    Directory where `fim_lookup` will save the benchmark FIM, HAND-FIM,
    and any metadata. This same directory will later be passed to
    `run_evaluation` as `Main_dir`.
"""

# Optional: Directory where benchmark FIM and HAND-FIM will be saved
out_dir = "path/to/fimserve_case_output"

#User can pass either exact date or date range
result = fm.fim_lookup(
    HUCID="10170203",
    date_input="2019-09-19 12:00:00", # Optional event datetime--> look at the exact date/hour match for the benchmark FIM
    start_date="2019-09-18",        # optional date range start
    end_date="2019-09-20",          # optional date range end
)
print("Lookup result from fim_lookup:")
print(result)

#Once the benchmark FIM is decided, generate the OWP HAND-FIM if not already present and get the benchmark FIM filename
fm.fim_lookup(
    HUCID="10170203",
    date_input="2019-09-19 12:00:00", # Optional event datetime to run HAND-FIM generation
    run_handfim=True,               # generate HAND-FIM if not already present
    file_name=specific_benchmark_fim_filename.tif,              # from fim_look up result previous step with HUCID and date
    out_dir=out_dir,    # Optional: directory to save benchmark FIM and HAND-FIM
)
    
"""
Run the FIM evaluation; once the benchmark FIM file name is decided.

Parameters
----------
Main_dir : str
    Directory containing FIM outputs to evaluate. This should be the
    same path that was used as `out_dir` in `fim_lookup`. Typically,
    it contains:
    - benchmark FIM(s) selected from the catalog
    - OWP HAND-FIM generated when `run_handfim=True`
    - any intermediate products created by FIMSERV

Notes
-----
- `output_dir` controls where evaluation results (CSV, plots, etc.)
    are saved.
- If `shapefile_path` is None, FIMSERV will use its internal AOI
    (e.g., derived from the benchmark/FIMs) for evaluation.
- Most parameters are optional and can be left as None to use
    sensible defaults.
"""
#Use the right combination of parameters as needed, it is almost similar to FIMeval EvaluateFIM function mentioned [**FIM Evaluation Framework**](https://github.com/sdmlua/fimeval).
fm.run_evaluation(
    Main_dir=Main_dir,
    output_dir="./fimserve_eval_results",
    shapefile_path=None,
    PWB_dir=None,
    building_footprint=None,
    target_crs=None,
    target_resolution=None,
    method_name=None,   # default is 'AOI' inside FIMSERV
    countryISO=None,
    geeprojectID=None,
    print_graphs=True,  # generate and save contingency maps / plots
    Evalwith_BF=False,  # set True if evaluating with building footprints
)
