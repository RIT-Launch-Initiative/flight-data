import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.outline(label="Table of Contents")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data Loading
    If you want it for yourself: https://github.com/RIT-Launch-Initiative/flight-data/tree/main/2026/AirbrakesL1Tests
    """)
    return


@app.cell
def _():
    import pandas as pd
    from collections import namedtuple
    import json
    import matplotlib.pyplot as plt
    import numpy as np
    import requests

    plt.rcParams["figure.figsize"] = [12, 9]
    return json, namedtuple, np, pd, plt, requests


@app.cell
def _(json, namedtuple, pd, requests):
    Flight = namedtuple("Flight", ["controller_config", "params","data", "gps"])

    def our_alt(kpa, coeffs):
        x = kpa * 1000
        y = 0
        xn = 1
        for coeff in coeffs:
            y += coeff * xn
            xn *= x
        return y

    def load_flight(dir, max_rows=-1):
        response = requests.get(dir+'/controller_configuration.json')
        config = json.loads(response.content)

        data = pd.read_csv(dir+'/flight/controls_module/data.csv')[0:max_rows].astype(float)
        params_df = pd.read_csv(dir+'/flight/controls_module/params.csv').T

        coeffs = [float(params_df.loc[f'atmo{i}'].iloc[0]) for i in range(0, 6)]
        data["timestamp_from_boost__ms"] = data.timestamp__ms.map(lambda x : x - params_df.loc["timestamp_of_boost_detect__ms"].iloc[0]+500) # 0 is start of data, 250 is probably lighting, 500 is when we detected

        data["ts"] = data.timestamp_from_boost__ms/1000


        gps_df = pd.read_csv(dir+"/flight/featherweight/downloaded.csv")
        gps_df["DELTA_TIME"] = gps_df.UNIXTIME - gps_df.UNIXTIME.min()


        return Flight(config, params_df, data.set_index('ts'), gps_df.set_index("UNIXTIME"))


    return (load_flight,)


@app.cell
def _(load_flight):
    emmas = load_flight("https://raw.githubusercontent.com/RIT-Launch-Initiative/flight-data/refs/heads/main/2026/AirbrakesL1Tests/Emmas")
    zoeys = load_flight("https://raw.githubusercontent.com/RIT-Launch-Initiative/flight-data/refs/heads/main/2026/AirbrakesL1Tests/Zoeys")
    johns = load_flight("https://raw.githubusercontent.com/RIT-Launch-Initiative/flight-data/refs/heads/main/2026/AirbrakesL1Tests/Johns", 1437)
    byperson = {"emma":emmas, "zoey":zoeys, "john":johns}
    return byperson, emmas, johns, zoeys


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Control Freak

    ## Stats
    """)
    return


@app.cell(hide_code=True)
def _(emmas, johns, mo, np, zoeys):
    mo.md(rf"""
    | Flight | Parameter | Value | Unit |
    | -- | -- | -- | -- |
    | Emmas | Max Accel. | {np.round(np.sqrt(emmas.data.accel_x__m_s2**2 + emmas.data.accel_y__m_s2**2 + emmas.data.accel_z__m_s2**2).max()/9.81, 2)} | g 
    | Zoeys | Max Accel. | {np.round(np.sqrt(zoeys.data.accel_x__m_s2**2 + zoeys.data.accel_y__m_s2**2 + zoeys.data.accel_z__m_s2**2).max()/9.81, 2)} | g | 
    | Johns | Max Accel. | {np.round(np.sqrt(johns.data.accel_x__m_s2**2 + johns.data.accel_y__m_s2**2 + johns.data.accel_z__m_s2**2).max()/9.81, 2)} | g |
    | Emmas | GPS Apogee | {emmas.gps["Altitude AGL"].max()} | ft |
    | Zoeys | GPS Apogee | {zoeys.gps["Altitude AGL"].max()} | ft |
    | Johns | GPS Apogee | {johns.gps["Altitude AGL"].max()} | ft |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Control Freak Accelerometers
    """)
    return


@app.cell
def _(emmas, johns, np, plt, zoeys):
    a_fig, a_axs=plt.subplots(4, 1, figsize=(16,9))

    emmas.data.accel_x__m_s2.plot(label="Emmas", ax=a_axs[0])
    zoeys.data.accel_x__m_s2.plot(label="Zoeys", ax=a_axs[0])
    johns.data.accel_x__m_s2.plot(label="Johns", ax=a_axs[0])

    emmas.data.accel_y__m_s2.plot(label="Emmas", ax=a_axs[1])
    zoeys.data.accel_y__m_s2.plot(label="Zoeys", ax=a_axs[1])
    johns.data.accel_y__m_s2.plot(label="Johns", ax=a_axs[1])


    emmas.data.accel_z__m_s2.plot(label="Emmas", ax=a_axs[2])
    zoeys.data.accel_z__m_s2.plot(label="Zoeys", ax=a_axs[2])
    johns.data.accel_z__m_s2.plot(label="Johns", ax=a_axs[2])


    np.sqrt(emmas.data.accel_x__m_s2**2 + emmas.data.accel_y__m_s2**2 + emmas.data.accel_z__m_s2**2).plot(label = "Emmas", ax=a_axs[3])
    np.sqrt(zoeys.data.accel_x__m_s2**2 + zoeys.data.accel_y__m_s2**2 + zoeys.data.accel_z__m_s2**2).plot(label = "Zoeys", ax=a_axs[3])
    np.sqrt(johns.data.accel_x__m_s2**2 + johns.data.accel_y__m_s2**2 + johns.data.accel_z__m_s2**2).plot(label = "Johns", ax=a_axs[3])

    a_axs[0].set_ylabel("Accel. X Axis (m/s²)")
    a_axs[0].set_xlabel("")
    a_axs[1].set_ylabel("Accel. Y Axis (m/s²)")
    a_axs[1].set_xlabel("")
    a_axs[2].set_ylabel("Accel. Z Axis (m/s²)")
    a_axs[2].set_xlabel("")
    a_axs[3].set_ylabel("Accel. Magnitude (m/s²)")
    a_axs[3].set_xlabel("")


    plt.xlabel("Timestamp (s)")

    a_axs[0].set_xlim(0,100)
    a_axs[1].sharex(a_axs[0])
    a_axs[2].sharex(a_axs[0])
    a_axs[3].sharex(a_axs[0])

    def accel_forward(x): 
        return x / 9.8
    def accel_inverse(x): 
        return x * 9.8


    ax_secax = a_axs[0].secondary_yaxis('right', functions=(accel_forward, accel_inverse))
    ax_secax.set_ylabel("Accel X (g)")
    ay_secax = a_axs[1].secondary_yaxis('right', functions=(accel_forward, accel_inverse))
    ay_secax.set_ylabel("Accel Y (g)")
    az_secax = a_axs[2].secondary_yaxis('right', functions=(accel_forward, accel_inverse))
    az_secax.set_ylabel("Accel Z (g)")
    am_secax = a_axs[3].secondary_yaxis('right', functions=(accel_forward, accel_inverse))
    am_secax.set_ylabel("Accel Mag (g)")


    a_axs[0].legend()
    a_fig.suptitle("Raw Accelerometer")
    a_fig.tight_layout()
    a_fig
    return a_axs, a_fig


@app.cell
def _(a_axs, a_fig):
    a_axs[0].set_xlim(0,15)
    a_fig.suptitle("Raw Accelerometer (Boost to Coast)")
    a_fig
    return


@app.cell
def _(a_axs, a_fig):
    a_axs[0].set_xlim(0,2)
    a_fig.suptitle("Raw Accelerometer (Boost")
    a_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Control Freak Gyroscopes
    """)
    return


@app.cell
def _(emmas, johns, np, plt, zoeys):
    g_fig, g_axs=plt.subplots(4, 1, figsize=(16,9))

    emmas.data.gyro_x__dps.plot(label="Emmas", ax=g_axs[0])
    zoeys.data.gyro_x__dps.plot(label="Zoeys", ax=g_axs[0])
    johns.data.gyro_x__dps.plot(label="Johns", ax=g_axs[0])

    emmas.data.gyro_y__dps.plot(label="Emmas", ax=g_axs[1])
    zoeys.data.gyro_y__dps.plot(label="Zoeys", ax=g_axs[1])
    johns.data.gyro_y__dps.plot(label="Johns", ax=g_axs[1])


    emmas.data.gyro_z__dps.plot(label="Emmas", ax=g_axs[2])
    zoeys.data.gyro_z__dps.plot(label="Zoeys", ax=g_axs[2])
    johns.data.gyro_z__dps.plot(label="Johns", ax=g_axs[2])

    np.sqrt(emmas.data.gyro_x__dps**2 + emmas.data.gyro_y__dps**2 + emmas.data.gyro_z__dps**2).plot(label = "Emmas", ax=g_axs[3])
    np.sqrt(zoeys.data.gyro_x__dps**2 + zoeys.data.gyro_y__dps**2 + zoeys.data.gyro_z__dps**2).plot(label = "Zoeys", ax=g_axs[3])
    np.sqrt(johns.data.gyro_x__dps**2 + johns.data.gyro_y__dps**2 + johns.data.gyro_z__dps**2).plot(label = "Johns", ax=g_axs[3])


    g_axs[0].set_ylabel("Gyro X Axis (deg/s)")
    g_axs[0].set_xlabel("")
    g_axs[1].set_ylabel("Gyro Y Axis (deg/s)")
    g_axs[1].set_xlabel("")
    g_axs[2].set_ylabel("Gyro Z Axis (deg/s)")
    g_axs[2].set_xlabel("")
    g_axs[3].set_ylabel("Gyro Magnitude (deg/s)")
    g_axs[3].set_xlabel("")



    g_axs[0].set_xlim(0,100)
    g_axs[1].sharex(g_axs[0])
    g_axs[2].sharex(g_axs[0])
    g_axs[3].sharex(g_axs[0])


    plt.xlabel("Timestamp (s)")
    plt.legend()
    g_fig.suptitle("Raw Gyroscope")
    g_fig.tight_layout()
    g_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Control Freak Barometer
    """)
    return


@app.cell
def _(emmas, johns, plt, zoeys):
    barom_fig, barom_axs=plt.subplots(2, 1, figsize=(16,9))


    barom_axs[0].set_ylabel("Pressure (kPa)")
    barom_axs[0].set_xlabel("")
    barom_axs[1].set_ylabel("Temperature (C)")
    barom_axs[1].set_xlabel("Time (s)")

    barom_axs[1].sharex(barom_axs[0])

    emmas.data.pressure__kpa.plot(label="Emma", ax=barom_axs[0])
    zoeys.data.pressure__kpa.plot(label="Zoey", ax=barom_axs[0])
    johns.data.pressure__kpa.plot(label="Johm", ax=barom_axs[0])

    emmas.data.temp__C.plot(label="Emma", ax=barom_axs[1])
    zoeys.data.temp__C.plot(label="Zoey", ax=barom_axs[1])
    johns.data.temp__C.plot(label="Johm", ax=barom_axs[1])

    def temp_forward(x): 
        return x*1.8 + 32
    def temp_inverse(x): 
        return (x-32)/1.8


    barom_secax = barom_axs[1].secondary_yaxis('right', functions=(temp_forward, temp_inverse))
    barom_secax.set_ylabel("Temperature (F)")

    barom_axs[0].set_title("Air Pressure")
    barom_axs[1].set_title("Air Temperature")
    barom_axs[0].legend()
    barom_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Control Freak Kalman Filter
    """)
    return


@app.cell
def _(byperson, plt):
    k_fig, k_axs = plt.subplots(6,1, figsize=(12,18))
    for kperson, kflight in byperson.items():
        kflight.data.e_alt__m.plot(ax=k_axs[0], label=kperson.title())
        kflight.data.e_vel__m_s.plot(ax=k_axs[1], label=kperson.title())
        kflight.data.e_acc__m_s2.plot(ax=k_axs[2], label=kperson.title())
        kflight.data.e_bias.plot(ax=k_axs[3], label=kperson.title())
        kflight.data.innovation0.plot(ax=k_axs[4], label=kperson.title())
        kflight.data.innovation1.plot(ax=k_axs[5], label=kperson.title())

    k_axs[0].set_title("Estimated Altitude (m)")
    k_axs[1].set_title("Estimated Velocity (m/s)")
    k_axs[2].set_title("Estimated Acceleration (m/s2)")
    k_axs[3].set_title("Estimated Bias")
    k_axs[4].set_title("Innovation (Barom)")
    k_axs[5].set_title("Innovation (IMU)")

    k_fig.tight_layout()
    k_fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    let the record show that innovation is lagging by one sample after boost
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Featherweight
    """)
    return


@app.cell
def _(emmas, johns, np, plt, zoeys):
    gps_fig, gps_ax = plt.subplots()

    emmas.gps.set_index("DELTA_TIME")["ALT"].plot(label=f"Emma:  Apo: {np.round(emmas.gps["Altitude AGL"].max(), 2)} ft", ax = gps_ax)
    zoeys.gps.set_index("DELTA_TIME")["ALT"].plot(label=f"Zoey:    Apo: {np.round(zoeys.gps["Altitude AGL"].max(), 2)} ft", ax = gps_ax)
    johns.gps.set_index("DELTA_TIME")["ALT"].plot(label=f"John:    Apo: {np.round(johns.gps["Altitude AGL"].max(), 2)} ft", ax = gps_ax)

    offset = emmas.gps.ALT.min()
    def forward(x): return x - offset
    def inverse(x): return x + offset
    secax = gps_ax.secondary_yaxis('right', functions=(forward, inverse))

    plt.title("GPS Altitude ASL")
    plt.xlabel("Time (s)")
    plt.ylabel("GPS Altitude ASL (ft)")
    plt.legend()
    return


@app.cell
def _(emmas, johns, plt, zoeys):
    # gps_3d_ax = plt.figure().add_subplot(projection='3d')
    gps_3d_fig, gps_3d_axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
    gps_3d_axs[0].view_init(elev=20, azim=-75)   # Isometric view
    gps_3d_axs[1].view_init(elev=90, azim=-90)    # Top-down view

    for ax in gps_3d_axs:
        ax.plot(emmas.gps.LON, emmas.gps.LAT, emmas.gps.ALT, label='Emmas')
        ax.plot(zoeys.gps.LON, zoeys.gps.LAT, zoeys.gps.ALT, label='Zoeys')
        ax.plot(johns.gps.LON, johns.gps.LAT, johns.gps.ALT, label='Johns')

    gps_3d_axs[0].set_title("GPS Position (Isometric)")
    gps_3d_axs[1].set_title("GPS Position (Top Down)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    gps_3d_fig.tight_layout()
    plt.legend()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Flight Computer Configurations
    """)
    return


@app.cell
def _(emmas):
    emmas.controller_config
    return


@app.cell
def _(zoeys):
    zoeys.controller_config
    return


@app.cell
def _(johns):
    johns.controller_config
    return


if __name__ == "__main__":
    app.run()
