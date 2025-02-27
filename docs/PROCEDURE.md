# Standard Operating Procedure (SOP) for Utah Organoids DataJoint Pipelines

## Overview

The **Utah Organoids DataJoint pipeline** facilitates **cerebral organoid characterization** and **electrophysiology (ephys) data analysis**. This guide provides step-by-step instructions for accessing and using the pipeline.

### Pipeline Components

- **Organoid Generation Pipeline**: Manages metadata for organoid generation protocols, tracking the process from induced pluripotent stem cells (iPSCs) to single neural rosettes (SNRs) to mature organoids.

- **Array Ephys Pipeline**: Handles ephys data analysis, managing metadata and raw data related to probes and ephys recordings. It also includes preprocessing, spike sorting, and quality metrics computations.

## Access

1. **Request Access**: Contact the DataJoint support team for an account.
2. **Log in**: Use DataJoint credentials to access:
     - works.datajoint.com
     - Organoids SciViz (metadata entry)
     - Database connections

## Organoid Generation Pipeline

3. **Metadata Entry**:
    1. Log into [Organoids SciViz](https://organoids.datajoint.com/) with your DataJoint credentials (username and password).
    2. Enter data in the corresponding sections:
        - `User` page → if you are a new experimenter, register a new experimenter.
        - `Lineage` page → create new “Lineage” and “Sequence” and submit.
        - `Stem Cell` page → register new “Stem Cell” data.
        - `Induction` page → add new “Induction Culture” and “Induction Culture Condition”
        - `Post Induction` page → add new “Post Induction Culture” and “Post Induction Culture Condition”
        - `Isolated Rosette` page → add new “Isolated Rosette Culture” and “Isolated Rosette Culture Condition”
        - `Organoid` page → add new “Organoid Culture” and “Organoid Culture Condition”
        - `Experiment` page → log new experiments performed on a particular organoid
            - Include metadata: organoid ID, datetime, experimenter, condition, etc.
            - Provide the experiment data directory — the relative path to where the acquired data is stored.

## Array Ephys Pipeline

4. **Upload Data to the Cloud**:
    1. Ensure data follows the [file structure guidelines](https://github.com/dj-sciops/utah_organoids/blob/main/docs/DATA_ORGANIZATION.md).
    2. Request Axon credentials from the DataJoint support team.
    3. Set up your local machine (if you haven't already):
        1. [Install the pipeline code](https://github.com/dj-sciops/utah_organoids/blob/main/docs/INSTALLATION_AND_CONFIGURATION_INSTRUCTIONS.md#installation-of-the-pipeline-codebase).  
        2. Configure axon settings ([Cloud upload configuration](https://github.com/dj-sciops/utah_organoids/blob/main/docs/CLOUD_UPLOAD_CONFIGURATION_INSTRUCTIONS.md)).  
    4. Upload data via the [cloud upload notebook](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/CREATE_new_session_with_cloud_upload.ipynb) using either:
        1. Jupyter Notebook Server:
            - Open a terminal or command prompt.
            - Activate the `utah_organoids` environment with `conda activate utah_organoids`.
            - Ensure `Jupyter` is installed in the `utah_organoids` environment. If not, install it by running `conda install jupyter`.
            - Navigate to the `utah_organoids/notebooks` directory in the terminal.
            - Run `jupyter notebook` in the terminal which will open the Jupyter notebook web interface.
            - Click on the notebook there (`CREATE_new_session_with_cloud_upload.ipynb`) and follow the instructions to upload your data to the cloud.
            - Note: to execute each code cell sequentially, press `Shift + Enter` on your keyboard or click "Run".
            - Close the browser tab and stop Jupyter with `Ctrl + C` in the terminal when you are done with the upload and notebook.
        2. Visual Studio Code (VS Code):
            - Install VS Code and the Python extension.
            - Select the kernel for the notebook by clicking on the kernel name `utah_organoids` in the top right corner of the notebook.
            - Open the `CREATE_new_session_with_cloud_upload.ipynb` notebook in VS Code.
            - Click on the "Run Cell" button in the top right corner of each code cell to execute the code.
            - Follow the instructions in the notebook to upload your data to the cloud.

5. **Define an `EphysSession`** (i.e. a time-window for ephys analysis)
    1. Log into [works.datajoint.com](works.datajoint.com)  and navigate to the `Notebook` tab.
    2. Open and execute [CREATE_new_session.ipynb](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/CREATE_new_session.ipynb).
    3. Define a time window for analysis:
        - **For LFP Analysis**: Set `session_type` to `lfp` for automatic analysis.
        - **For Spike Sorting Analysis**: Set `session_type` to `spike_sorting`, and create an `EphysSessionProbe` to store probe information, including the channel mapping. This triggers probe insertion detection automatically. For spike sorting, you will need to manually select the spike sorting algorithm and parameter set to run in the next step.

6. **Run Spike Sorting Analysis**
    1. Manually select a spike-sorting algorithm and parameter set (this is called to create a `ClusteringTask` in the pipeline):
        - Go to [works.datajoint.com](works.datajoint.com) → `Notebook` tab
        - Open [CREATE_new_clustering_paramset.ipynb](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/CREATE_new_clustering_paramset.ipynb) and follow the instructions.
        - Open [CREATE_new_clustering_task.ipynb](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/CREATE_new_clustering_task.ipynb) to assign parameter set to an `EphysSession`.
        - The spike sorting process will run automatically.
        - Follow the [download spike sorting results](#8-download-spike-sorting-results-to-your-local-machine) to retrieve results.

7. **Explore LFP & Spike Sorting Results**
    1. Go to [works.datajoint.com](works.datajoint.com) → `Notebook` tab
    2. Open [EXPLORE_array_ephys.ipynb](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/EXPLORE_array_ephys.ipynb) to analyze ephys results.
    3. Open [EXPLORE_quality_metrics.ipynb](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/EXPLORE_quality_metrics.ipynb) to examine unit quality metrics.

8. **Download Spike Sorting Results to Your Local Machine**
    2. Request Axon credentials from the DataJoint support team.
    3. Set up your local machine (if you haven't already):
        1. [Install the pipeline code](https://github.com/dj-sciops/utah_organoids/blob/main/docs/INSTALLATION_AND_CONFIGURATION_INSTRUCTIONS.md#installation-of-the-pipeline-codebase).  
        2. Configure axon settings ([Cloud upload configuration](https://github.com/dj-sciops/utah_organoids/blob/main/docs/CLOUD_UPLOAD_CONFIGURATION_INSTRUCTIONS.md)).  
    4. Download spike sorting results via the [DOWNLOAD_spike_sorted_data.ipynb](https://github.com/dj-sciops/utah_organoids/blob/main/notebooks/CREATE_new_session_with_cloud_upload.ipynb) using either:
        1. Jupyter Notebook Server:
            - Open a terminal or command prompt.
            - Activate the `utah_organoids` environment with `conda activate utah_organoids`.
            - Ensure `Jupyter` is installed in the `utah_organoids` environment. If not, install it by running `conda install jupyter`.
            - Navigate to the `utah_organoids/notebooks` directory in the terminal.
            - Run `jupyter notebook` in the terminal which will open the Jupyter notebook web interface.
            - Click on the notebook there (`DOWNLOAD_spike_sorted_data.ipynb`) and follow the instructions to download results.
            - Note: to execute each code cell sequentially, press `Shift + Enter` on your keyboard or click "Run".
            - Close the browser tab and stop Jupyter with `Ctrl + C` in the terminal when you are done with the upload and notebook.
        2. Visual Studio Code (VS Code):
            - Install VS Code and the Python extension.
            - Select the kernel for the notebook by clicking on the kernel name `utah_organoids` in the top right corner of the notebook.
            - Open the `DOWNLOAD_spike_sorted_data.ipynb` notebook in VS Code.
            - Click on the "Run Cell" button in the top right corner of each code cell to execute the code.
            - Follow the instructions in the notebook to download spike sorting results.

## Troubleshooting

For help, refer to the [Troubleshooting Guide](TROUBLESHOOTING.md), which provides solutions to common issues encountered during pipeline setup and execution. If you need further assistance, contact the DataJoint support team.
