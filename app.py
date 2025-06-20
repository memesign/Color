import streamlit as st
import streamlit.components.v1 as components
import colorsys
import re
from typing import Tuple, List

# ======================
# 初始化配置
# ======================
st.set_page_config(
    page_title="色轮选色器",
    layout="centered",
    page_icon="🎨"
)

# ======================
# 颜色工具函数
# ======================
@st.cache_data
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """HEX转RGB (#RRGGBB -> (R,G,B))"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@st.cache_data
def adjust_brightness(hex_color: str, brightness: float) -> str:
    """调整颜色明度"""
    r, g, b = [x / 255 for x in hex_to_rgb(hex_color)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    v = max(0, min(v * brightness, 1))
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"

def generate_similar_colors(hex_color: str) -> List[str]:
    """生成相近颜色"""
    r, g, b = hex_to_rgb(hex_color)
    variants = []
    for delta in (-20, 0, 20):
        nr = min(255, max(0, r + delta))
        ng = min(255, max(0, g + delta))
        nb = min(255, max(0, b + delta))
        variants.append(f"#{nr:02X}{ng:02X}{nb:02X}")
    return variants

# ======================
# 状态管理
# ======================
def get_color_from_query():
    """从URL获取颜色参数"""
    color = st.query_params.get("color", "")
    if re.match(r"^#[0-9A-Fa-f]{6}$", color, re.IGNORECASE):
        return color.upper()
    return None

# 初始化颜色状态
if "current_color" not in st.session_state:
    st.session_state.current_color = "#D88DC6"  # 默认颜色

# 如果URL中有颜色参数，覆盖当前颜色
url_color = get_color_from_query()
if url_color and url_color != st.session_state.current_color:
    st.session_state.current_color = url_color
    st.rerun()  # 强制刷新使新颜色生效

# ======================
# 色轮组件
# ======================
components.html(f"""
<div style="width:100%; max-width:320px; margin:0 auto; padding:20px; 
            background:#f8f8f8; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1)">
  <div id="picker"></div>
  <p style="text-align:center; margin-top:15px; font-size:16px;">
    当前颜色: <span id="current-color" style="font-weight:bold;">{st.session_state.current_color}</span>
  </p>
</div>

<script src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"></script>
<script>
  const colorPicker = new iro.ColorPicker('#picker', {{
    width: Math.min(300, window.innerWidth - 40),
    color: '{st.session_state.current_color}',
    layout: [
      {{ component: iro.ui.Wheel }},
      {{ component: iro.ui.Slider, options: {{ sliderType: 'value' }} }}
    ]
  }});

  // ✅ 用 href 强制刷新，确保 Streamlit 能感知 URL 改变
  colorPicker.on('color:change', function(color) {{
    const hex = color.hexString.toUpperCase();
    window.location.href = `?color=${{hex}}`;
  }});
</script>
""", height=420)

# ======================
# 颜色展示区
# ======================
brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01)
adjusted_color = adjust_brightness(st.session_state.current_color, brightness)

# 主颜色展示
st.markdown(f"""
<div style="display:flex; justify-content:center; align-items:center; gap:20px; 
            margin:25px 0; padding:15px; background:#f9f9f9; border-radius:10px;">
  <div style="width:80px; height:80px; border-radius:10px; 
              background:{adjusted_color}; box-shadow:0 4px 12px rgba(0,0,0,0.15)"></div>
  <div>
    <div style="font-size:24px; font-weight:bold;">{adjusted_color}</div>
    <div style="color:#666; margin-top:5px;">
      RGB: {hex_to_rgb(adjusted_color)} | 十进制: {hex_to_rgb(adjusted_color)[0]*65536 + hex_to_rgb(adjusted_color)[1]*256 + hex_to_rgb(adjusted_color)[2]}
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
        color = similar_colors[i]
        text_color = "#000" if (hex_to_rgb(color)[0]*0.299 + hex_to_rgb(color)[1]*0.587 + hex_to_rgb(color)[2]*0.114) > 150 else "#fff"
        st.markdown(f"""
        <div style="background:{color}; color:{text_color}; width:100%; aspect-ratio:1;
                    border-radius:10px; display:flex; justify-content:center; 
                    align-items:center; font-weight:bold; box-shadow:0 2px 6px rgba(0,0,0,0.1)">
          {color}
        </div>
        """, unsafe_allow_html=True)

# 使用说明
st.markdown("""
<div style="margin-top:30px; padding:15px; background:#f0f4f8; border-radius:8px;">
  <h3 style="color:#2C3E50;">使用说明</h3>
  <ul style="color:#555; line-height:1.6;">
    <li><strong>拖动色轮</strong> - 实时改变颜色</li>
    <li><strong>明度滑块</strong> - 调整颜色亮度</li>
    <li><strong>URL共享</strong> - 自动保存当前颜色到链接</li>
  </ul>
</div>
""", unsafe_allow_html=True)
