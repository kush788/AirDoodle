# ✋ Air Doodle

Introducing **Air Doodle** – where your imagination takes flight with just the flick of a finger! Draw anything your heart desires using nothing but the motion of your hands. No brush, no stylus — just pure air.

By tracking the landmarks on your hand using computer vision and machine learning, Air Doodle transforms your gestures into art on a virtual canvas — right in your browser.

🌐 **Live Demo:** [airdoodle.streamlit.app](https://airdoodle-aavgjkvkesntdgmipqxkgf.streamlit.app/) <!-- Replace with your actual URL -->

---

## 🎨 Features

- ✏️ Draw in the air using your **index finger**
- 🤌 **Pinch** (thumb + index finger) to lift the brush
- 🎨 Choose from **4 colors** — Blue, Green, Red, Yellow
- 🗑️ **Clear** the canvas with a gesture or button
- 🌐 Runs entirely in the **browser** — no installation needed

---

## ⚙️ How It Works

1. **Hand Detection** — OpenCV detects your hand from the webcam feed in real-time
2. **Landmark Detection** — MediaPipe tracks 21 hand landmarks (knuckles, fingertips, etc.) with high precision
3. **Motion Tracking** — Your index fingertip position is mapped to strokes on the virtual canvas
4. **Gesture Recognition** — Pinching lifts the brush; moving to the top bar switches colors or clears the canvas

---

## 🚀 Try It Online

Just open the link below in **Chrome or Firefox** on any device with a webcam:

👉 **[Open Air Doodle](https://airdoodle-aavgjkvkesntdgmipqxkgf.streamlit.app/)** <!-- Replace with your actual URL -->

> 📷 A webcam (built-in or USB) is required. Works on laptops, phones, and tablets.

---

## 🛠️ Run Locally

If you want to run it on your own machine:

### Prerequisites
- Python 3.10+
- A webcam

### Clone the repository
```bash
git clone https://github.com/kush788/Air_Doodle.git
cd Air_Doodle
```

### Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the app
```bash
streamlit run AirDoodle.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📦 Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) | Webcam streaming in browser |
| [MediaPipe](https://mediapipe.dev) | Hand landmark detection |
| [OpenCV](https://opencv.org) | Image processing |
| [NumPy](https://numpy.org) | Array operations |

---

## 📁 Project Structure

```
Air_Doodle/
├── AirDoodle.py        # Main Streamlit app
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies (for Streamlit Cloud)
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
