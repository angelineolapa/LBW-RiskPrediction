# ML Zoomcamp Mid-Term Project: LBW-RiskPrediction

Random Forest Model to predit risk of low weight at birth. App to serve model: **https://lbw-risk-predictor.herokuapp.com/**

## Project Description
The objective of this project is to develop a ML model to predict the risk of low weight at birth during the course of a pregnancy. 
Low birth weight (LBW) is a term used to describe newborn who weigh less than 2500g (5 pounds, 8 ounces). LBW can lead to serious health problems for 
babies and in developing countries it remain one of the leading indicators of infant mortality. Newborns who weigh less than 2500g have higher risk of malnutrition in the first year of life and are more vulnerable to infections. Studies have identified several factors associated to LBW including socio-economic context of parents, health history of the mother and medical care during preganancy. In Colombia, there is still an incidence of over 10% of LBW in infants born each year. Therefore, this project aims to develop a tool that can serve to raise awareness about socioeconomic factors that can lead to LBW and also predict risk during the course of a pregnancy.

## Dataset
![image](https://user-images.githubusercontent.com/89426444/200992845-87e45638-e065-4d78-affb-0e079cbbbabc.png)
The dataset selected for this project is the official record of all live births in Colombian territory during 2020. It was compiled by the Colombian National Department of Statistics DANE and available for download at: https://microdatos.dane.gov.co//catalog/732/get_microdata. Train.py and notebook.ipyn use the dataset on dta formta (nac2020.dta). All data is
extracted from the Certificate of Live Birth for the Civil Registry (*Certificado de Nacido Vivo Antecedente para el Registro Civil*) and encoded following the instructions attached to the form available at: https://microdatos.dane.gov.co/catalog/732/related_materials.
The original dataset contained 629402 records with data related to the birth itself - city, province, type of birth, person who delivered baby, etc - as well as of the new born - sex, gestion period, etc. and his parents - age, education levels, place of residence, marital status. 
As sugested in literature reviewed, the dataset was filtered to exclude any records with missing information. Multiple pregnancies were also excluded. After applying these criteria for inclusion - complete information and single pregnancy - 547147 records remained.

## EDA
As this project not only aims to review factor that influence LBW but also provide a tool to antcipate risk during pregnancy, the Exploratory Data Analysis conducted focused on those variables that are available during pregnancy and not on those that relate to the birth or the newborn. Upon observing the 7.995% incidence of LBW in the records, it was clear that the data was unbalanced for the purpose of the study so implementing strategies to address this issue would be required during the model selection. An analysis of feature importance was conducted to confirm that variables selected were relevant. Results of the analysis conducted are available in the notebook.ipynb file. 

## Model
Different models were trained and tested to select the best performing one for the LBW risk prediciton tool. The first approach was running a logistic regression and comparing results for different sets of features as well as with and without a Synthetic Minority Oversampling Technique (SMOTE) to address the unbalanced nature of the data. The second attemp was with a random forest, tuning its parameters and training with and without SMOTE. These four models were cross-validated using ROC AUC and average_prediction scores. Finally, the third attempt was an XGBoost model with default parameters but fine tuning parameters and cross-validation became too computationally challenging. The best performing model was the random forest which was trained with the full training set, validated with the test set and pickled for use in the risk prediction app. Results of all tests of the different models are available in the notebook.ipynb file. The train.py file shows all steps to train and pickle the selected model and the predict.py file develops a function to deploy the model. Train.py and predict.py may by found in the data folder.    

## Deployment
An plotly.Dash app was created to serve the model. The app provides a user form that upon submission indicates a risk of LBW during a pregnancy. The variables in the form are coded in the same way as the certificate for the live registry, so health professionals should be familiar with the different categories, for mother age, gestion period, etc. A pipenv environment within a docker app where created for deployment. After testing locally, the app was deployed to Heroku. The app is available at: https://lbw-risk-predictor.herokuapp.com/ (unfotunately it takes some time to load!).
![image](https://user-images.githubusercontent.com/89426444/200990897-37011c51-5e56-47d6-8c89-906db2f8ba85.png)

## Instructions for running locally
This repository can be cloned to run the app locally after building the docker image and running the container, which automatically triggers the app in port 0.0.0.9696. 
