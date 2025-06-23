

# 🔍 Real-Time Number Plate Detection

This project performs **real-time number plate detection** using OpenCV and Haar Cascade classifiers. It supports detection from a **webcam**, **recorded video**, or **IP camera stream**, and saves **unique number plates** as cropped images.

---

## 📦 Features

- 🔁 Real-time number plate detection
- 📷 Supports webcam, video files, and IP camera streams
- 🧠 Avoids saving duplicate plates using hashing & time delay
- 🧾 Automatically saves cropped number plate images to disk
- 🏃‍♂️ Optimized with frame skipping for better performance

---

## 🖥️ Demo

https://youtu.be/ZbM4fapNxnA 

---

## 📁 Folder Structure

```

number-plate-detector/
│
├── model/
│   └── haarcascade\_russian\_plate\_number.xml  # Haar Cascade file
│
├── plates/          # Saved number plate images
│
├── videos/          # Optional input video files
│
├── main.py          # Main detection script
└── README.md

````

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.x
- OpenCV
- (Optional) pytesseract for OCR (not included in base script)


## 🧪 Run the Project

### ✅ Webcam Mode

```python
source = 0
```

### ✅ IP Camera Mode (e.g., Android IP Webcam)

```python
source = 'http://<your_ip>:8080/video'
```

### ✅ Local Video File

```python
source = 'videos/car_drive.mp4'
```

Then run:

```bash
python main.py
```

---

## 📸 Output

* Saved plates are stored in `/plates` with unique filenames.
* Only unique plates (based on image hash and time threshold) are saved.

---

## 🧠 How It Works

* Captures frames from the video source
* Converts to grayscale
* Detects plates using Haar cascade
* Extracts ROI (Region of Interest)
* Hashes the ROI and saves it only if it's not a duplicate
* Draws rectangles on live video feed

---

## 📈 Future Improvements

* Add OCR using `pytesseract`
* Integrate with database or CSV logging
* Use deep learning models (e.g., YOLOv5 or EasyOCR)
* Real-time number recognition & validation

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙋‍♂️ Author

**Nihal Jaiswal**
📧 [nihaljaisawal1@gmail.com](mailto:nihaljaisawal1@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/nihal-jaiswal/)
