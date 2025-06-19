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
# 工具函数 (带缓存)
# ======================
@st.cache_data
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """HEX转RGB元组 (#RRGGBB -> (r,g,b))"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@st.cache_data
def hex_to_decimal(hex_color: str) -> int:
    """HEX转十进制值 (#RRGGBB -> 十进制)"""
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

@st.cache_data
def generate_similar_colors(hex_color: str, step: int = 20) -> List[str]:
    """生成相近颜色 (明暗变体)"""
    r, g, b = hex_to_rgb(hex_color)
    variants = []
    for i in [-step, 0, step]:
        r2 = min(255, max(0, r + i))
        g2 = min(255, max(0, g + i))
        b2 = min(255, max(0, b + i))
        variants.append(f"#{r2:02X}{g2:02X}{b2:02X}")
    return variants

@st.cache_data
def adjust_brightness(hex_color: str, brightness_factor: float) -> str:
    """调整颜色明度 (0.1-1.0)"""
    r, g, b = hex_to_rgb(hex_color)
    r_f, g_f, b_f = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)
    v = max(0, min(v * brightness_factor, 1))
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
    return f"#{int(r_new * 255):02X}{int(g_new * 255):02X}{int(b_new * 255):02X}"

def get_text_color_for_bg(hex_color: str) -> str:
    """根据背景色返回最佳文字颜色 (黑/白)"""
    r, g, b = hex_to_rgb(hex_color)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#000000" if brightness > 140 else "#FFFFFF"

# ======================
# 状态管理
# ======================
def get_valid_color_from_url() -> str:
    """从URL参数获取有效颜色值"""
    color = st.query_params.get("color", [None])[0]
    if color:
        color = color.upper()
        if re.match(r"^#[0-9A-F]{6}$", color):
            return color
    return None

# 初始化或从URL恢复颜色
if "selected_color" not in st.session_state:
    st.session_state.selected_color = "#D88DC6"  # 默认颜色

color_in_url = get_valid_color_from_url()
if color_in_url and color_in_url != st.session_state.selected_color:
    st.session_state.selected_color = color_in_url

current_color = st.session_state.selected_color

# ======================
# 页面布局
# ======================
st.markdown("""
<h1 style="text-align:center; color:#2C3E50;">🎨 色轮选色器</h1>
<p style="text-align:center; font-size:18px; color:#7F8C8D;">
拖动色轮选择颜色，点击色值可复制
</p>
""", unsafe_allow_html=True)

# ======================
# 色轮组件 (前端交互)
# ======================
components.html(f"""
<div style='width:100%; max-width:320px; margin:0 auto; padding:15px; 
             background:#f8f8f8; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1)'>
  <div id='picker'></div>
  <p style='text-align:center; font-size:16px; margin-top:15px; cursor:pointer;'>
    当前颜色: <span id='current-color' style='font-weight:bold;'>{current_color}</span>
  </p>
</div>

<script src='https://cdn.jsdelivr.net/npm/@jaames/iro@5'></script>
<script>
  // 初始化色轮
  var colorPicker = new iro.ColorPicker('#picker', {{
    width: Math.min(300, window.innerWidth - 40),
    color: '{current_color}',
    layout: [
      {{ component: iro.ui.Wheel }},
      {{ component: iro.ui.Slider, options: {{ sliderType: 'value' }} }}
    ]
  }});

  // 颜色变化时更新UI和URL
  colorPicker.on('color:change', function(color) {{
    const hex = color.hexString.toUpperCase();
    document.getElementById('current-color').textContent = hex;
    window.history.replaceState(null, null, `?color=${{hex}}`);
    
    // 更新页面上的颜色显示 (避免Streamlit重载)
    document.querySelectorAll('.color-display').forEach(el => {{
      if (el.style.background) el.style.background = hex;
    }});
  }});

  // 点击复制颜色
  document.getElementById('current-color').addEventListener('click', function() {{
    navigator.clipboard.writeText(this.textContent)
      .then(() => alert(`已复制: ${{this.textContent}}`))
      .catch(err => console.error('复制失败:', err));
  }});
</script>
""", height=420)

# ======================
# 颜色调整与展示
# ======================
brightness = st.slider("明度调整", 0.1, 1.0, 1.0, 0.01, key="brightness_slider")
adjusted_color = adjust_brightness(current_color, brightness)

# 主颜色展示
st.markdown(f"""
<div style='display:flex; justify-content:center; align-items:center; gap:20px; 
            margin:25px 0; padding:15px; background:#f9f9f9; border-radius:10px;'>
    <div class='color-display' 
         style='width:80px; height:80px; border-radius:10px; background:{adjusted_color};
                box-shadow:0 4px 12px rgba(0,0,0,0.15);'></div>
    <div>
        <div style='font-size:24px; font-weight:bold; color:#333;'>{adjusted_color}</div>
        <div style='color:#666; margin-top:5px;'>
            RGB: {hex_to_rgb(adjusted_color)} | 十进制: <code>{hex_to_decimal(adjusted_color)}</code>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 相近颜色展示
st.markdown("### 相近颜色")
similar_colors = generate_similar_colors(adjusted_color)
cols = st.columns(3)
for i, col in enumerate(cols):
    with col:
        c = similar_colors[i]
        text_color = get_text_color_for_bg(c)
        st.markdown(f"""
        <div style='background:{c}; color:{text_color}; width:100%; aspect-ratio:1;
                    border-radius:10px; display:flex; justify-content:center; 
                    align-items:center; font-weight:bold; font-size:18px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.15);'>
            {c}
        </div>
        """, unsafe_allow_html=True)

# ======================
# 使用说明
# ======================
st.markdown("""
<div style='margin-top:40px; padding:15px; background:#f0f4f8; border-radius:8px;'>
    <h3 style='color:#2C3E50;'>使用说明</h3>
    <ul style='color:#555; line-height:1.6;'>
        <li>拖动色轮选择颜色，色值会自动保存到URL</li>
        <li>点击色值代码可直接复制到剪贴板</li>
        <li>调整滑块改变颜色明度</li>
        <li>页面刷新后会保持当前选择的颜色</li>
    </ul>
</div>
""", unsafe_allow_html=True)
