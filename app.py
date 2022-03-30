import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, send_file
from model import trained_model
from Visualization import plot_raw_data, plot_raw_data2, plot_raw_data3
from datetime import datetime
from datetime import timedelta


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/contactus", methods=["GET"])
def Contact():
    return render_template("contactus.html")


@app.route("/projects", methods=["GET"])
def projects():
    return render_template("projects.html")


@app.route("/team", methods=["GET"])
def team():
    return render_template("team.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    try:
        stock_name = request.form["stock_name"].upper()
        raw_start_date = request.form["start_date"]
        raw_end_date = request.form["end_date"]
        forecast = int(request.form["forecast"])

        start_date = raw_start_date.replace("/", "-")
        start_date = f"{raw_start_date[6:]}-{raw_start_date[0:2]}-{raw_start_date[3:5]}"
        end_date = raw_end_date.replace("/", "-")
        end_date = f"{raw_end_date[6:]}-{raw_end_date[0:2]}-{raw_end_date[3:5]}"

        # making new date columns dataframe for predicted prices
        pred_date = f"{raw_end_date[:6]}{raw_end_date[-2:]}"
        list_ = []
        for i in range(1, forecast + 1):
            current_date = pred_date
            current_date_temp = datetime.strptime(current_date, "%m/%d/%y")
            newdate = current_date_temp + timedelta(days=i)
            newdate = str(newdate.date())
            list_.append(newdate)
        pd_date = pd.DataFrame(list_, columns=["Date"])

        model = trained_model()
        graph_data, prediction = model.get_data_future(
            stock_name, start_date, end_date, forecast
        )
        steps_data = model.get_data_steps(
            graph_data, stock_name, start_date, end_date, forecast
        )

        name, url, summary = model.get_info(stock_name)
        fig1 = plot_raw_data(graph_data)
        fig2 = plot_raw_data2(graph_data, pd_date, prediction)
        fig3 = plot_raw_data3(graph_data, forecast, steps_data)

        return render_template(
            "result.html",
            data1=url,
            data2=name,
            data3=summary,
            plot1=fig1,
            plot2=fig2,
            plot3=fig3,
        )

    except Exception as ex:
        data = f"An Error have occured while predicting the data!!!"
        excep = f"Error: {ex}"

        return render_template("result.html", data2=data, error=excep)


if __name__ == "__main__":
    app.run(debug=True)
