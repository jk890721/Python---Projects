# The prediction of whether the price will go up or down tomorrow
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, accuracy_score, precision_score
from sklearn.ensemble import RandomForestClassifier

TSMC = yf.Ticker("TSM")
TSMC = TSMC.history(period="max")
# print(TSMC)

# print(TSMC.index)

# print(TSMC.plot.line(y = "Close", use_index = True))

del TSMC["Dividends"]
del TSMC["Stock Splits"]
# print(TSMC)

TSMC["Tomorrow"] = TSMC["Close"].shift(-1)
TSMC["Target"] = (TSMC["Tomorrow"] > TSMC["Close"]).astype(int)  # astype = round up
# print(TSMC["Target"])

# delete the date before certain date which we are not gonna do in this project
# TSMC = TSMC.loc["1990-01-01":].copy()


# Trained the model 
model = RandomForestClassifier(n_estimators = 150, min_samples_split = 100, random_state = 1)
# print(model)

train = TSMC.iloc[:-100]
test = TSMC.iloc[-100:]

predictors = ["Close", "High", "Low", "Open", "Volume"]
model.fit(train[predictors], train["Target"])

preds = model.predict(test[predictors])

preds = pd.Series(preds, index = test.index)


# print(preds)
# print(precision_score(test["Target"], preds))

combined = pd.concat([test["Target"], preds], axis = 1)
# combined.plot()

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index = test.index, name = "Predictions")
    combined = pd.concat([test["Target"], preds], axis = 1)
    return combined


def backtest(data, model, predictors, start = 2500, step = 250):
    all_predictions = []
    
    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)
    return pd.concat(all_predictions)

predictions = backtest(TSMC, model, predictors)
op = predictions["Predictions"].value_counts()
# print(op)

# print(precision_score(predictions["Target"], predictions["Predictions"]))

# print(predictions["Target"].value_counts() / predictions.shape[0])

# Adding additional predictors to the model

horizons = [5, 10, 20, 60, 120] #各個均線
new_predictors = []

for horizon in horizons:
    rolling_averages = TSMC.rolling(horizon).mean()

    ratio_column = f"Close_Ratio_{horizon}"
    TSMC[ratio_column] = TSMC["Close"] / rolling_averages["Close"]

    trend_column = f"Trend_{horizon}"
    TSMC[trend_column] = TSMC.shift(1).rolling(horizon).sum()["Target"]

    new_predictors += [ratio_column, trend_column]

# print(TSMC)

TSMC = TSMC.dropna()
# print(TSMC)

model = RandomForestClassifier(n_estimators = 170, min_samples_split = 100, random_state = 1)
def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict_proba(test[predictors])[:,1]
    preds[preds >= .55] = 1
    preds[preds < .55] = 0
    preds = pd.Series(preds, index = test.index, name = "Predictions")
    combined = pd.concat([test["Target"], preds], axis = 1)
    return combined

predictions = backtest(TSMC, model, new_predictors)
print(predictions["Predictions"].value_counts())

accuracy = accuracy_score(predictions["Target"], predictions["Predictions"])
mae = mean_absolute_error(predictions["Target"], predictions["Predictions"])
rmse = np.sqrt(mean_squared_error(predictions["Target"], predictions["Predictions"]))
mse = mean_squared_error(predictions["Target"], predictions["Predictions"])


print(f"Accuracy: {accuracy * 100:.2f}%")
print(precision_score(predictions["Target"], predictions["Predictions"]))
# print(f"Mean Absolute Error : {mae}")
# print(f"Root Mean Square Error: {rmse}")
# print(f"Mean Squared Error (MSE): {mse}")



