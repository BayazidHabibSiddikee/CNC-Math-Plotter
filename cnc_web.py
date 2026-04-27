"""
Streamlit Web App for CNC Math Equation Plotter
Works with your existing Draw class from new.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# ==================== COPY YOUR DRAW CLASS HERE ====================
# (Modified to return data instead of launching Tkinter)

class Draw:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.last_xc = None
        self.last_yc = None
        self.last_t = None
    
    def _store_result(self, xc, yc, t):
        """Store the result instead of showing it"""
        self.last_xc = xc
        self.last_yc = yc
        self.last_t = t
        return xc, yc, t
    
    def circle(self, radius=None):
        r = radius if radius is not None else self.r   
        t = np.linspace(0, 2*np.pi, 120)
        xc = self.x + r*np.cos(t)
        yc = self.y + r*np.sin(t)
        return self._store_result(xc, yc, t)
    
    def heart_curve(self):
        t = np.linspace(0, 2*np.pi, 300)
        xc = self.x + 16 * (np.sin(t))**3
        yc = self.y + 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        return self._store_result(xc, yc, t)

    def petal_rose(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 1*np.pi, 250)
        r_val = r * np.cos(5 * t)
        x = self.x + r_val * np.cos(t)
        y = self.y + r_val * np.sin(t)
        return self._store_result(x, y, t)

    def lissajous(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 200)
        xc = self.x + r * np.sin(t)
        yc = self.y + r * np.sin(2 * t)
        return self._store_result(xc, yc, t)

    def butterfly(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 10*np.pi, 600)
        expr = np.exp(np.cos(t)) - 2*np.cos(4*t) - np.sin(t/12)**5
        x = self.x + r * np.sin(t) * expr
        y = self.y + r * np.cos(t) * expr
        return self._store_result(x, y, t)

    def spiral(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 8*np.pi, 800)
        x = self.x + (r/10) * t * np.cos(t)
        y = self.y + (r/10) * t * np.sin(t)
        return self._store_result(x, y, t)
    
    def cardioid(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 300)
        r_val = r * (1 + np.cos(t))
        x = self.x + r_val * np.cos(t)
        y = self.y + r_val * np.sin(t)
        return self._store_result(x, y, t)
    
    def astroid(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 300)
        x = self.x + r * np.cos(t)**3
        y = self.y + r * np.sin(t)**3
        return self._store_result(x, y, t)
    
    def epitrochoid(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 500)
        R, r_small, d = r, r/3, r/2
        x = self.x + (R + r_small) * np.cos(t) - d * np.cos((R + r_small)/r_small * t)
        y = self.y + (R + r_small) * np.sin(t) - d * np.sin((R + r_small)/r_small * t)
        return self._store_result(x, y, t)
    
    def hypotrochoid(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 500)
        R, r_small, d = r, r/4, r/2
        x = self.x + (R - r_small) * np.cos(t) + d * np.cos((R - r_small)/r_small * t)
        y = self.y + (R - r_small) * np.sin(t) - d * np.sin((R - r_small)/r_small * t)
        return self._store_result(x, y, t)
    
    def rhodonea(self, radius=None, petals=7):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 400)
        r_val = r * np.cos(petals * t)
        x = self.x + r_val * np.cos(t)
        y = self.y + r_val * np.sin(t)
        return self._store_result(x, y, t)
    
    def limacon(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 300)
        a, b = r, r * 0.5
        r_val = a + b * np.cos(t)
        x = self.x + r_val * np.cos(t)
        y = self.y + r_val * np.sin(t)
        return self._store_result(x, y, t)
    
    def cycloid(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 4*np.pi, 400)
        x = self.x + r * (t - np.sin(t))
        y = self.y + r * (1 - np.cos(t))
        return self._store_result(x, y, t)
    
    def deltoid(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 2*np.pi, 300)
        x = self.x + r * (2*np.cos(t) + np.cos(2*t))
        y = self.y + r * (2*np.sin(t) - np.sin(2*t))
        return self._store_result(x, y, t)
    
    def logarithmic_spiral(self, radius=None):
        r = radius if radius is not None else self.r
        t = np.linspace(0, 4*np.pi, 500)
        r_val = (r/20) * np.exp(0.2 * t)
        x = self.x + r_val * np.cos(t)
        y = self.y + r_val * np.sin(t)
        return self._store_result(x, y, t)


# ==================== HELPER FUNCTIONS ====================

def export_to_c_header(xc, yc, t, name):
    """Generate C header file content"""
    x_list = xc.tolist() if hasattr(xc, 'tolist') else list(xc)
    y_list = yc.tolist() if hasattr(yc, 'tolist') else list(yc)
    
    content = f"""#ifndef {name.upper().replace(' ', '_')}_H
#define {name.upper().replace(' ', '_')}_H

#define NUM_POINTS {len(x_list)}

typedef struct {{
    float x;
    float y;
}} Point2D;

Point2D cnc_path[] = {{
"""
    
    for i in range(len(x_list)):
        content += f"    {{{x_list[i]:.6f}f, {y_list[i]:.6f}f}}"
        if i < len(x_list) - 1:
            content += ","
        content += "\n"
    
    content += f"""
}};

#endif // {name.upper().replace(' ', '_')}_H
"""
    return content


def plot_curve(xc, yc, title="CNC Toolpath"):
    """Create matplotlib figure"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(xc, yc, 'b-', linewidth=2)
    ax.scatter([xc[0]], [yc[0]], color='green', s=100, zorder=5, label='Start')
    ax.scatter([xc[-1]], [yc[-1]], color='red', s=100, zorder=5, label='End')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('X (mm)', fontsize=12)
    ax.set_ylabel('Y (mm)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.axis('equal')
    ax.legend()
    return fig


# ==================== STREAMLIT APP ====================

st.set_page_config(page_title="CNC Math Plotter", layout="wide", page_icon="🤖")

st.title("🤖 2-Axis CNC Math Equation Plotter")
st.markdown("Generate toolpaths for parametric curves with downloadable C arrays")

# Sidebar - Curve Selection
st.sidebar.header("🎨 Curve Selection")

curve_options = {
    "Circle": "circle",
    "Heart Curve": "heart_curve",
    "Petal Rose": "petal_rose",
    "Lissajous (Infinity)": "lissajous",
    "Butterfly": "butterfly",
    "Spiral": "spiral",
    "Cardioid": "cardioid",
    "Astroid": "astroid",
    "Epitrochoid": "epitrochoid",
    "Hypotrochoid": "hypotrochoid",
    "Rhodonea (Rose)": "rhodonea",
    "Limaçon": "limacon",
    "Cycloid": "cycloid",
    "Deltoid": "deltoid",
    "Logarithmic Spiral": "logarithmic_spiral"
}

selected_curve = st.sidebar.selectbox("Select Curve", list(curve_options.keys()))
curve_method = curve_options[selected_curve]

# Parameters
st.sidebar.header("⚙️ Parameters")
center_x = st.sidebar.number_input("Center X", value=0.0, step=1.0)
center_y = st.sidebar.number_input("Center Y", value=0.0, step=1.0)
radius = st.sidebar.number_input("Radius/Size", value=10.0, step=1.0, min_value=0.1)

# Special parameters for some curves
if curve_method == "rhodonea":
    petals = st.sidebar.slider("Number of Petals", 3, 12, 7)

generate_button = st.sidebar.button("🚀 Generate Toolpath", type="primary", use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

if generate_button:
    with st.spinner(f"Generating {selected_curve}..."):
        # Create Draw instance
        drawer = Draw(center_x, center_y, radius)
        
        # Call the appropriate method
        try:
            if curve_method == "rhodonea":
                xc, yc, t = drawer.rhodonea(petals=petals)
            else:
                method = getattr(drawer, curve_method)
                xc, yc, t = method()
            
            # Store in session state
            st.session_state.xc = xc
            st.session_state.yc = yc
            st.session_state.t = t
            st.session_state.curve_name = selected_curve
            
            st.success(f"✅ {selected_curve} generated with {len(xc)} points!")
            
        except Exception as e:
            st.error(f"Error generating curve: {str(e)}")

# Display results if available
if "xc" in st.session_state:
    with col1:
        st.subheader(f"📊 {st.session_state.curve_name} - CNC Toolpath")
        fig = plot_curve(st.session_state.xc, st.session_state.yc, st.session_state.curve_name)
        st.pyplot(fig)
        plt.close(fig)
    
    with col2:
        st.subheader("📈 Statistics")
        st.metric("Total Points", len(st.session_state.xc))
        st.metric("X Range", f"{st.session_state.xc.min():.2f} to {st.session_state.xc.max():.2f}")
        st.metric("Y Range", f"{st.session_state.yc.min():.2f} to {st.session_state.yc.max():.2f}")
        
        # Path length calculation
        dx = np.diff(st.session_state.xc)
        dy = np.diff(st.session_state.yc)
        path_length = np.sum(np.sqrt(dx**2 + dy**2))
        st.metric("Total Path Length", f"{path_length:.2f} mm")
    
    # Arrays preview
    st.subheader("🔧 CNC Arrays (Python)")
    
    col_x, col_y = st.columns(2)
    
    with col_x:
        st.text("X Coordinates (first 20)")
        x_preview = st.session_state.xc[:20].tolist()
        st.code(f"xc = {x_preview}...", language="python")
    
    with col_y:
        st.text("Y Coordinates (first 20)")
        y_preview = st.session_state.yc[:20].tolist()
        st.code(f"yc = {y_preview}...", language="python")
    
    # Download options
    st.subheader("📥 Download Options")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        # C Header file
        c_header = export_to_c_header(st.session_state.xc, st.session_state.yc, 
                                      st.session_state.t, st.session_state.curve_name)
        st.download_button(
            label="Download C Header (.h)",
            data=c_header,
            file_name=f"{st.session_state.curve_name.replace(' ', '_').lower()}.h",
            mime="text/plain"
        )
    
    with col_d2:
        # CSV file
        csv_data = "x,y\n"
        for x, y in zip(st.session_state.xc, st.session_state.yc):
            csv_data += f"{x:.6f},{y:.6f}\n"
        
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"{st.session_state.curve_name.replace(' ', '_').lower()}.csv",
            mime="text/csv"
        )
    
    with col_d3:
        # NumPy binary
        buffer = BytesIO()
        np.savez(buffer, xc=st.session_state.xc, yc=st.session_state.yc, t=st.session_state.t)
        
        st.download_button(
            label="Download NumPy (.npz)",
            data=buffer.getvalue(),
            file_name=f"{st.session_state.curve_name.replace(' ', '_').lower()}.npz",
            mime="application/octet-stream"
        )

else:
    with col1:
        st.info("👈 Select a curve from the sidebar and click 'Generate Toolpath' to get started!")
        
        # Show example
        st.subheader("Example: Circle")
        example_t = np.linspace(0, 2*np.pi, 100)
        example_x = 10 * np.cos(example_t)
        example_y = 10 * np.sin(example_t)
        fig = plot_curve(example_x, example_y, "Example: Circle (radius=10)")
        st.pyplot(fig)
        plt.close(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Available Curves")
st.sidebar.markdown("""
- **Circle**: Basic circle
- **Heart**: Valentine's heart shape
- **Petal Rose**: 5-petal flower
- **Lissajous**: Figure-8 infinity
- **Butterfly**: Intricate butterfly
- **Spiral**: Archimedean spiral
- **Cardioid**: Heart-shaped polar
- **Astroid**: 4-cusped star
- **Epitrochoid**: Spirograph flower
- **Hypotrochoid**: Inner spirograph
- **Rhodonea**: N-petal rose
- **Limaçon**: Snail shell
- **Cycloid**: Rolling wheel path
- **Deltoid**: 3-cusped curve
- **Logarithmic Spiral**: Nautilus shell
""")

st.sidebar.info("💡 Pro Tip: The C header file is ready for your microcontroller!")