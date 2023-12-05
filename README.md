# NHL-Points-Predictor
An exploration of models that attempt to predict NHL players' point totals given their stats partway through the season. See predictions [here](https://nhl-points-predictor.streamlit.app/)

So far, the following models have been applied on the 2022-2023 NHL season. 
Root mean squared errors are shown, comparing each model's prediction of NHL player end-of-season points totals compared to their actual end-of-season point totals.

Simple Model: 12.74979458344329 

Linear Regression: 7.888248219171965 

Random Forest: 6.760429713877552 

Gradient Boosting: 6.520630288468742 <--- Currently in use on Streamlit website.

Where "Simple Model" is just extrapolation of points: points_end = (points/games played) * 82.
 
