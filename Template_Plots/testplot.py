import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "none"
import pylectureplots as pylp

fig = go.Figure()
x = np.arange(10)
fig.add_trace(go.Scatter(x=x,y=x));

fig.update_layout(margin=dict(l=25, r=10, t=10,b=40),autosize=True)

pylp.to_html(fig)