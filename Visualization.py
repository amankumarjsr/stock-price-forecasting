from plotly import graph_objs as go
import json
import plotly


def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
    fig.layout.update(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        width=1600,
        height=600,
        title_text="Raw Stock Prices",
        xaxis_rangeslider_visible=True,
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def plot_raw_data2(data, date, predicted_data):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Actual Price"))
    fig2.add_trace(
        go.Scatter(
            x=date["Date"], y=predicted_data["Predicted"], name="Predicted Price"
        )
    )
    fig2.layout.update(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        width=1600,
        height=600,
        title_text="Future Price Forecasting",
        xaxis_rangeslider_visible=True,
    )
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON2


def plot_raw_data3(data, forecast, predicted_data):
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=data["Date"][-forecast:],
            y=data["Close"][-forecast:],
            name="Actual Stock Price",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=data["Date"][-forecast:],
            y=predicted_data["Predicted"],
            name="Predicted Stock Price",
        )
    )
    fig3.layout.update(
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        width=1600,
        height=600,
        title_text="Actual Vs Predicted Price with shifting Method",
        xaxis_rangeslider_visible=True,
    )
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON3
