import streamlit as st

st.set_page_config(page_title="色轮选色器", page_icon="🎨")

st.title("🎨 色轮选色器")

# 颜色选择器控件
selected_color = st.color_picker("选择颜色", "#FF7F50")

# 将Hex转为RGB和十进制值
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_decimal(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

rgb = hex_to_rgb(selected_color)
decimal_value = hex_to_decimal(selected_color)

# 显示当前颜色
st.markdown(
    f"<div style='width:100px;height:100px;background-color:{selected_color};border-radius:10px;border:1px solid #ccc'></div>",
    unsafe_allow_html=True
)

# 显示色值
st.write("**RGB 值：**", f"{rgb}")
st.write("**十六进制：**", f"`{selected_color.upper()}`")
st.write("**十进制：**", f"`{decimal_value}`")
