Data preprocessing code for the paper [_Machine learning based multi-modal prediction of future decline toward Alzheimer’s disease: An empirical study_](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0277322), where we present an empirical study to characterize how predictable individual subjects’ future Alzheimer's Disease trajectory is, several years in advance, based on rich multi-modal data, and using modern deep learning methods. 

Our preprocessing pipeline consists of several steps. The first step is where we take care of the fundamental misconceptions in the data. In the second step, we extract the disease progression trajectories of the subjects and perform participant selection. Finally, we split the data into multiple training/validation/test splits in a stratified fashion, since the follow-up diagnosis are unbalanced. Each step has its own .py file. 

The raw data file used in preparation of this paper is 'ADNIMERGE.csv', and were obtained from the Alzheimer’s Disease Neuroimaging Initiative (ADNI) database [https://adni.loni.usc.edu](https://adni.loni.usc.edu). Applications for ADNI data use can be submitted through the ADNI website at [https://adni.loni.usc.edu/data samples/accessdata/](https://adni.loni.usc.edu/data-samples/accessdata/). You would be able to access the data in the same manner as us. We did not have any special access privileges that others would not have.

We note that ADNI database, hence 'ADNIMERGE.csv', is updated with the addition of new subjects and follow-up visits almost daily. Therefore, even if you choose the same participant selection method as us, there will be minor differences in subject characteristics, number of available follow-up visits, and missingness. We provide an additional script, 'Analyze.py', for you to analyze your version of 'ADNIMERGE.csv'.

We encourage researchers to use our preprocessing pipeline for their works, so we can have a cumulatively growing literature on early prediction of Alzheimer's. We would like our paper to serve as a baseline for others to improve upon. If you are using our data preprocessing pipeline in whole or in part, please cite:

Karaman BK, Mormino EC, Sabuncu MR, for the Alzheimer’s Disease Neuroimaging Initiative (2022) Machine learning based multi-modal prediction of future decline toward Alzheimer’s disease: An empirical study. PLoS ONE 17(11): e0277322. [https://doi.org/10.1371/journal.pone.0277322](https://doi.org/10.1371/journal.pone.0277322) 
