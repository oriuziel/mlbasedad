import pandas as pd
import numpy as np
import copy

class DataPreparation:
    def __init__(self, directory_to_read, directory_to_save):
        """
        Reads ADNI data, cleans it up, organizes it for the following stage of data processing, and saves the prepared data and its dictionary.
        Args:
            directory_to_read : Directory of ADNIMERGE.csv. 
            directory_to_save : Directory to save the prepared data.
        Returns:
            Saves preprocessed data as df_prepared.csv at directory_to_save.
            Saves dictionary for columns of preprocessed data as df_cols_prepared.csv at directory_to_save.
        """
        self.directory_to_read = directory_to_read
        self.directory_to_save = directory_to_save
    
    def read(self):
        """
        Read the raw data.
        """
        self.df_raw = pd.read_csv(self.directory_to_read, low_memory=False)

    def initialize_df(self):
        """
        Initialize self.df. Preparation operation will be applied to self.df.
        """
        self.df = copy.deepcopy(self.df_raw)

    def remove_unwanted_baseline_columns(self):
        """
        Remove unwanted baseline columns.
        """
        unwanted_cols = self.df.columns[60:]
        unwanted_cols = [z for z in unwanted_cols if z not in ['Month_bl']]
        self.df = self.df_raw.drop(unwanted_cols, axis=1, inplace=False)

    def fix_terminology(self):
        """
        Fix the terminology in data cells.
        """
        self.df.replace({'Unknown':pd.NA}, inplace=True)
        self.df.replace({'m0':'bl'}, inplace=True)
        self.df.replace({'y1':'m12'}, inplace=True)
    
    def convert_csf_to_LowMidHigh(self):
        """
        CSF data is censored. When the measurement is greater or less than a certain value, the cell data contains "<" or ">". 
        We add a new column, "LowMidHigh", for each csf biomarker to indicate the censoring status, and get rid of "<" and ">" signs in actual measurement columns.
        """
        csf_cols = ['ABETA', 'TAU', 'PTAU']
        for col in csf_cols: 
            self.df.insert(loc=list(self.df.columns).index(col)+1, column=col+'_LowMidHigh', value=pd.NA)
            for i in range(len(self.df)):
                if pd.isna(self.df[col].iloc[i]):
                    self.df[col+'_LowMidHigh'].iloc[i] = pd.NA
                    pass
                else:
                    self.df[col+'_LowMidHigh'].iloc[i] = 'Mid'
                    if '<' in str(self.df[col].iloc[i]):
                        self.df[col].iloc[i] = str(self.df[col].iloc[i])[1:]
                        self.df[col+'_LowMidHigh'].iloc[i] = 'Low'
                    elif '>' in str(self.df[col].iloc[i]):
                        self.df[col].iloc[i] = str(self.df[col].iloc[i])[1:]
                        self.df[col+'_LowMidHigh'].iloc[i] = 'High'

    def get_df_cols(self):
        """
        Initialize the dictionary for the columns of the preprocessed data.
        Mod : Modality of the column.
        NumCat : Indicates whether the column is numerical or categorical.
        DataType : Indicates the datatype. Usually, one of the following: Nominal, Ordinal, Discrete, Continuous. (A column that has a DataType different than the aforementioned ones is handled in a way that is unique to it, hence the DataType is also unique.)
        Dtype : Python dtype of the column (Included here for completeness. Added by a different function at a later stage.)
        """
        # 0. id 
        df_id = pd.DataFrame({'Name':['RID'], 
                                            'Mod':'Id', 'NumCat':None, 'DataType':None})
        # 1. other
        df_other = pd.DataFrame({'Name':['PTID', 
                                            'VISCODE', 
                                            'SITE', 
                                            'COLPROT', 
                                            'ORIGPROT', 
                                            'EXAMDATE', 
                                            'DX_bl', 
                                            'FLDSTRENG', 
                                            'FSVERSION', 
                                            'IMAGEUID', 
                                            'Month_bl'], 
                                                'Mod':'Other', 'NumCat':None, 'DataType':None})
        # 2. demog
        df_demog = pd.DataFrame({'Name':['AGE', 
                                            'PTGENDER', 
                                            'PTEDUCAT', 
                                            'PTETHCAT', 
                                            'PTRACCAT', 
                                            'PTMARRY'], 
                                                'Mod':'Demog', 'NumCat':'Cat', 'DataType':'Nominal'})
        df_demog.loc[0, 'NumCat'] = 'Num'
        df_demog.loc[0, 'DataType'] = 'Continuous'
        df_demog.loc[2, 'DataType'] = 'Ordinal'
        # 3. gene
        df_gene = pd.DataFrame({'Name':['APOE4'], 
                                                'Mod':'Gene', 'NumCat':'Cat', 'DataType':'Ordinal'})
        # 5. pet
        df_pet = pd.DataFrame({'Name':['FDG', 
                                        'PIB', 
                                        'AV45'], 
                                            'Mod':'Pet', 'NumCat':'Num', 'DataType':'Continuous'})
        # 4. csf
        df_lmh = pd.DataFrame({'Name':['ABETA_LowMidHigh', 
                                            'TAU_LowMidHigh', 
                                            'PTAU_LowMidHigh'], 
                                                'Mod':'Csf', 'NumCat':'CsfCat', 'DataType':'CsfOrdinal'})
        df_csf = pd.DataFrame({'Name':['ABETA', 
                                        'TAU', 
                                        'PTAU'], 
                                            'Mod':'Csf', 'NumCat':'CsfNum', 'DataType':'CsfContinuous'})
        # 7. cli
        df_cli = pd.DataFrame({'Name':['CDRSB', 
                                        'FAQ', 
                                        'EcogPtMem',
                                        'EcogPtLang',
                                        'EcogPtVisspat',
                                        'EcogPtPlan',
                                        'EcogPtOrgan',
                                        'EcogPtDivatt',
                                        'EcogPtTotal',
                                        'EcogSPMem',
                                        'EcogSPLang',
                                        'EcogSPVisspat',
                                        'EcogSPPlan',
                                        'EcogSPOrgan',
                                        'EcogSPDivatt',
                                        'EcogSPTotal'], 
                                            'Mod':'Cli', 'NumCat':'Cat', 'DataType':'Ordinal'})
        # 8. cog
        df_cog = pd.DataFrame({'Name':['ADAS11',
                                        'ADAS13',
                                        'ADASQ4',
                                        'MMSE',
                                        'RAVLT_immediate',
                                        'RAVLT_learning',
                                        'RAVLT_forgetting',
                                        'RAVLT_perc_forgetting',
                                        'LDELTOTAL',
                                        'DIGITSCOR',
                                        'TRABSCOR',
                                        'MOCA'], 
                                            'Mod':'Cog', 'NumCat':'Cat', 'DataType':'Ordinal'})
        # 6. mri
        df_mri = pd.DataFrame({'Name':['Ventricles', 
                                            'Hippocampus', 
                                            'WholeBrain', 
                                            'Entorhinal', 
                                            'Fusiform', 
                                            'MidTemp', 
                                            'ICV'], 
                                                'Mod':'Mri', 'NumCat':'Num', 'DataType':'Discrete'})
        # 9. dx
        df_dx = pd.DataFrame({'Name':['DX'], 
                                            'Mod':'Dx', 'NumCat':'DxCat', 'DataType':'DxOrdinal'})
        # Concatenate.
        self.df_cols = pd.concat([df_id, 
                                    df_other, 
                                    df_demog, 
                                    df_gene, 
                                    df_cli, 
                                    df_cog, 
                                    df_lmh, 
                                    df_csf, 
                                    df_pet, 
                                    df_mri, 
                                    df_dx]).reset_index(drop=True)

    def enforce_dtype(self, column_name, column_value, new_dtype):
        """
        Ensure that columns have the correct python dtype.
        """
        cols = self.df_cols.loc[self.df_cols[column_name]==column_value, 'Name']
        self.df[cols] = self.df[cols].astype(new_dtype)

    def add_dtype_to_df_cols(self):
        """
        Add python dtype of the columns to the data dictionary.
        """
        cols = list(self.df.columns)[11:] # No need for Id and Other.
        for col in cols:
            self.df_cols.loc[self.df_cols['Name']==col, 'Dtype'] = str(self.df[col].dtype)

    def enforce_pandas_nan(self):
        """
        Ensure that missingness can be detected by pandas.
        """
        self.df = self.df.fillna(pd.NA)
    
    def write(self):
        """
        Save the preprocessed data as df_prepared.csv at directory_to_save.
        Save the dictionary for columns of preprocessed data as df_cols_prepared.csv at directory_to_save.
        """
        self.df.to_csv(self.directory_to_save+'df_prepared.csv', index=False)
        self.df_cols.to_csv(self.directory_to_save+'df_cols_prepared.csv', index=False)

    # Apply the methods.
    read()
    initialize_df()
    remove_unwanted_baseline_columns()
    fix_terminology()
    convert_csf_to_LowMidHigh()
    get_df_cols()
    enforce_dtype('DataType', 'Nominal', 'string')
    enforce_dtype('DataType', 'Ordinal', float)
    enforce_dtype('NumCat', 'Num', float)
    enforce_dtype('NumCat', 'CsfCat', 'string')
    enforce_dtype('NumCat', 'CsfNum', float)
    enforce_dtype('NumCat', 'DxCat', 'string')
    add_dtype_to_df_cols()
    enforce_pandas_nan()
    write()

    





