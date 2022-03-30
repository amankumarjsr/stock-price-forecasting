from tracemalloc import start
from keras.models import load_model
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class trained_model:
    def get_info(self, input_code_):
        info = yf.Ticker(input_code_)
        inf = info.info
        name = inf["shortName"]
        url = inf["logo_url"]
        summary = inf["longBusinessSummary"]
        return name, url, summary

    def get_data_future(self, input_code_, start_date_, end_date_, forecast):

        data = yf.download(input_code_, start=start_date_, end=end_date_)
        data.reset_index(inplace=True)
        df = pd.DataFrame(data["Close"])

        pred_list = []

        model = load_model("keras_model.h5")

        past_100_days = df.tail(100)
        scaler = MinMaxScaler(feature_range=(0, 1))
        input_data = scaler.fit_transform(past_100_days)

        r_input_data = np.array(input_data)
        r1_input_data = r_input_data.reshape(1, 100, 1)

        y_prediction = model.predict(r1_input_data)
        y_pred = scaler.inverse_transform(y_prediction)
        pred_list.append(y_pred[0])

        r_input_data = np.append(r_input_data, y_prediction)

        for item in range(forecast):
            r_input_data = r_input_data[-100:]
            r1_input_data = r_input_data.reshape(1, 100, 1)

            y_prediction = model.predict(r1_input_data)

            y_pred = scaler.inverse_transform(y_prediction)
            pred_list.append(y_pred[0])

            r_input_data = np.append(r_input_data, y_prediction)

        y_predicted = pd.DataFrame(pred_list, columns=["Predicted"])

        return data, y_predicted

    def get_data_steps(self, df, input_code_, start_date_, end_date_, forecast):

        df.reset_index(inplace=True)
        df = pd.DataFrame(df["Close"])

        model = load_model("keras_model.h5")

        past_data = df.tail(100 + forecast)

        scaler_steps = MinMaxScaler(feature_range=(0, 1))
        input_data_steps = scaler_steps.fit_transform(past_data)

        X_test = []
        y_test = []

        for i in range(100, input_data_steps.shape[0]):
            X_test.append(input_data_steps[i - 100 : i])
            y_test.append(input_data_steps[i, 0])

        X_test, y_test = np.array(X_test), np.array(y_test)

        y_pred_steps = model.predict(X_test)
        y_predicted_steps = scaler_steps.inverse_transform(y_pred_steps)
        y_predicted_steps = pd.DataFrame(y_predicted_steps, columns=["Predicted"])
        return y_predicted_steps


# a = trained_model()
# b = a.get_data("HDFC.NS", "2015-03-01", "2022-03-15", 10)
# print(b)
