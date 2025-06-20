import streamlit as st
import streamlit.components.v1 as components
import colorsys

st.set_page_config(page_title="ColorSelector", layout="wide")

# 工具函数
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))

def hex_to_decimal(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return r * 256**2 + g * 256 + b

def generate_similar_colors(hex_color):
    r,g,b = hex_to_rgb(hex_color)
    variants = []
    for delta in [-40, -20, 20]:
        rr = min(255, max(0, r + delta))
        gg = min(255, max(0, g + delta))
        bb = min(255, max(0, b + delta))
        variants.append(f'#{rr:02X}{gg:02X}{bb:02X}')
    return variants

def adjust_brightness(hex_color, factor):
    r,g,b = hex_to_rgb(hex_color)
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    v = max(0, min(v*factor,1))
    rn,gn,bn = colorsys.hsv_to_rgb(h,s,v)
    return f'#{int(rn*255):02X}{int(gn*255):02X}{int(bn*255):02X}'

# HTML + JS 交互式色轮 & 响应式布局
components.html(f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"></script>
  <style>
    body {{margin:0;padding:0;}}
    .container {{display:flex; flex-direction:column; align-items:center;}}
    .controls{{width:90%; max-width:600px; margin-top:20px; text-align:center;}}
    .main{{display:flex; flex-wrap:wrap; justify-content:center; margin-top:30px; gap:20px; width:90%; max-width:900px;}}
    .color-box{{border-radius:16px; box-shadow:0 2px 8px rgba(0,0,0,0.15);}}
    .large-box{{width:200px; height:200px;}}
    .small-box{{width:160px;}}
    @media (max-width:600px) {{
      .main {{flex-direction:column; align-items:center;}}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>🎨 ColorSelector</h1>
    <div id="picker"></div>
    <div class="controls">
      明度调节 <span id="bright_text">当前100%</span><br>
      <input type="range" id="bright" min="10" max="100" value="100"/>
    </div>
    <div class="main">
      <div id="main_color" class="color-box large-box"></div>
      <div id="main_info"></div>
      <div id="similar_colors"></div>
    </div>
  </div>

  <script>
    const picker = new iro.ColorPicker("#picker", {{
      width: 300,
      layout: [{{
        component: iro.ui.Wheel,
        options: {{}}
      }}]
    }});
    const bright = document.getElementById("bright");
    const bright_text = document.getElementById("bright_text");
    const main_color = document.getElementById("main_color");
    const main_info = document.getElementById("main_info");
    const similar_colors = document.getElementById("similar_colors");

    function updateUI() {{
      const hex = picker.color.hexString;
      const factor = bright.value / 100;
      const [r,g,b] = picker.color.rgb;
      const color = iro.Color({{r,g,b}}).setValue("hsv").rgbaString; // adjust brightness
      const adjusted = iro.Color(color).toString('hex8').slice(0,7);
      main_color.style.background = adjusted;
      bright_text.textContent = "当前" + bright.value + "%";
      const dec = (parseInt(adjusted.slice(1),16));
      main_info.innerHTML = `<div>十进制：<code>${{dec}}</code></div>
                              <div>HEX：<code>${{adjusted.toUpperCase()}}</code></div>
                              <div>RGB：<code>(${{r}},${{g}},${{b}})</code></div>`;
      // 生成相近色
      similar_colors.innerHTML = '';
      [-40,-20,20].forEach(delta => {{
        const rc = Math.max(0,Math.min(255,r+delta));
        const gc = Math.max(0,Math.min(255,g+delta));
        const bc = Math.max(0,Math.min(255,b+delta));
        const hex2 = '#' + ((1<<24)+(rc<<16)+(gc<<8)+bc).toString(16).slice(1).toUpperCase();
        const div = document.createElement("div");
        div.className = "color-box small-box";
        div.style.background = hex2;
        div.innerHTML = `<div style="padding:8px; color:#000;">
                          HEX: <code>${{hex2}}</code><br>
                          RGB: <code>(${{rc}},${{gc}},${{bc}})</code><br>
                          <button onclick="picker.color.hexString='${{hex2}}'">Select Color</button>
                         </div>`;
        similar_colors.appendChild(div);
      }});
    }}

    picker.on('color:change', updateUI);
    bright.addEventListener('input', () => {{
      picker.color.hsv = picker.color.hsv; 
      updateUI();
    }});
    updateUI();
  </script>
</body>
</html>
""", height=800)
