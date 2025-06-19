import streamlit as st

st.set_page_config(page_title="色轮选色器", layout="wide")

st.title("🎨 色轮")

st.markdown("使用色轮选择和谐的颜色调色板，并输出对应色值。")

col1, col2 = st.columns([1, 2])

with col1:
    selected_color = st.color_picker("主色", "#D88DC6")

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

    rgb = hex_to_rgb(selected_color)
    decimal_value = hex_to_decimal(selected_color)
    similar_colors = generate_similar_colors(selected_color)

    st.markdown(f"""
        <div style='display:flex;align-items:center;margin-top:10px'>
            <div style='width:30px;height:30px;border-radius:50%;background:{selected_color};margin-right:10px'></div>
            <span style='font-size:20px;font-weight:bold'>{selected_color.upper()}</span>
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
    st.markdown("##### 选择主色（或使用下方滑块调整明度）")
    st.write("（Streamlit 暂不支持真实色轮，但可以拓展）")

    brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.05)
    # 在这里可以用 colorsys 或 PIL 来调节实际颜色明度（可选）

