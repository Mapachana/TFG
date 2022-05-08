import plotly.express as px
import pandas as pd

df = pd.DataFrame([
    dict(Task="T1", Start='2021-09-20', Finish='2021-10-04', Resource="A"),
    dict(Task="T2", Start='2021-10-05', Finish='2021-10-19', Resource="B"),
    dict(Task="T3", Start='2021-10-20', Finish='2021-11-04', Resource="C"),
    dict(Task="T4", Start='2021-11-05', Finish='2022-03-21', Resource="D"),
    dict(Task="T5", Start='2021-11-05', Finish='2022-01-24', Resource="E"),
    dict(Task="T6", Start='2022-01-25', Finish='2022-03-01', Resource="F"),
    dict(Task="T7", Start='2022-03-02', Finish='2022-05-02', Resource="G"),
    dict(Task="T8", Start='2021-09-20', Finish='2022-05-31', Resource="H")
])

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource")
fig.update_yaxes(autorange="reversed")
fig.update_layout(showlegend=False, yaxis = dict( tickfont = dict(size=16)), xaxis = dict( tickfont = dict(size=16)))
fig.show()
