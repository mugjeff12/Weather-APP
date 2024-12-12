import pandas as pd
from flask import Flask,render_template
import numpy as np

stations_data = pd.read_csv("data_small/stations.txt",skiprows=17)
station_columns = stations_data.columns
stations_data=stations_data[[station_columns[0],station_columns[1]]]
app=Flask(__name__)
#variable = "Hello there"
@app.route('/')
def home():
    return render_template('Main.html', data=stations_data.to_html())

@app.route('/api/v1/<station>/<date>')
def about(station,date):
    df =  pd.read_csv("data_small/TG_STAID"+str(station).zfill(6)+".txt" ,skiprows=20, parse_dates=["    DATE"])
    columns = df.columns

    df[columns[3]] = df[columns[3]].mask(df[columns[3]] == -9999, np.nan)
    #df["ATG"] = df[columns[3]]/10
    #df["ATG"] = df["ATG"].mask(df["ATG"] == -999.9, np.nan)
    temperature=df.loc[df[columns[2]]==date][columns[3]].squeeze()/10

    return {"station":station , "date": date, "temperature":temperature }

@app.route('/api/v1/<station>')
def all_data(station):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result
@app.route('/api/v1/yearly/<station>/<year>')
def yearly(station,year):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20)
    columns = df.columns
    df[columns[2]] = df[columns[2]].astype(str)
    result=df[df[columns[2]].str.startswith(str(year))].to_dict(orient="records")
    return result

if __name__ == "__main__" :
    app.run(debug=True)