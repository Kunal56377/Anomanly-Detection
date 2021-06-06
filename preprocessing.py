import pandas as pd
import numpy as np

''' Raw data is corrupted data. So to handle corrupted below processing done. 
1) Chacter "X"  is replaced in TransactionAmount Column with value present in adjusent column anc created new
column TransactionAmount1 
2) TransactionAmount is null and 4th Column is null, We dropped those. Beucase that data I dont think 
add in any value right now
3) Dropped TransactionAmount becuse we have copy of that Column in TransactionAmount1
4) Dropped 4th column and MerchantId column. Two Id are not at same time. and  MerchantId columns 
has many nan values as well
5) Caluculate the Std deviation and mean as per Accountid or user
6) Std deviation was null for some account becuase only one record was present replace those by mean deviation
7) Based on 3 Std Deviation detect Anomaly Detection
8) Addned new column in processed csv with new columns data is anomaly or not 

'''



class Preprocessor:
    def __init__(self):
        self.file_object = pd.read_csv("Data\\data.csv",names=['AccountId','MerchantId','TransactionAmount','Meaningless'])
    
    def load_data(self):
        self.file_object  = self.file_object.drop(self.file_object[self.file_object['MerchantId'].isnull() &  self.file_object['TransactionAmount'].isnull()].index,axis = 0)
        self.file_object['TransactionAmount1'] = np.where(self.file_object['TransactionAmount'].str.strip()=="X",self.file_object['Meaningless'],self.file_object['TransactionAmount'])
        self.file_object.drop(['TransactionAmount'],inplace= True,axis=1)
        self.file_object.drop(['Meaningless'],inplace= True,axis=1)
        self.file_object.drop(['MerchantId'],inplace= True,axis=1)
        self.file_object['TransactionAmount1'] = np.where(self.file_object['TransactionAmount1'].isnull(),0,self.file_object['TransactionAmount1'])
        self.file_object['mean'] = self.file_object['AccountId']
        self.file_object['dev'] = self.file_object['AccountId']
        self.file_object['TransactionAmount1'] = self.file_object['TransactionAmount1'].astype(float) 
        Modified_data_mean = self.file_object.groupby('AccountId')['TransactionAmount1'].mean().to_dict()
        Modified_data_dev = self.file_object.groupby('AccountId')['TransactionAmount1'].std().to_dict()
        self.file_object['mean'] = self.file_object['mean'].map(Modified_data_mean)
        self.file_object['dev'] = self.file_object['dev'].map(Modified_data_dev)
        devation_mean_population = self.file_object['dev'].mean()
        self.file_object['dev'] = np.where(self.file_object['dev'].isnull(),devation_mean_population,self.file_object['dev'])
        minimim_Trasaction_perAccount = self.file_object.groupby('AccountId')['TransactionAmount1'].min().to_dict()
        maximum_Trasaction_perAccount = self.file_object.groupby('AccountId')['TransactionAmount1'].max().to_dict()
        self.file_object['minimim_Trasaction'] = self.file_object['AccountId'] 
        self.file_object['maximum_Trasaction'] = self.file_object['AccountId'] 
        self.file_object['minimim_Trasaction'] = self.file_object['minimim_Trasaction'].map(minimim_Trasaction_perAccount)
        self.file_object['maximum_Trasaction'] = self.file_object['maximum_Trasaction'].map(maximum_Trasaction_perAccount)
        self.file_object['maximum_to_minimum_ratio'] = self.file_object['maximum_Trasaction']/self.file_object['minimim_Trasaction']
        self.file_object['Anomaly'] = np.where( (self.file_object['TransactionAmount1']<=(self.file_object['mean'] - 3*self.file_object['dev'])),'Yes','No')
        self.file_object['Anomaly'] = np.where( (self.file_object['TransactionAmount1']>=(self.file_object['mean'] + 3*self.file_object['dev'])),'Yes',self.file_object['Anomaly'])
        self.file_object.to_csv("Processed_Data\\ProcessedData.csv")
        Modified_data1 =  self.file_object[['AccountId','mean','dev']]
        Modified_data1 = Modified_data1.drop_duplicates(subset=["AccountId","mean","dev"])
        Modified_data1.to_csv("Processed_Data\\MeanandDevaiationPerCustomer.csv")

    
    def meanofTransction(value,self):
        return self.file_object[(self.file_object['AccountId']==value)]['TransactionAmount1'].mean()