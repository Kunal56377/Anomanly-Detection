import pandas as pd

class Predict:
    def __init__(self):
        pass

    def predict_anomaly(self,Accid,trans):
        data = pd.read_csv("Processed_Data\\MeanandDevaiationPerCustomer.csv");
        
        mean_p = data['mean'].mean()
        devation_p =  3 * data['dev'].mean()
        data = data.set_index('AccountId')
        if (Accid in data.index):
            mean = float(data.iloc[:Accid][:1]['mean'])
            dev = float(data.iloc[:Accid][:1]['dev'] * 3)
            result = "No"
            if ((trans <= (mean - dev)) or (trans >= (mean + dev))):
                result = "Yes"
                return result 
            
            return result 
        else:
            print('Kunal')
            result = "No"
            if ((trans <= (mean_p - devation_p )) or (trans >= (mean_p + devation_p))):
                result = "Yes"
                return result 
            
            return result 


        
        
