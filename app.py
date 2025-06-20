import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ColorSelector", layout="wide")

components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"></script>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: #fff;
    }

    .title {
      font-size: 28px;
      font-weight: 600;
      color: #000;
      margin-top: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .title::before {
      content: "🎨";
      font-size: 24px;
    }

    #colorWheel {
      margin-top: 20px;
    }

    .slider-container {
      margin: 20px auto;
      text-align: center;
    }

    .slider-container span {
      font-size: 18px;
      color: #333;
    }

    .slider-container .value {
      color: #d58aff;
      margin-left: 5px;
    }

    input[type="range"] {
      width: 250px;
      accent-color: #d58aff;
    }

    .section {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: flex-start;
      gap: 30px;
      max-width: 960px;
      padding: 20px;
    }

    .main-color {
      width: 220px;
      height: 220px;
      border-radius: 20px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .info {
      font-size: 16px;
      color: #111;
      margin-top: 20px;
    }

    .info code {
      font-size: 16px;
      background: #f2f2f2;
      padding: 2px 6px;
      border-radius: 4px;
    }

    .hint {
      font-size: 14px;
      color: #666;
      margin-top: 6px;
    }

    .similar-section {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .similar-card {
      width: 180px;
      border-radius: 20px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
      overflow: hidden;
    }

    .color-block {
      height: 80px;
    }

    .color-info {
      padding: 10px;
      background: #fff;
      font-size: 14px;
      color: #222;
    }

    .color-info code {
      background: #f3f3f3;
      padding: 2px 4px;
      border-radius: 4px;
    }

    button {
      margin-top: 8px;
      padding: 4px 10px;
      font-size: 12px;
      border: 1px solid #aaa;
      border-radius: 6px;
      background: #f9f9f9;
      cursor: pointer;
    }

    @media (max-width: 768px) {
      .section {
        flex-direction: column;
        align-items: center;
      }
    }
  </style>
</head>
<body>
  <div class="title">ColorSelector</div>
  <div id="colorWheel"></div>

  <div class="slider-container">
    <span>明度调节</span>
    <span class="value" id="brightLabel">当前100%</span><br/>
    <input type="range" id="brightness" min="10" max="100" value="100"/>
  </div>

  <div class="section">
    <div>
      <div class="main-color" id="mainColor"></div>
      <div class="info">
        十进制: <code id="decValue"></code><br/>
        HEX: <code id="hexValue"></code><br/>
        RGB: <code id="rgbValue"></code><br/>
        <div class="hint">点击色块复制十进制色值</div>
      </div>
    </div>

    <div class="similar-section" id="similarColors"></div>
  </div>

  <script>
    const colorPicker = new iro.ColorPicker("#colorWheel", {
      width: 300,
      layout: [
        { component: iro.ui.Wheel }
      ]
    });

    const brightnessSlider = document.getElementById("brightness");
    const mainColorBox = document.getElementById("mainColor");
    const hexValue = document.getElementById("hexValue");
    const rgbValue = document.getElementById("rgbValue");
    const decValue = document.getElementById("decValue");
    const brightLabel = document.getElementById("brightLabel");
    const similarColors = document.getElementById("similarColors");

    function adjustBrightness(color, factor) {
      const hsv = color.hsv;
      hsv.v = Math.max(0, Math.min(100, hsv.v * factor));
      const newColor = iro.Color({ h: hsv.h, s: hsv.s, v: hsv.v });
      return newColor.hexString;
    }

    function updateUI() {
      const color = colorPicker.color;
      const factor = parseInt(brightnessSlider.value) / 100;
      const adjHex = adjustBrightness(color, factor);
      const rgb = color.rgb;
      const dec = parseInt(adjHex.slice(1), 16);

      mainColorBox.style.background = adjHex;
      hexValue.textContent = adjHex.toUpperCase();
      rgbValue.textContent = `(${rgb.r}, ${rgb.g}, ${rgb.b})`;
      decValue.textContent = dec;

      brightLabel.textContent = `当前${brightnessSlider.value}%`;

      // 相似色
      similarColors.innerHTML = '';
      [-40, -20, 20].forEach(delta => {
        let r = Math.min(255, Math.max(0, rgb.r + delta));
        let g = Math.min(255, Math.max(0, rgb.g + delta));
        let b = Math.min(255, Math.max(0, rgb.b + delta));
        let hex = '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1).toUpperCase();
        let card = document.createElement('div');
        card.className = 'similar-card';
        card.innerHTML = `
          <div class="color-block" style="background:${hex}"></div>
          <div class="color-info">
            HEX: <code>${hex}</code><br/>
            RGB: <code>(${r}, ${g}, ${b})</code><br/>
            <button onclick="colorPicker.color.hexString='${hex}'">Select Color</button>
          </div>
        `;
        similarColors.appendChild(card);
      });
    }

    colorPicker.on('color:change', updateUI);
    brightnessSlider.addEventListener('input', updateUI);

    mainColorBox.addEventListener('click', () => {
      navigator.clipboard.writeText(decValue.textContent).then(() => {
        alert('已复制十进制色值：' + decValue.textContent);
      });
    });

    updateUI();
  </script>
</body>
</html>
""", height=960)
