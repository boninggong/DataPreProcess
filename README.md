# DataPreProcess
Pre-processing both the #NowPlaying-RS as well as InCarMusic datasets so they can be used by the modified version of the CARSKit (https://github.com/boninggong/CARSKitModified) to create initial recommendation lists. 

The #NowPlaying-RS dataset is left out in this repository because of its size. It can be downloaded from https://zenodo.org/record/3248543. Please put the extracted raw data files in _\data\nprs\\_ in order to execute these scripts.

See https://github.com/boninggong/Re-rankSystem for instructions for where the resulting files should be put to use the re-rank system. 

WARNING: The original dataset contains millions of listening events, so executing the pre-process scripts takes several hours. 
