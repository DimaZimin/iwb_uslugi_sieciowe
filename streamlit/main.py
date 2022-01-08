import streamlit as st
import datetime
from datetime import date

import pandas_datareader as web
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import logging


def validate_ticker(ticker):
    try:
        web.DataReader(ticker, data_source='yahoo')
    except Exception as e:
        logging.error(e)
        return False
    return True


@st.cache
def load_data(ticker, start):
    try:
        df = web.DataReader(ticker, data_source='yahoo', start=start, end=TODAY)
        df.reset_index(inplace=True)
    except Exception as e:
        logging.info(e)
        return False
    return df


def plot_raw_data():
    fig = go.Figure()
    try:
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.layout.update(title_text='Time Series data with range slider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    except TypeError:
        st.text('Select stock..')


st.title('Stock Forecast App')

TODAY = date.today().strftime("%Y-%m-%d")

START = st.date_input('Select start day of ticker history', min_value=datetime.date(year=1990, month=1, day=1),
                      value=datetime.date(year=1999, month=1, day=1))

st.text(f'Today is: {TODAY}')

if START:
    selected_stock = st.text_input('Select ticker for prediction')
else:
    selected_stock = None
    st.text_input('Select start date first')

days = st.slider('Days of prediction:', 1, 365, value=90)


if selected_stock:
    data = load_data(selected_stock, START)
else:
    data = None
    st.text('Invalid stock ticker')

if data is not None:
    data_load_state = st.text('Loading data...')
    data_load_state.text('Loading data... done!')

    st.subheader(f'Last 5 {selected_stock} price')
    try:
        st.write(data.tail())
    except AttributeError:
        st.write('Select stock first')

    plot_raw_data()

    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    with st.spinner('Wait...The model is being trained..'):

        m.fit(df_train)
        future = m.make_future_dataframe(periods=days)
        forecast = m.predict(future)
        data_load_state.text('Loading data... done!')
        st.subheader('Forecast data')
        st.write(forecast.tail())

        st.write(f'Forecast plot for {days} years')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
