import streamlit as st
import streamlit.components.v1 as components
import colorsys
import re
from typing import Tuple, List

# ======================
# 配置与初始化
# ======================
st.set_page_config(page_title="色轮选色器", layout="centered", page_icon="🎨")

# ======================
# 工具函数
# ======================
@st.cache_data
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@st.cache_data
def hex_to_decimal(hex_color: str) -> int:
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

@st.cache_data
def generate_similar_colors(hex_color: str) -> List[str]:
    r, g, b = hex_to_rgb(hex_color)
    variants = []
    for i in [-20, 0, 20]:
        r2 = min(255, max(0, r + i))
        g2 = min(255, max(0, g + i))
        b2 = min(255, max(0, b + i))
        variants.append(f"#{r2:02X}{g2:02X}{b2:02X}")
    return variants

@st.cache_data
def adjust_brightness(hex_color: str, brightness_factor: float) -> str:
    r, g, b = hex_to_rgb(hex_color)
    r_f, g_f, b_f = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)
    v = max(0, min(v * brightness_factor, 1))
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r_new * 255):02X}{int(g_new * 255):02X}{int(b_new * 255):02X}"

def get_text_color(hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#000000" if brightness > 140 else "#FFFFFF"

# ======================
# 状态管理
# ======================
def get_color_from_url():
    color = st.query_params.get("color", [None])[0]
    if color:
        color = color.upper()
        if re.match(r"^#[0-9A-F]{6}$", color):
            return color
    return None

if "selected_color" not in st.session_state:
    st.session_state.selected_color = "#D88DC6"

url_color = get_color_from_url()
if url_color and url_color != st.session_state.selected_color:
    st.session_state.selected_color = url_color
    st.rerun()  # 关键修复：URL颜色变化时强制刷新

current_color = st.session_state.selected_color

# ======================
# 色轮组件
# ======================
components.html(f"""
<div style='width:100%; max-width:320px; margin:0 auto; padding:15px; 
             background:#f8f8f8; border-radius:10px;'>
  <div id='picker'></div>
  <p style='text-align:center; font-size:16px; margin-top:15px; cursor:pointer;'
     onclick='navigator.clipboard.writeText("{current_color}")'>
    当前颜色: <span id='current-color' style='font-weight:bold;'>{current_color}</span>
  </p>
</div>

<script src='https://cdn.jsdelivr.net/npm/@jaames/iro@5'></script>
<script>
  const colorPicker = new iro.ColorPicker('#picker', {{
    width: Math.min(300, window.innerWidth - 40),
    color: '{current_color}',
    layout: [
      {{ component: iro.ui.Wheel }},
      {{ component: iro.ui.Slider, options: {{ sliderType: 'value' }} }}
    ]
  }});

  // 关键修复：通过Streamlit的setQueryParams触发后端更新
  colorPicker.on('color:change', function(color) {{
    const hex = color.hexString.toUpperCase();
    document.getElementById('current-color').textContent = hex;
    window.parent.postMessage({{
      type: 'streamlit:setComponentValue',
      value: hex
    }}, '*');
    
    // 更新URL但不刷新页面
    const url = new URL(window.location);
    url.searchParams.set('color', hex);
    window.history.replaceState(null, null, url.toString());
  }});
</script>
""", height=400)

# 监听前端颜色变化
color_from_js = components.declare_component("color_picker", path="./frontend")
selected_color = color_from_js(default=current_color, key="color_picker")

if selected_color != current_color:
    st.session_state.selected_color = selected_color
    st.rerun()

# ======================
# 颜色展示区
# ======================
brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01)
adjusted_color = adjust_brightness(current_color, brightness)

# 主颜色显示
st.markdown(f"""
<div style='display:flex; justify-content:center; align-items:center; gap:20px; margin:20px 0;'>
    <div style='width:80px; height:80px; border-radius:10px; background:{adjusted_color}; 
                box-shadow:0 4px 12px rgba(0,0,0,0.15);'></div>
    <div>
        <div style='font-size:24px; font-weight:bold;'>{adjusted_color}</div>
        <div style='color:#666; margin-top:5px;'>
            RGB: {hex_to_rgb(adjusted_color)} | 十进制: {hex_to_decimal(adjusted_color)}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 相近颜色
st.markdown("### 相近颜色")
similar_colors = generate_similar_colors(adjusted_color)
cols = st.columns(3)
for i, col in enumerate(cols):
    with col:
        c = similar_colors[i]
        text_color = get_text_color(c)
        st.markdown(f"""
        <div style='background:{c}; color:{text_color}; width:100%; aspect-ratio:1;
                    border-radius:10px; display:flex; justify-content:center; 
                    align-items:center; font-weight:bold;'>
            {c}
        </div>
        """, unsafe_allow_html=True)

# 使用说明
st.markdown("""
<div style='margin-top:30px; padding:15px; background:#f0f4f8; border-radius:8px;'>
    <h3 style='color:#2C3E50;'>使用说明</h3>
    <ul style='color:#555;'>
        <li>拖动色轮选择颜色，色值会自动同步</li>
        <li>点击色值代码可复制到剪贴板</li>
        <li>调整滑块改变颜色明度</li>
    </ul>
</div>
""", unsafe_allow_html=True)
