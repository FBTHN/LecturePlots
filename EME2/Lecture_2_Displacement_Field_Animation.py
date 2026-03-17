import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "none"
from plotly.subplots import make_subplots
from pathlib import Path



# ==========================================
# 1. SETUP DATA AND PARAMETERS
# ==========================================
xr = [0, 4]
yr = [-1.5, 1.5]
xgrd = np.arange(xr[0], xr[1] + 0.5, 0.5)
ygrd = np.arange(yr[0], yr[1] + 0.5, 0.5)
n = 100  

# Deformation Function
w0 = 0.1

def uf(x, y): return - w0 * ((x-xr[0])+(x-xr[1]))*y
def vf(x, y): return w0 * (x-xr[0])*(x-xr[1])

# Interpolation functions (t goes from 0 to 1)
def def_x(x, y, t=0.0): return x + t * uf(x, y)
def def_y(x, y, t=0.0): return y + t * vf(x, y)

# Colors
col_inner     = 'rgba(102, 102, 102, 1.0)' 
col_outer     = 'rgba(0, 0, 0, 1.0)'
col_poly      = 'rgba(204, 230, 255, 1.0)' 
col_poly_ref = 'rgba(230, 230, 230, 1.0)' 

# ==========================================
# 2. CREATE FIGURE & TRACK TRACES
# ==========================================
fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference Configuration", "Momentarily Configuration"))

# We need to track the exact index of the traces on the RIGHT plot 
# so the slider knows exactly which lines to animate.
dynamic_trace_indices = []
current_trace_index = 0

# Base Polygon points
x_poly = np.concatenate([
    np.linspace(xr[0], xr[1], n), np.full(n, xr[1]),
    np.linspace(xr[1], xr[0], n), np.full(n, xr[0])
])
y_poly = np.concatenate([
    np.full(n, yr[0]), np.linspace(yr[0], yr[1], n),
    np.full(n, yr[1]), np.linspace(yr[1], yr[0], n)
])

# Poly (Left - Static)
fig.add_trace(go.Scatter(x=x_poly, y=y_poly, fill='toself', fillcolor=col_poly_ref, line=dict(width=0), showlegend=False, hoverinfo='skip'), row=1, col=1)
current_trace_index += 1

# Poly (Right - Dynamic) - Starts at t=0.0
fig.add_trace(go.Scatter(x=def_x(x_poly, y_poly, 0.0), y=def_y(x_poly, y_poly, 0.0), fill='toself', fillcolor=col_poly, line=dict(width=0), showlegend=False, hoverinfo='skip'), row=1, col=2)
dynamic_trace_indices.append(current_trace_index)
current_trace_index += 1

# Vertical lines (x-lines)
for i, x_val in enumerate(xgrd):
    color = col_outer if i == 0 or i == len(xgrd) - 1 else col_inner
    width = 2 if i == 0 or i == len(xgrd) - 1 else 1
    x_line = np.full(n, x_val)
    y_line = np.linspace(yr[0], yr[1], n)
    
    # Left (Static)
    fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', line=dict(color=color, width=width), showlegend=False, hoverinfo='skip'), row=1, col=1)
    current_trace_index += 1
    
    # Right (Dynamic)
    fig.add_trace(go.Scatter(x=def_x(x_line, y_line, 0.0), y=def_y(x_line, y_line, 0.0), mode='lines', line=dict(color=color, width=width), showlegend=False, hoverinfo='skip'), row=1, col=2)
    dynamic_trace_indices.append(current_trace_index)
    current_trace_index += 1

# Horizontal lines (y-lines)
for i, y_val in enumerate(ygrd):
    color = col_outer if i == 0 or i == len(ygrd) - 1 else col_inner
    width = 2 if i == 0 or i == len(ygrd) - 1 else 1
    x_line = np.linspace(xr[0], xr[1], n)
    y_line = np.full(n, y_val)
    
    # Left (Static)
    fig.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', line=dict(color=color, width=width), showlegend=False, hoverinfo='skip'), row=1, col=1)
    current_trace_index += 1
    
    # Right (Dynamic)
    fig.add_trace(go.Scatter(x=def_x(x_line, y_line, 0.0), y=def_y(x_line, y_line, 0.0), mode='lines', line=dict(color=color, width=width), showlegend=False, hoverinfo='skip'), row=1, col=2)
    dynamic_trace_indices.append(current_trace_index)
    current_trace_index += 1

# Outline reference on right plot (Static - dashed line)
fig.add_trace(go.Scatter(x=[xr[0], xr[1], xr[1], xr[0], xr[0]], y=[yr[0], yr[0], yr[1], yr[1], yr[0]], mode='lines', line=dict(color='black', width=1, dash='dash'), showlegend=False, hoverinfo='skip'), row=1, col=2)
current_trace_index += 1

# ==========================================
# 3. BUILD THE SLIDER STEPS
# ==========================================
t_values = np.linspace(0, 1, 21) # Creates 21 frames from t=0.0 to t=1.0
steps = []

for t in t_values:
    step_x = []
    step_y = []
    
    # 1. Calculate Poly Right for this t
    step_x.append(def_x(x_poly, y_poly, t))
    step_y.append(def_y(x_poly, y_poly, t))
    
    # 2. Calculate x-lines Right for this t
    for x_val in xgrd:
        x_line = np.full(n, x_val)
        y_line = np.linspace(yr[0], yr[1], n)
        step_x.append(def_x(x_line, y_line, t))
        step_y.append(def_y(x_line, y_line, t))
        
    # 3. Calculate y-lines Right for this t
    for y_val in ygrd:
        x_line = np.linspace(xr[0], xr[1], n)
        y_line = np.full(n, y_val)
        step_x.append(def_x(x_line, y_line, t))
        step_y.append(def_y(x_line, y_line, t))
        
    # Package into a restyle command targeting ONLY the dynamic right-side traces
    step = dict(
        method="restyle",
        args=[
            {"x": step_x, "y": step_y}, 
            dynamic_trace_indices  
        ],
        label=f"{t:.2f}"
    )
    steps.append(step)

sliders = [dict(
    active=0, # Default active state is t=0.0
    currentvalue={
        "font": {"color": "white", "size": 5} 
    },
    pad={"t": 30},
    font=dict(color="rgba(0,0,0,0)"), # make numbers below slider invisible
    ticklen=0, # hide ticks
    steps=steps
)]

# ==========================================
# 4. FORMAT AXES, FONTS, AND TITLES
# ==========================================
for j in [1, 2]:
    fig.update_xaxes(range=[-2, 6], dtick=1, gridcolor='rgba(204,204,204,0.5)', zeroline=True, zerolinecolor='black', zerolinewidth=1, 
                     title_text="$x$", title_standoff=5, row=1, col=j)
    fig.update_yaxes(range=[-2, 2], dtick=1, gridcolor='rgba(204,204,204,0.5)', zeroline=True, zerolinecolor='black', zerolinewidth=1, 
                     title_text="$y$", title_standoff=5, scaleanchor=f"x{j}", scaleratio=1, row=1, col=j)

# Shift subplot titles up slightly
for annotation in fig['layout']['annotations']:
    annotation['yshift'] = 20

fig.update_layout(margin=dict(l=50, r=50, t=50,b=50),autosize=True,font=dict(size=16),title_font=dict(size=18),sliders=sliders)

# Save html
html = fig.to_html(
    full_html=True,
    include_plotlyjs='cdn',     # smaller file; loads Plotly from CDN
    config = {"responsive": True},
    include_mathjax='cdn'
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

output_path = Path(__file__).resolve().with_suffix('.html')
with open(output_path, "w", encoding="utf-8") as f:
    f.write(fullscreen_html)

