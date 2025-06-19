import streamlit as st
import colorsys

st.set_page_config(page_title="色轮选色器", layout="centered")

st.markdown(
    """
    <h1 style="text-align:center; color:#2C3E50; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        🎨 色轮选色器
    </h1>
    <p style="text-align:center; font-size:18px; color:#7F8C8D; margin-bottom:40px;">
        使用色轮选择和谐的颜色调色板，并输出对应色值。
    </p>
    """,
    unsafe_allow_html=True
)

with st.container():
    left_space, main_col, right_space = st.columns([1, 6, 1])

    with main_col:
        col1, col2 = st.columns([3, 1])

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

            brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01)

            adjusted_color = adjust_brightness(selected_color, brightness)
            decimal_value = hex_to_decimal(adjusted_color)
            similar_colors = generate_similar_colors(adjusted_color)

            # 主色显示区域
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:15px; margin-top:15px;">
                <div style="width:50px; height:50px; border-radius:8px; background:{adjusted_color}; box-shadow:0 0 5px rgba(0,0,0,0.15);"></div>
                <div>
                    <div style="font-size:22px; font-weight:bold; color:#333;">{adjusted_color.upper()}</div>
                    <div style="color:#666; margin-top:3px;">十进制值：<code style="font-size:18px;">{decimal_value}</code></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 相近颜色")
            st.markdown('<div style="display:flex; gap:12px; margin-top:10px;">', unsafe_allow_html=True)
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

        with col2:
            st.markdown("""
            <div style='padding:20px; font-size:18px; line-height:1.5; color:#555;'>
                <b>选择主色：</b>使用左侧的色彩选择器挑选颜色。<br>
                <b>明度调整：</b>通过滑块调整颜色的明度，帮助您找到更合适的色调。<br><br>
                目前演示版本暂不支持真实色轮交互，后续可以扩展。
            </div>
            """, unsafe_allow_html=True)
