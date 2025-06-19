import streamlit as st
import streamlit.components.v1 as components
import colorsys
import re

st.set_page_config(page_title="色轮选色器", layout="centered")

def get_color_from_query():
    color = st.query_params.get("color", [None])[0]
    if color and re.match(r"^#[0-9A-Fa-f]{6}$", color):
        return color.upper()
    return None

color_in_url = get_color_from_query()

if "selected_color" not in st.session_state:
    st.session_state.selected_color = "#D88DC6"

# 如果URL参数颜色和session颜色不一样，更新并刷新页面
if color_in_url and color_in_url != st.session_state.selected_color:
    st.session_state.selected_color = color_in_url
    st.experimental_rerun()

color = st.session_state.selected_color

st.markdown("""
<h1 style="text-align:center; color:#2C3E50;">🎨 色轮选色器</h1>
<p style="text-align:center; font-size:18px; color:#7F8C8D;">
拖动色轮选择颜色，页面刷新同步当前选色。
</p>
""", unsafe_allow_html=True)

components.html(f"""
<div style='width:300px; margin:0 auto; padding:10px; background:#f8f8f8; border:1px solid #ddd; border-radius:8px;'>
  <div id='picker'></div>
  <p style='text-align:center; font-size:16px; margin-top:10px;'>
    当前颜色: <span id='current-color'>{color}</span>
  </p>
</div>

<script src='https://cdn.jsdelivr.net/npm/@jaames/iro@5'></script>
<script>
  var colorPicker = new iro.ColorPicker('#picker', {{
    width: 280,
    color: '{color}',
    layout: [
      {{ component: iro.ui.Wheel }},
      {{ component: iro.ui.Slider, options: {{ sliderType: 'value' }} }}
    ]
  }});

  colorPicker.on('color:change', function(color) {{
    const hex = color.hexString.toUpperCase();
    document.getElementById('current-color').textContent = hex;
    const url = new URL(window.location);
    url.searchParams.set('color', hex);
    window.history.replaceState(null, null, url.toString());
  }});
</script>
""", height=400)

brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_decimal(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

def generate_similar_colors(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    variants = []
    for i in [-20, 0, 20]:
        r2 = min(255, max(0, r + i))
        g2 = min(255, max(0, g + i))
        b2 = min(255, max(0, b + i))
        variants.append('#{:02X}{:02X}{:02X}'.format(r2, g2, b2))
    return variants

def adjust_brightness(hex_color, brightness_factor):
    r, g, b = hex_to_rgb(hex_color)
    r_f, g_f, b_f = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)
    v = max(0, min(v * brightness_factor, 1))
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
    return '#{:02X}{:02X}{:02X}'.format(int(r_new * 255), int(g_new * 255), int(b_new * 255))

adjusted_color = adjust_brightness(color, brightness)
decimal_value = hex_to_decimal(adjusted_color)
similar_colors = generate_similar_colors(adjusted_color)

st.markdown(f"""
<div style='display:flex; justify-content:center; align-items:center; gap:15px; margin-top:15px;'>
    <div style='width:50px; height:50px; border-radius:8px; background:{adjusted_color}; box-shadow:0 0 5px rgba(0,0,0,0.15);'></div>
    <div>
        <div style='font-size:22px; font-weight:bold; color:#333;'>{adjusted_color}</div>
        <div style='color:#666; margin-top:3px; text-align:center;'>十进制值：<code style='font-size:18px;'>{decimal_value}</code></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 相近颜色")
st.markdown("<div style='display:flex; justify-content:center; gap:12px; margin-top:10px;'>", unsafe_allow_html=True)
for c in similar_colors:
    r, g, b = hex_to_rgb(c)
    brightness_check = (r*299 + g*587 + b*114) / 1000
    text_color = "#000" if brightness_check > 140 else "#fff"
    st.markdown(f"""
    <div style='
        background:{c};
        width:80px; height:80px; border-radius:10px;
        display:flex; justify-content:center; align-items:center;
        font-weight:bold; color:{text_color}; font-size:16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        user-select:none;'>
        {c}
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style='max-width:600px; margin:40px auto 0; font-size:18px; line-height:1.5; color:#555; text-align:center;'>
    <b>提示：</b>拖动色轮，颜色同步到地址栏，刷新页面更新显示。明度滑块调节明度。
</div>
""", unsafe_allow_html=True)
