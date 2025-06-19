import streamlit as st
import colorsys

st.set_page_config(page_title="色轮选色器", layout="wide")

st.title("色轮选色器")

st.markdown("使用色轮选择和谐的颜色调色板，并输出对应色值。")

col1, col2 = st.columns([1, 2])

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
    r_new_i = int(r_new * 255)
    g_new_i = int(g_new * 255)
    b_new_i = int(b_new * 255)
    return '#{:02X}{:02X}{:02X}'.format(r_new_i, g_new_i, b_new_i)

with col1:
    selected_color = st.color_picker("主色", "#D88DC6")

    brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.05)
    adjusted_color = adjust_brightness(selected_color, brightness)

    decimal_value = hex_to_decimal(adjusted_color)
    similar_colors = generate_similar_colors(adjusted_color)

    st.markdown(f"""
        <div style='display:flex;align-items:center;margin-top:10px'>
            <div style='width:30px;height:30px;border-radius:50%;background:{adjusted_color};margin-right:10px'></div>
            <span style='font-size:20px;font-weight:bold'>{adjusted_color.upper()}</span>
        </div>
        <p style='margin-top:5px'>十进制值：<code>{decimal_value}</code></p>
    """, unsafe_allow_html=True)

    st.markdown("##### 相近颜色")
    for c in similar_colors:
        st.markdown(f"""
        <div style='display:inline-block;width:80px;height:80px;background:{c};border-radius:6px;
                    margin:5px;text-align:center;line-height:80px;font-weight:bold;color:#333;
                    box-shadow:0 0 3px rgba(0,0,0,0.1)'>{c}</div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("##### 选择主色（或使用左侧滑块调整明度）")
    st.write("（Streamlit 暂不支持真实色轮，但可以拓展）")
