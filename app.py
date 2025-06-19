import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import colorsys

st.set_page_config(page_title="联动色轮", layout="centered")

# 默认初始颜色
default_color = "#D88DC6"

# 获取 JS 中的颜色（实时同步）
hex_color = streamlit_js_eval(js_expressions="window.hexColor", key="color_picker") or default_color

# ---- 工具函数 ----
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

# ---- 色轮嵌入 ----
st.markdown("### 🎨 拖动色轮选择颜色")
st.components.v1.html(f"""
<div id="pickerContainer" style="display:flex; justify-content:center;"></div>
<script src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"></script>
<script>
    const picker = new iro.ColorPicker("#pickerContainer", {{
        width: 260,
        color: "{default_color}",
        layout: [
            {{ component: iro.ui.Wheel }},
            {{ component: iro.ui.Slider, options: {{ sliderType: 'value' }} }}
        ]
    }});
    window.hexColor = "{default_color}";
    picker.on('color:change', function(color) {{
        window.hexColor = color.hexString.toUpperCase();
        window.dispatchEvent(new Event("streamlit:rerun"));  // 触发回传
    }});
</script>
""", height=310)

# ---- 明度调整与展示 ----
brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01)

adjusted_color = adjust_brightness(hex_color, brightness)
decimal_value = hex_to_decimal(adjusted_color)
similar_colors = generate_similar_colors(adjusted_color)

# 主色显示
st.markdown(f"""
<div style="display:flex; justify-content:center; align-items:center; gap:15px; margin-top:15px;">
    <div style="width:50px; height:50px; border-radius:8px; background:{adjusted_color}; box-shadow:0 0 5px rgba(0,0,0,0.15);"></div>
    <div>
        <div style="font-size:22px; font-weight:bold; color:#333;">{adjusted_color}</div>
        <div style="color:#666; margin-top:3px; text-align:center;">十进制值：<code style="font-size:18px;">{decimal_value}</code></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 相近颜色
st.markdown("### 相近颜色")
st.markdown('<div style="display:flex; justify-content:center; gap:12px; margin-top:10px;">', unsafe_allow_html=True)
for c in similar_colors:
    r, g, b = hex_to_rgb(c)
    brightness_check = (r*299 + g*587 + b*114) / 1000
    text_color = "#000" if brightness_check > 140 else "#fff"
    st.markdown(f"""
    <div style="
        background:{c};
        width:80px; height:80px; border-radius:10px;
        display:flex; justify-content:center; align-items:center;
        font-weight:bold; color:{text_color}; font-size:16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        user-select:none;">
        {c}
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
