import pandas as pd

import streamlit as st
from neuralprophet import NeuralProphet
from plotly import graph_objs as go


def plot_raw_data():
    fig = go.Figure()
    try:
        fig.add_trace(go.Scatter(x=data['Year'], y=data['Value'], name="life_expectancy"))
        fig.layout.update(title_text='Time Series data with range slider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    except TypeError:
        st.text('Select stock..')


df = pd.read_csv('health_stat.csv')

countries = df[['Country']].drop_duplicates()

st.title('Life expectancy forecast')

country = st.selectbox('Select country', countries)

data = df[df['Country'] == country]
data = data[data['Variable'] == 'Total population at birth']
data = data[['Year', 'Value']]

st.write(f'Selected country: {country}')

plot_raw_data()

df_train = data.rename(columns={"Year": "ds", "Value": "y"})
model = NeuralProphet()

data_load_state = st.text('Loading data...')

with st.spinner('Wait...The model is being trained..'):
    metrics = model.fit(
        df_train, freq='A'
    )
    future = model.make_future_dataframe(df=df_train, periods=10, n_historic_predictions=len(df_train))
    forecast = model.predict(future)
    data_load_state.text('Loading data... done!')
    st.write(f'Forecast plot for  days')
    fig1 = model.plot(forecast, xlabel="Year", ylabel="Life expectancy")

    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = model.plot_components(forecast)

    st.write(fig2)
