import streamlit as st
import streamlit.components.v1 as components
import requests

# JavaScript를 이용해 위치 정보를 가져오는 HTML 코드
location_component = """
<!DOCTYPE html>
<html>
  <head>
    <title>Current Location</title>
    <script>
      function getLocation() {
          if (navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(showPosition, showError);
          } else {
              document.getElementById("location").innerHTML = "Geolocation is not supported by this browser.";
          }
      }

      function showPosition(position) {
          const latitude = position.coords.latitude;
          const longitude = position.coords.longitude;
          document.getElementById("location").innerHTML = "위도: " + latitude + "<br>경도: " + longitude;

          // Streamlit에 위치 정보를 전달
          window.parent.postMessage({latitude: latitude, longitude: longitude}, "*");
      }

      function showError(error) {
          switch(error.code) {
              case error.PERMISSION_DENIED:
                  alert("사용자가 위치 정보를 요청을 거부했습니다.");
                  break;
              case error.POSITION_UNAVAILABLE:
                  alert("위치 정보를 사용할 수 없습니다.");
                  break;
              case error.TIMEOUT:
                  alert("위치 정보 요청 시간이 초과되었습니다.");
                  break;
              case error.UNKNOWN_ERROR:
                  alert("알 수 없는 오류가 발생했습니다.");
                  break;
          }
      }
      getLocation();
    </script>
  </head>
  <body>
    <div id="location">위치 정보 받는 중...</div>
    <iframe src="https://www.google.com/maps/d/u/0/embed?mid=11rt0zmsvqgm93BrLoVIVzCAg3-XffoY&ehbc=2E312F&noprof=1" width="640" height="480"></iframe>
  </body>
</html>
"""

# HTML 코드 실행
components.html(location_component, height=700)  # iframe 높이에 맞게 설정

# 위치 정보를 Streamlit에서 받기 위한 메시지 처리
location_data = st.query_params  # Streamlit에서 쿼리 파라미터 가져오기
if "latitude" in location_data and "longitude" in location_data:
    lat = float(location_data["latitude"][0])
    lon = float(location_data["longitude"][0])
    st.write(f"위도: {lat}, 경도: {lon}")

data = {
    "목적지": ["김대중컨벤션센터역", "광주공항", "상무포차"],
    "걸리는 시간 (분)": ["5분(360M)", "56분(3.5km)", "33분(1.9km)"]
}

import pandas as pd

df = pd.DataFrame(data)
st.dataframe(df)

selected_destination = st.selectbox("목적지를 선택하세요:", df["목적지"].tolist())

selected_time = df.loc[df["목적지"] == selected_destination, "걸리는 시간 (분)"].values[0]
st.write(f"선택한 목적지: **{selected_destination}** - 걸리는 시간: **{selected_time}**분")
