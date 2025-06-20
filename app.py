import streamlit as st
import colorsys
import numpy as np

st.set_page_config(page_title="ColorSelector", layout="centered")

# 定义颜色转换函数
def hex_to_rgb(hex_color):
    """将十六进制颜色转换为RGB元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """将RGB元组转换为十六进制颜色"""
    return f'#{r:02x}{g:02x}{b:02x}'.upper()

def hex_to_decimal(hex_color):
    """将十六进制颜色转换为十进制值"""
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

def adjust_brightness(hex_color, brightness_factor):
    """调整颜色明度"""
    r, g, b = hex_to_rgb(hex_color)
    r_f, g_f, b_f = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)
    v = max(0, min(v * brightness_factor, 1))
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
    return rgb_to_hex(int(r_new * 255), int(g_new * 255), int(b_new * 255))

def generate_similar_colors(hex_color):
    """在HSV空间生成类似色（调整色相±15度）"""
    r, g, b = hex_to_rgb(hex_color)
    r_f, g_f, b_f = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)
    similar_colors = []
    for hue_shift in [-15, 0, 15]:
        h_new = (h + hue_shift / 360) % 1
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h_new, s, v)
        similar_colors.append(rgb_to_hex(
            int(r_new * 255), int(g_new * 255), int(b_new * 255)
        ))
    return similar_colors

# 页面样式：响应式布局 + 颜色展示样式
st.markdown("""
<style>
/* 全局样式 */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 标题样式 */
.title-container {
    text-align: center;
    margin: 20px 0;
}

/* 色轮容器（居中） */
.color-wheel-container {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

/* 明度滑块容器（居中） */
.slider-container {
    display: flex;
    justify-content: center;
    margin: 20px 0;
}

/* 颜色展示区域（响应式布局） */
.color-display {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 20px;
    margin: 30px 0;
    width: 100%;
}

/* 移动端适配：小于768px时垂直排列 */
@media (max-width: 768px) {
    .color-display {
        flex-direction: column;
        align-items: center;
    }
}

/* 当前颜色区域 */
.current-color {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    max-width: 300px;
    width: 100%;
}

.color-box {
    width: 120px;
    height: 120px;
    border-radius: 8px;
    background: {color};
    box-shadow: 0 0 8px rgba(0,0,0,0.15);
    margin-bottom: 15px;
}

.color-value {
    font-size: 22px;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 5px;
}

.decimal-value {
    color: #666;
    font-size: 16px;
    text-align: center;
}

/* 近似颜色区域 */
.similar-colors {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    max-width: 500px;
    width: 100%;
}

.similar-title {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
}

.similar-boxes {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
}

.similar-box {
    background: {color};
    width: 90px;
    height: 90px;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    color: {text_color};
    font-size: 14px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
    transition: transform 0.2s;
}

.similar-box:hover {
    transform: scale(1.05);
}

/* 提示文字样式 */
.tip-container {
    max-width: 600px;
    margin: 40px auto 0;
    font-size: 16px;
    line-height: 1.6;
    color: #555;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 主界面
st.markdown(
    """
    <div class="title-container">
        <h1 style="color:#2C3E50;">ColorSelector</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# 色轮部分（使用color_picker模拟，居中显示）
with st.container():
    st.markdown("<div class='color-wheel-container'>", unsafe_allow_html=True)
    selected_color = st.color_picker("选择颜色", "#D88DC6", key="color_picker")
    st.markdown("</div>", unsafe_allow_html=True)

    # 明度调节滑块（居中显示）
    st.markdown("<div class='slider-container'>", unsafe_allow_html=True)
    brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01)
    st.markdown("</div>", unsafe_allow_html=True)

    # 计算调整后的颜色和近似色
    adjusted_color = adjust_brightness(selected_color, brightness)
    decimal_value = hex_to_decimal(adjusted_color)
    similar_colors = generate_similar_colors(adjusted_color)

    # 渲染当前颜色和近似色（响应式布局）
    # 构建当前颜色展示HTML
    current_color_html = f"""
    <div class="current-color">
        <div class="color-box" style="background:{adjusted_color}"></div>
        <div class="color-value">{adjusted_color}</div>
        <div class="decimal-value">十进制值：<code>{decimal_value}</code></div>
    </div>
    """

    # 构建近似色展示HTML
    similar_boxes_html = ""
    for c in similar_colors:
        r, g, b = hex_to_rgb(c)
        brightness_check = (r * 299 + g * 587 + b * 114) / 1000
        text_color = "#000" if brightness_check > 140 else "#fff"
        similar_boxes_html += f"""
        <div class="similar-box" style="background:{c}; color:{text_color}">{c}</div>
        """

    similar_colors_html = f"""
    <div class="similar-colors">
        <div class="similar-title">近似颜色</div>
        <div class="similar-boxes">
            {similar_boxes_html}
        </div>
    </div>
    """

    # 组合并显示响应式布局
    st.markdown(f"""
    <div class="color-display">
        {current_color_html}
        {similar_colors_html}
    </div>
    """, unsafe_allow_html=True)

    # 提示文字
    st.markdown("""
    <div class="tip-container">
        <b>使用说明：</b><br>
        - 点击色轮选择主色，或通过颜色选择器打开调色板<br>
        - 拖动明度滑块调整颜色亮度，获得更理想的色调<br>
        - 右侧近似色基于主色的色相生成，可直接用于配色方案
    </div>
    """, unsafe_allow_html=True)
