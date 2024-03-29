# ML Zoomcamp Mid-Term Project: LBW-RiskPrediction

Random Forest Model to predict risk of low weight at birth. 

## 1. Project Overview
- Created a tool to help predict the risk of low weight at birth during the course of a pregnancy. Early detection of this risk, which is still one of the leading indicators of infant mortality in the developing world, could allow to take timely action to prevent complications for the newborn.
- Cleaned and analized official records of all live births in Colombian territory during 2020.
- Optimized logistic regression, random forest and xgboost models to reach the best model.
- Built a webapp using plotly.Dash to serve the model.
- As a requirement of the ML Zoomcamp course this project had to be peer-reviewed, so I have adjusted the readme file below and the notebooks based on my classmates' valuable feedbacks. 
  
## 2. Project Description
The objective of this project is to develop a ML model to predict the risk of low weight at birth during the course of a pregnancy. Low birth weight (LBW) is a term used to describe newborns who weigh less than 2500g (5 pounds, 8 ounces). LBW can lead to serious health problems for babies and in developing countries it remains one of the leading indicators of infant mortality. Newborns who weigh less than 2500g have higher risk of malnutrition in the first year of life and are more vulnerable to infections. Studies have identified several factors associated to LBW including socio-economic context of parents, health history of the mother and medical care during pregnancy. In Colombia, there is still an incidence of over 10% of LBW in infants born each year. Therefore, this project aims to develop a tool that can serve to raise awareness about socioeconomic factors that can lead to LBW and also predict risk during the course of a pregnancy.

## 3. Dataset
![image](https://user-images.githubusercontent.com/89426444/200992845-87e45638-e065-4d78-affb-0e079cbbbabc.png)
The dataset selected for this project is a collection of the official records for all live births in Colombian territory during 2020. It was compiled by the Colombian National Department of Statistics DANE and available for download at: https://microdatos.dane.gov.co//catalog/732/get_microdata. Train.py and notebook.ipyn use the dataset in dta format (nac2020.dta). All data is
extracted from the Certificate of Live Birth for the Civil Registry (*Certificado de Nacido Vivo Antecedente para el Registro Civil*) and encoded following the instructions attached to the form available at: https://microdatos.dane.gov.co/catalog/732/related_materials.
The original dataset contained 629,402 records with data related to the birth itself - city, province, type of birth, person who delivered baby, etc - as well as of the new born - sex, gestion period, etc. and his parents - age, education levels, place of residence, marital status. 
As sugested in literature reviewed, the dataset was filtered to exclude any records with missing information. Multiple pregnancies were also excluded. After applying these criteria for inclusion - complete information and single pregnancy - 547147 records remained.

## 4. EDA
As this project not only aims to review factors that influence LBW and also provide a tool to anticipate risk during pregnancy, the Exploratory Data Analysis conducted focused on those variables that are available during pregnancy and not on those that relate to the birth or the newborn. Upon observing the 7.995% incidence of LBW in the records, it was clear that the data was unbalanced for the purpose of the study, so implementing strategies to address this issue would be required during the model selection. An analysis of feature importance was conducted to confirm that variables selected were relevant. Results of the analysis conducted are available in the notebook.ipynb file. 

## 5. Model
Different models were trained and tested to select the best performing one for the LBW risk prediciton tool. The first approach was running a logistic regression and comparing results for different sets of features as well as with and without a Synthetic Minority Oversampling Technique (SMOTE) to address the unbalanced nature of the data. The second attemp was with a random forest, tuning its parameters and training with and without SMOTE. These four models were cross-validated using ROC AUC and average_prediction scores. Finally, the third attempt was an XGBoost model with default parameters but fine tuning parameters and cross-validation became too computationally challenging. The best performing model was the random forest which was trained with the full training set, validated with the test set and pickled for use in the risk prediction app. Results of all tests of the different models are available in the notebook.ipynb file. The train.py file shows all steps to train and pickle the selected model and the predict.py file develops a function to deploy the model. Train.py and predict.py may by found in the data folder.    

## 6. Deployment
An plotly.Dash app was created to serve the model. The app provides a user form that upon submission indicates a risk of LBW during a pregnancy. The variables in the form are coded in the same way as the certificate for the live registry, so health professionals should be familiar with the different categories, for mother age, gestion period, etc. A pipenv environment within a docker app where created for deployment. After testing locally, the app was deployed to Heroku but it is no longer available online as the platform no longer offers a free tier.
![image](https://user-images.githubusercontent.com/89426444/200990897-37011c51-5e56-47d6-8c89-906db2f8ba85.png)

## 7. Instructions for running the webapp locally
The app can be replicated locally following these steps: 
1. Clone the repository
2. Open the repository and in the main folder build the docker image: `docker build -t lbw-predictor .`
3. Run the container from the image built in the previous step: `docker run -it -p 9696:9696 lbw-predictor:latest`. 
This automatically triggers the app in port 0.0.0.9696. 
