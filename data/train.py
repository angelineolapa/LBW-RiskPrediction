#Import Libraries
import pandas as pd

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score

import xgboost as xgb

import pickle

#Import data
births_df = pd.read_stata("nac2020.dta")

#Adjust variable names
births_df.columns = births_df.columns.str.lower().str.replace(' ', '_')

#Variables of interest following recommendations in articles reviewed and availability before birth
birth_vars = ["mul_parto", "t_ges", "numconsul"]
mom_vars = ["edad_madre", "est_civm", "niv_edum", "n_hijosv", "n_emb", "seg_social", "area_res"]
dad_vars = ["edad_padre", "niv_edup"]
selected_vars = birth_vars + mom_vars + dad_vars + ["peso_nac"]

#Filter dataset
births_df = births_df[selected_vars]

#Inclusion criteria

#Only newborns for which all information is available
no_area_res = births_df[births_df["area_res"]==""].index
births_df.drop(labels = no_area_res, axis=0, inplace=True)
missing_val_vars = {"peso_nac":9.0, "mul_parto":"9", "edad_madre":99.0, "est_civm":"9",
                   "niv_edum":"99", "n_hijosv":99.0, "n_emb":99.0, "edad_padre":999.0, 
                   "area_res":"9", "niv_edup":"99"}
for key in missing_val_vars.keys():
    index_drop = births_df[births_df[key]==missing_val_vars[key]].index.to_list()
    births_df.drop(labels=index_drop, axis=0, inplace=True)

#Only single pregnancies
births_df = births_df[births_df["mul_parto"]=="1"]
births_df.drop("mul_parto", axis=1, inplace=True)

#Reset Index
births_df.reset_index(inplace=True, drop=True)

#Classify final variable list in numeric and categorical
#Numeric variables
numeric_vars = ["t_ges", "numconsul", "edad_madre", "n_hijosv", "n_emb", "edad_padre"]
#Categorical variables
categorical_vars = ["est_civm", "niv_edum","seg_social", "area_res", "niv_edup"]

#Dictionary for variable names in English
var_names = {"edad_madre":"Age - mother","est_civm":"Marital status - mother", 
             "niv_edum":"Education level - mother","n_hijosv":"Living children - mother",
             "n_emb":"Previous pregnancies - mother", 
             "seg_social":"Health Insurance Regime - mother",
             "edad_padre":"Age - father", "niv_edup":"Education level - father", 
             "area_res":"Residential area - mother", "peso_nac":"Birth weight",
             "numconsul":"Pre-natal medical visits", "t_ges":"Gestation Time"}

#Category Label Dictionaries
est_civm_labels = {"1":"Cohabiting - 2Y or more", "2":"Cohabiting - less than 2Y", "3":"Divorced", 
                  "4":"Widowed", "5":"Single", "6":"Married"}
niv_edu_labels = {"01":"Preschool", "02":"Primary", "03":"Secondary", "04":"Secondary", 
                  "05":"Secondary", "06":"Non-University Higher", "07":"Non-University Higher", 
                  "08":"Non-University Higher", "09":"Undegraduate","10":"Postgraduate", 
                  "11":"Postgraduate", "12":"Postgraduate", "13":"None"}
seg_social_labels = {"1":"Contributory", "2":"Subsidized", "3":"Exception", "4":"Special", 
                     "5":"Non-insured"}
area_res_labels = {"1":"Cabecera Municipal", "2":"Centro Poblado", "3":"Rural"}

#Apply Category Label Dictionaries
births_df["est_civm"] = births_df["est_civm"].map(est_civm_labels)
births_df["niv_edum"] = births_df["niv_edum"].map(niv_edu_labels)
births_df["niv_edup"] = births_df["niv_edup"].map(niv_edu_labels)
births_df["seg_social"] = births_df["seg_social"].map(seg_social_labels)
births_df["area_res"] = births_df["area_res"].map(area_res_labels)

#Declare categorical variables as such
for var in categorical_vars:
    births_df[var] = births_df[var].astype("category")

#Define low birth weight identifier
def lbw_identifier(w):
    if w<=4:
        return 1
    else:
        return 0    
births_df["lbw"] = births_df["peso_nac"].apply(lbw_identifier)

#Divide in train, validation and test sets
#Stratified sampling will be using to account for imbalanced nature of the data
df_train_full, df_test = train_test_split(births_df, test_size=0.2, random_state=1, 
                                          stratify=births_df.lbw)

#Reset index
df_train_full.reset_index(drop=True, inplace=True) 
df_test.reset_index(drop=True, inplace=True)

#Calculate y_train, y_val and y_test variable for all sets
y_train = df_train_full.lbw.values
y_test = df_test.lbw.values

df_train_full.drop("peso_nac", axis=1, inplace=True)
df_test.drop("peso_nac", axis=1, inplace=True)
df_train_full.drop("lbw", axis=1, inplace=True)
df_test.drop("lbw", axis=1, inplace=True)

#Encoding with DictVectorizer
train_dict = df_train_full.to_dict(orient='records')
dv = DictVectorizer(sparse=False)
dv.fit(train_dict)

#Prepare feature matrix for model training
X_train = dv.transform(train_dict)

#Random Forest with parameters identified in jupyter notebook 
model = RandomForestClassifier(n_estimators=25, max_depth=10, random_state=1)
model.fit(X_train, y_train)

#Model validation
test_dict = df_test.to_dict(orient='records')
X_test = dv.transform(test_dict)
y_pred = model.predict_proba(X_test)[:, 1]

#AUC Score
print("AUC Score:", roc_auc_score(y_test, y_pred))

#Average Precision Score
print("Average Precision Score:", average_precision_score(y_test, y_pred))

#Save model for use in dashboard
import pickle
with open('model.bin', 'wb') as f_out:
   pickle.dump((dv, model), f_out)
f_out.close()