import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import colorsys

st.set_page_config(page_title="二维H-S色彩选择器", layout="centered")

st.title("🎨 二维 H-S 色彩选择器 + 明度调节")

# 画一个H-S色彩平面图
h_range = 360
s_range = 100
img = np.zeros((s_range, h_range, 3))

for i in range(s_range):      # S从100%到0%
    for j in range(h_range):  # H从0到360度
        h = j / 360
        s = 1 - i / 100  # 注意反转坐标轴，顶部饱和度高
        v = 1.0         # 明度先设1
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        img[i, j] = [r, g, b]

fig, ax = plt.subplots(figsize=(9, 3))
ax.imshow(img, aspect='auto', origin='lower')
ax.set_xticks([0, 60, 120, 180, 240, 300, 360])
ax.set_xticklabels(['0°', '60°', '120°', '180°', '240°', '300°', '360°'])
ax.set_yticks([0, 25, 50, 75, 100])
ax.set_yticklabels(['100%', '75%', '50%', '25%', '0%'])
ax.set_xlabel("色相 (Hue)")
ax.set_ylabel("饱和度 (Saturation)")
ax.set_title("点击色块选择色相和饱和度")

st.pyplot(fig)

# 用户输入色相和饱和度
h = st.slider("色相 H (0°~360°)", 0, 360, 300)
s = st.slider("饱和度 S (0%~100%)", 0, 100, 70)

v = st.slider("明度 V (0%~100%)", 0, 100, 90)

# 计算当前颜色
h_norm = h / 360
s_norm = s / 100
v_norm = v / 100
r, g, b = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)
hex_color = '#{:02X}{:02X}{:02X}'.format(int(r*255), int(g*255), int(b*255))

st.markdown(f"""
<div style="display:flex; justify-content:center; align-items:center; margin-top:20px; gap:15px;">
    <div style="width:80px; height:80px; border-radius:12px; background:{hex_color}; box-shadow: 0 0 10px rgba(0,0,0,0.2);"></div>
    <div style="font-size:24px; font-weight:bold; color:#333;">{hex_color}</div>
</div>
""", unsafe_allow_html=True)

st.write("你现在选择的颜色，明度可单独调整，灵活控制色调和亮度。")

