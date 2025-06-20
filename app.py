import streamlit as st
import streamlit.components.v1 as components
import colorsys

st.set_page_config(page_title="色轮选色器", layout="wide")

st.title("🎨 色轮选色器（严格还原设计）")

# === 色轮交互用HTML+JS生成，canvas点击返回色相和饱和度 ===
def get_color_wheel_html():
    html = """
    <canvas id="colorwheel" width="250" height="250" style="cursor:pointer;border-radius:50%;"></canvas>
    <script>
    const canvas = document.getElementById('colorwheel');
    const ctx = canvas.getContext('2d');
    const radius = canvas.width / 2;
    const toHex = (c) => ('0' + c.toString(16)).slice(-2);

    function drawColorWheel() {
        for(let y=0; y<canvas.height; y++) {
            for(let x=0; x<canvas.width; x++) {
                let dx = x - radius;
                let dy = y - radius;
                let dist = Math.sqrt(dx*dx + dy*dy);
                if(dist <= radius) {
                    let angle = Math.atan2(dy, dx);
                    if(angle < 0) angle += 2*Math.PI;
                    let hue = angle / (2*Math.PI);
                    let sat = dist / radius;
                    let rgb = hslToRgb(hue, sat, 0.5);
                    ctx.fillStyle = 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
                    ctx.fillRect(x, y, 1, 1);
                }
            }
        }
    }
    // HSL转RGB，取L=0.5
    function hslToRgb(h, s, l) {
        let r, g, b;

        if(s === 0){
            r = g = b = l * 255; // achromatic
        } else {
            const hue2rgb = (p, q, t) => {
                if(t < 0) t += 1;
                if(t > 1) t -= 1;
                if(t < 1/6) return p + (q - p)*6*t;
                if(t < 1/2) return q;
                if(t < 2/3) return p + (q - p)*(2/3 - t)*6;
                return p;
            }
            let q = l < 0.5 ? l*(1 + s) : l + s - l*s;
            let p = 2*l - q;
            r = hue2rgb(p, q, h + 1/3)*255;
            g = hue2rgb(p, q, h)*255;
            b = hue2rgb(p, q, h - 1/3)*255;
        }
        return [Math.round(r), Math.round(g), Math.round(b)];
    }

    drawColorWheel();

    canvas.onclick = function(event){
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const dx = x - radius;
        const dy = y - radius;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if(dist <= radius){
            let angle = Math.atan2(dy, dx);
            if(angle < 0) angle += 2*Math.PI;
            let hue = angle / (2*Math.PI);
            let sat = dist / radius;
            // 向streamlit传递色相和饱和度
            const msg = JSON.stringify({hue: hue, sat: sat});
            window.parent.postMessage({isStreamlitMessage:true,type:"color_wheel_click",data:msg}, "*");
        }
    }
    </script>
    """
    return html

# ======= 主状态 =======
if "hue" not in st.session_state:
    st.session_state.hue = 0.0
if "sat" not in st.session_state:
    st.session_state.sat = 0.0
if "lum" not in st.session_state:
    st.session_state.lum = 0.5

# 监听JS消息
msg = st.experimental_get_query_params().get("msg", [None])[0]
if msg and "color_wheel_click" in msg:
    import json
    try:
        data = json.loads(msg.split(":",1)[1])
        st.session_state.hue = float(data["hue"])
        st.session_state.sat = float(data["sat"])
    except Exception:
        pass

# === 色轮嵌入 ===
components.html(get_color_wheel_html(), height=270)

# 明度调整滑条
lum = st.slider("明度调整", 0.0, 1.0, st.session_state.lum, 0.01)
st.session_state.lum = lum

# 颜色计算函数
def hsl_to_rgb(h, s, l):
    return tuple(round(i * 255) for i in colorsys.hls_to_rgb(h, l, s))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def rgb_to_dec(rgb):
    return rgb[0]*65536 + rgb[1]*256 + rgb[2]

# 主色
main_rgb = hsl_to_rgb(st.session_state.hue, st.session_state.sat, st.session_state.lum)
main_hex = rgb_to_hex(main_rgb)
main_dec = rgb_to_dec(main_rgb)

# 计算近似色（色相±10°、±20°）
def calc_near_colors(h, s, l):
    offsets = [-20/360, -10/360, 10/360]
    colors = []
    for off in offsets:
        nh = (h + off) % 1.0
        nrgb = hsl_to_rgb(nh, s, l)
        nhex = rgb_to_hex(nrgb)
        ndec = rgb_to_dec(nrgb)
        colors.append({"rgb": nrgb, "hex": nhex, "dec": ndec})
    return colors

near_colors = calc_near_colors(st.session_state.hue, st.session_state.sat, st.session_state.lum)

# === UI显示 ===

st.markdown("### 选择颜色结果")

col_main, col_info = st.columns([1, 2])

with col_main:
    st.markdown("#### 主色")
    st.markdown(f'<div style="width:100px; height:100px; background:{main_hex}; border-radius:10px; border: 1px solid #000;"></div>', unsafe_allow_html=True)

with col_info:
    st.markdown(f"HEX值: `{main_hex}`")
    st.markdown(f"10进制值: `{main_dec}`")

st.markdown("### 近似色")

cols = st.columns(3)
for i, c in enumerate(near_colors):
    with cols[i]:
        st.markdown(f'<div style="width:80px; height:80px; background:{c["hex"]}; border-radius:10px; border: 1px solid #000; margin-bottom:6px;"></div>', unsafe_allow_html=True)
        # 文字颜色自动判断浅色深色，这里简单黑色文字，且文字大小和位置适中不遮挡色块本身
        st.markdown(f'HEX: `{c["hex"]}`')
        st.markdown(f'Dec: `{c["dec"]}`')

