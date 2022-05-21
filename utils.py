import streamlit as st
import math
import gpxpy
from modify_dist import run
import datetime


def get_pace(dist, time, mile=False):
    # convert datetime to sec
    if not mile:
        pace = (time/dist)/60.*1000.
    else:
        pace = (time/dist)/60.*1609.32
    pace_min = math.floor(pace)
    pace_sec = round((pace % 1) * 60)
    if (pace % 1) * 60 > 59.5:
        pace_min += 1
        pace_sec = 0
    return pace_min, pace_sec


def td_to_str(td):
    td = datetime.datetime.strptime(str(td), "%H:%M:%S")
    if td.hour != 0:
        td = td.strftime('%Hh %Mm %Ss')
    else:
        td = td.strftime('%Mm %Ss')
    td = td.replace(' 0', ' ')
    if td[0] == '0':
        td = td[1:]
    return td


def format_time(h, m, s):
    hms = [h, m, s]
    try:
        h, m, s = hms[0], hms[1], hms[2]
        if h < 0 or m < 0 or s < 0:
            return "Hours, minutes, and seconds should be >= 0. You can't travel back in time !"
        if s > 59 or m > 59:
            return "Minutes, and seconds can't exceed 59 !"
        if h == 0 and m == 0 and s == 0:
            return "You can't use instant teleport !"
        return h, m, s
    except:
        return 'Time not in the right format !'


def show():

    st.write("👉 Has it ever happened that your watch stopped or had ant malfunction during your workout, thus **losing part** of your activity?"
             " Or has it happened that due to bad GPS signal your watch recorded a **shorter distance** than your actual one? 🤔")
    st.write("👉 Imagine that, after a maximal effort, you have just broken your 10km PB but your watch only recorded 9.8km,"
             " thus failing to register your record. How would you feel?"
             " Satisfied because you know you made it but probably a little disappointed because you can't show it. 😥")
    st.write("👉 The goal of this application is to **modify** the **gpx file** of your activity in order to add the distance that"
             " has not been recorded, while leaving your original trajectory. Don't let your app lose track of your progress! ✊")
    st.write("👉 Feel free to report any bug or suggestion on [Github](https://github.com/davide97l/gpx-distance-modifier) and leave a ⭐ if you found it useful.")

    gpx_file_raw = st.file_uploader("📂 Upload your activity.gpx file", type=["gpx"], accept_multiple_files=False)
    if gpx_file_raw is None:
        return
    add = st.number_input('Distance to add (meters)', min_value=1)
    text = "How long did it take to do your {}m?".format(add)
    st.write(text)
    column1, column2, column3 = st.columns(3)
    h = column1.number_input("Hours", 0, 9999, 0)
    m = column2.number_input("Minutes", 0, 59, 30)
    s = column3.number_input("Seconds", 0, 59, 0)
    time = format_time(h, m, s)
    if type(time) == str:
        st.error(time)
        return

    h, m, s = time
    time = h * 3600 + m * 60 + s

    gpx_file = gpxpy.parse(gpx_file_raw)
    gpx_xlm, data = run(gpx_file, add, time)

    #st.write("Uploaded file: **{}**".format(gpx_file_raw.name))
    activity_name = gpx_file_raw.name.split('.')[0] + '_modified.gpx'
    st.write("Original distance **{:.2f}**m:".format(data['init_d']))
    st.write("Final distance **{:.2f}**m:".format(data['final_d']))
    st.write("Added **{}** GPS points:".format(data['add_p']))

    st.download_button(
        label="📂 Download modified GPX file",
        data=gpx_xlm,
        file_name=activity_name,
    )


if __name__ == "__main__":
    show()
