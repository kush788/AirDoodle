import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av

# Page config
st.set_page_config(page_title="✋ Air Paint", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0f0f0f; }
        .main { background-color: #0f0f0f; }
        h1 { color: #ffffff; font-family: 'Courier New', monospace; }
        .stMarkdown p { color: #aaaaaa; }
        .instructions {
            background: #1a1a1a;
            border-left: 3px solid #00ff88;
            padding: 10px 16px;
            border-radius: 4px;
            color: #cccccc;
            font-family: monospace;
            font-size: 0.85rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("✋ Air Paint")
st.markdown("Paint in the air using your **index finger**. Pinch thumb + index to lift the brush.")

# JavaScript: detect webcam availability and show friendly message
st.markdown("""
<div id="cam-warning" style="display:none; background:#2a1a1a; border-left:4px solid #ff4444;
     padding:14px 18px; border-radius:6px; color:#ffaaaa; font-family:monospace;
     margin-bottom:16px;">
    ⚠️ <b>No camera detected on your device.</b><br>
    <span style="color:#cc8888; font-size:0.85rem;">
        This app requires a webcam to track your hand movements.<br>
        Try opening it on a device with a built-in or USB camera (laptop, phone, tablet).
    </span>
</div>

<script>
(async () => {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const hasCamera = devices.some(d => d.kind === 'videoinput');
        if (!hasCamera) {
            document.getElementById('cam-warning').style.display = 'block';
        }
    } catch (e) {
        // If permissions blocked, we can't enumerate — show warning too
        document.getElementById('cam-warning').style.display = 'block';
    }
})();
</script>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 🎨 Select Color")
    color_choice = st.radio(
        "", ["🔵 Blue", "🟢 Green", "🔴 Red", "🟡 Yellow"], index=0
    )
    st.markdown("---")
    st.markdown('<div class="instructions">'
                '<b>How to use:</b><br>'
                '👆 Raise index finger → Draw<br>'
                '🤌 Pinch (thumb + index) → Lift brush<br>'
                '🖐 Move to top bar → Select color / Clear'
                '</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="instructions">'
                '📋 <b>Requirements:</b><br>'
                '📷 Webcam (built-in or USB)<br>'
                '🌐 Chrome or Firefox browser<br>'
                '💡 Good lighting on your hand'
                '</div>', unsafe_allow_html=True)

color_map = {
    "🔵 Blue":   (255, 0, 0),
    "🟢 Green":  (0, 255, 0),
    "🔴 Red":    (0, 0, 255),
    "🟡 Yellow": (0, 255, 255),
}
color_index_map = {
    "🔵 Blue": 0,
    "🟢 Green": 1,
    "🔴 Red": 2,
    "🟡 Yellow": 3,
}

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class AirPaintProcessor(VideoProcessorBase):
    def __init__(self):
        self.bpoints = [deque(maxlen=1024)]
        self.gpoints = [deque(maxlen=1024)]
        self.rpoints = [deque(maxlen=1024)]
        self.ypoints = [deque(maxlen=1024)]

        self.blue_index = 0
        self.green_index = 0
        self.red_index = 0
        self.yellow_index = 0

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0

        self.kernel = np.ones((5, 5), np.uint8)

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
        )
        self.mpdraw = mp.solutions.drawing_utils

    def set_color(self, idx):
        self.colorIndex = idx

    def clear(self):
        self.bpoints = [deque(maxlen=512)]
        self.gpoints = [deque(maxlen=512)]
        self.rpoints = [deque(maxlen=512)]
        self.ypoints = [deque(maxlen=512)]
        self.blue_index = 0
        self.green_index = 0
        self.red_index = 0
        self.yellow_index = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        h, w, _ = img.shape

        # Draw UI buttons on frame
        img = cv2.rectangle(img, (40, 1), (140, 65), (200, 200, 200), 2)
        img = cv2.rectangle(img, (160, 1), (255, 65), (255, 0, 0), 2)
        img = cv2.rectangle(img, (275, 1), (370, 65), (0, 255, 0), 2)
        img = cv2.rectangle(img, (390, 1), (485, 65), (0, 0, 255), 2)
        img = cv2.rectangle(img, (505, 1), (600, 65), (0, 255, 255), 2)

        cv2.putText(img, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2, cv2.LINE_AA)
        cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "YELLOW", (516, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        framergb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(framergb)

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * w)
                    lmy = int(lm.y * h)
                    landmarks.append([lmx, lmy])

            self.mpdraw.draw_landmarks(img, handslms, self.mpHands.HAND_CONNECTIONS)

            fore_finger = (landmarks[8][0], landmarks[8][1])
            center = fore_finger
            thumb = (landmarks[4][0], landmarks[4][1])
            cv2.circle(img, center, 6, (0, 255, 0), -1)

            if thumb[1] - center[1] < 30:
                # Pinch = lift brush
                self.bpoints.append(deque(maxlen=512))
                self.blue_index += 1
                self.gpoints.append(deque(maxlen=512))
                self.green_index += 1
                self.rpoints.append(deque(maxlen=512))
                self.red_index += 1
                self.ypoints.append(deque(maxlen=512))
                self.yellow_index += 1

            elif center[1] <= 65:
                if 40 <= center[0] <= 140:
                    self.clear()
                elif 160 <= center[0] <= 255:
                    self.colorIndex = 0
                elif 275 <= center[0] <= 370:
                    self.colorIndex = 1
                elif 390 <= center[0] <= 485:
                    self.colorIndex = 2
                elif 505 <= center[0] <= 600:
                    self.colorIndex = 3
            else:
                if self.colorIndex == 0:
                    self.bpoints[self.blue_index].appendleft(center)
                elif self.colorIndex == 1:
                    self.gpoints[self.green_index].appendleft(center)
                elif self.colorIndex == 2:
                    self.rpoints[self.red_index].appendleft(center)
                elif self.colorIndex == 3:
                    self.ypoints[self.yellow_index].appendleft(center)
        else:
            self.bpoints.append(deque(maxlen=512))
            self.blue_index += 1
            self.gpoints.append(deque(maxlen=512))
            self.green_index += 1
            self.rpoints.append(deque(maxlen=512))
            self.red_index += 1
            self.ypoints.append(deque(maxlen=512))
            self.yellow_index += 1

        # Draw strokes
        points = [self.bpoints, self.gpoints, self.rpoints, self.ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(img, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


with col1:
    ctx = webrtc_streamer(
        key="air-paint",
        video_processor_factory=AirPaintProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if ctx.video_processor:
        ctx.video_processor.set_color(color_index_map[color_choice])

    if st.button("🗑️ Clear Canvas"):
        if ctx.video_processor:
            ctx.video_processor.clear()
