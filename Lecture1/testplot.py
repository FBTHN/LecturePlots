import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "none"

fig = go.Figure()
x = np.arange(10)
fig.add_trace(go.Scatter(x=x,y=x));

fig.update_layout(margin=dict(l=25, r=10, t=10,b=40),autosize=True)


# Save html
html = fig.to_html(
    full_html=True,
    include_plotlyjs='cdn',     # smaller file; loads Plotly from CDN
    config = {"responsive": True}
)

# Wrap it in a minimal full-screen HTML template

fullscreen_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<style>
  html, body {{
    height: 100%;
    width: 100%;
    margin: 0;     /* remove default margins */
    padding: 0;
    overflow: hidden;
    background: #fff;
  }}
  
#wrap {{
        height: 100dvh;   /* works inside PowerPoint iframe */
        width: 100vw;
    }}

#wrap > div {{
        height: 100% !important;
        width: 100% !important;
    }}

.plotly-graph-div {{
        height: 100% !important;
        width: 100% !important;
    }}

</style>
</head>
<body>
    
<div id="wrap">
        {html}
    </div>

</body>
</html>"""


with open("./Lecture1/testplot.html", "w", encoding="utf-8") as f:
    f.write(fullscreen_html)

