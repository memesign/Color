import streamlit as st
import colorsys
import base64

st.set_page_config(page_title="ColorSelector", layout="wide")

# ====================
# 工具函数
# ====================
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_decimal(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

def generate_similar_colors(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    variants = []
    for i in [-40, -20, 20]:  # 更丰富对比
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

# ====================
# UI部分
# ====================
st.markdown("""
    <div style="text-align:center;">
        <h1 style="font-family:Segoe UI; font-size:36px;">🎨 ColorSelector</h1>
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6e/Munsell_Color_Wheel.png" 
             style="max-width:300px; border-radius:50%; box-shadow:0 0 8px rgba(0,0,0,0.15);">
    </div>
    """, unsafe_allow_html=True)

# ====================
# 明度调整滑块
# ====================
st.markdown("---")
col_brightness = st.columns([1, 6, 1])[1]
with col_brightness:
    st.markdown(f"<div style='text-align:center; font-size:18px;'>明度调节 <span style='color:#c084fc;'>当前{int(100)}%</span></div>", unsafe_allow_html=True)
    brightness = st.slider("", 0.1, 1.0, 1.0, 0.01, key="bright_slider")

# ====================
# 颜色选择 + 显示
# ====================
selected_color = st.color_picker("请选择主色", "#FF6347", label_visibility="collapsed")
adjusted_color = adjust_brightness(selected_color, brightness)
decimal_value = hex_to_decimal(adjusted_color)
r, g, b = hex_to_rgb(adjusted_color)
similar_colors = generate_similar_colors(adjusted_color)

# ====================
# 主体部分：左主色 + 右类似色
# ====================
col_left, col_right = st.columns([1.5, 1])

# 左侧：主色块
with col_left:
    st.markdown("### 🎯 点选颜色")
    st.markdown(f"""
        <div style="
            width: 240px;
            height: 240px;
            border-radius: 24px;
            background: {adjusted_color};
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            margin-top: 10px;
            ">
        </div>
        <div style="font-size:18px; margin-top:20px;">
            十进制: <code>{decimal_value}</code><br>
            HEX: <code>{adjusted_color.upper()}</code><br>
            RGB: <code>({r}, {g}, {b})</code><br>
            <span style="color:#999;">点击色块可复制十进制色值</span>
        </div>
    """, unsafe_allow_html=True)

# 右侧：相近色
with col_right:
    st.markdown("### 🎨 近似色")
    for sc in similar_colors:
        r2, g2, b2 = hex_to_rgb(sc)
        st.markdown(f"""
        <div style="
            background:{sc};
            border-radius:16px;
            width: 200px;
            height: 80px;
            padding: 12px;
            margin-bottom:16px;
            color:#000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            display:flex;
            flex-direction: column;
            justify-content:center;">
            <div style="font-size:14px;">HEX: <code>{sc.upper()}</code></div>
            <div style="font-size:14px;">RGB: <code>({r2}, {g2}, {b2})</code></div>
            <button style="
                margin-top:6px;
                padding:4px 10px;
                background:white;
                border:1px solid #ccc;
                border-radius:6px;
                cursor:pointer;
                font-size:12px;">Select Color</button>
        </div>
        """, unsafe_allow_html=True)

# ====================
# 底部提示
# ====================
st.markdown("---")
st.markdown("<div style='text-align:center; color:#888;'>© 2025 ColorSelector Prototype</div>", unsafe_allow_html=True)
