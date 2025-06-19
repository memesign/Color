import streamlit as st
import streamlit.components.v1 as components

st.title("测试 iro.js 色轮是否可交互")

html_code = """
<div id="picker" style="margin: auto;"></div>
<script src="https://cdn.jsdelivr.net/npm/@jaames/iro@5"></script>
<script>
  var colorPicker = new iro.ColorPicker("#picker", {
    width: 280,
    color: "#D88DC6",
    layout: [
      { component: iro.ui.Wheel },
      { component: iro.ui.Slider, options: { sliderType: 'value' } }
    ]
  });

  colorPicker.on('color:change', function(color) {
    console.log("颜色变化:", color.hexString);
    document.getElementById("current-color").textContent = color.hexString.toUpperCase();
  });
</script>
<p style="text-align:center; font-size:20px; margin-top: 15px;">
  当前颜色: <span id="current-color">#D88DC6</span>
</p>
"""

components.html(html_code, height=350)
