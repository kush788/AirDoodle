# Air Doodle

Introducing the Air Doodle project – where your imagination takes flight with just the flick of a finger! Ever dreamed of creating art without lifting a brush? Well, get ready to turn that dream into reality as we dive into the exciting world of computer vision and machine learning.

With the Air Doodle, you have the power to draw anything your heart desires using nothing but the motion of your hands. By tracking the landmarks on your hand, including the fingertips, we can transform your gestures into pure creativity.


# Working


#### 1. Hand Detection: Using OpenCV's computer vision techniques, our project will detect your hand from the background .


#### 2. Landmark Detection: With the help of Mediapipe, or project will track the landmarks on your hand with remarkable precision. From knuckles to fingertips, every movement will be captured in real-time.


#### 3.Motion Tracking: As you wave your hand through the air, our system will track its every move, translating your gestures into strokes on our virtual canvas.

## Packages Required

- opencv-python
- mediapipe
- numpy
- python Interpretor 3.8

### Clone the project using
```
git clone https://github.com/kush788/Air_Doodle.git
cd Air_Doodle
```

### create virtual environment and activate
```
source <venv>/bin/activate   # On Linux/Mac
<venv>\Scripts\activate      # On Windows
cd ../..
```
- Replace <venv with the path to your virtual environment directory.


Install packages using
```
pip install -r requirements.txt
```

Run the project using:
```angular2html
python "Air Doodle.py"
```

