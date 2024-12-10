import pandas as pd
from flask import Flask,render_template
import numpy as np

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('Main.html')

@app.route('/api/v1/<station>/<date>')
def about(station,date):
    df =  pd.read_csv("data_small/TG_STAID"+str(station).zfill(6)+".txt" ,skiprows=20, parse_dates=["    DATE"])
    columns = df.columns

    df[columns[3]] = df[columns[3]].mask(df[columns[3]] == -9999, np.nan)
    #df["ATG"] = df[columns[3]]/10
    #df["ATG"] = df["ATG"].mask(df["ATG"] == -999.9, np.nan)
    temperature=df.loc[df[columns[2]]==date][columns[3]].squeeze()/10

    return {"station":station , "date": date, "temperature":temperature }

if __name__ == "__main__" :
    app.run(debug=True)