# 🎨 AI Drawing Recognition App (QuickDraw-Based Learning Tool)

## 📌 Overview

The **AI Drawing Recognition App** is an interactive web-based application designed for children to learn through creativity. Users can draw objects on a digital canvas, and the system uses a trained Machine Learning model to recognize and predict the drawing in real time.

This project is inspired by Google’s QuickDraw and utilizes the QuickDraw dataset to build an intelligent and engaging educational tool.

---

## 🎯 Objectives

* Develop an AI-powered application for real-time drawing recognition
* Enhance children's creativity and learning through interaction
* Demonstrate the practical use of Machine Learning in education
* Utilize large-scale datasets for training accurate models

---

## 🚀 Features

* ✏️ Interactive drawing canvas
* 🤖 Real-time AI prediction of drawings
* 🎯 High accuracy using trained ML model
* 📚 Educational feedback for kids
* ⚡ Fast and responsive interface (Glassmorphism UI)

---

## 🧠 Machine Learning Approach

* **Type:** Supervised Learning
* **Task:** Image Classification
* **Model Used:** Convolutional Neural Network (CNN)
* **Dataset:** Google QuickDraw Dataset (Subset: Apple, Car, Cat, House, Tree, Sun)

The model is trained on labeled doodles to recognize patterns and predict user drawings accurately.

---

## 🗂️ Dataset

We use the **QuickDraw Dataset**, which contains millions of labeled sketches collected globally.

* Includes categories like: cat, car, house, tree, etc.
* Data is preprocessed and converted into image format for training

---

## 🏗️ System Architecture

### 🔹 Frontend

* Web Application
* Technologies: HTML, CSS, JavaScript (Vanilla custom implementation)
* Features:
  * Responsive Drawing canvas with touch support
  * Premium design system
  * Display predictions and interactive feedback

---

### 🔹 Backend

* Technologies: Python, TensorFlow, Flask
* Responsibilities:
  * Process input drawings (Base64 decoding to 28x28 inversion arrays)
  * Run ML model for prediction
  * Return results to frontend

---

## ⚙️ How It Works

1. User draws an object on the canvas
2. Drawing is captured as input data (base64 image)
3. Data is sent to the backend model via REST API
4. Model predicts the object
5. Result is displayed instantly on the interface

---

## 📈 Advantages

* Encourages creativity in children
* Makes learning interactive and fun
* Demonstrates real-world AI application
* Scalable for more categories and features

---

## ⚠️ Limitations

* Accuracy depends on drawing quality
* May misclassify complex or unclear sketches
* Requires trained model for better performance

---

## 🔮 Future Improvements

* 🔊 Voice feedback (“This is a cat!”)
* 🎮 Gamification (levels, scoring system)
* 🌍 Multi-language support
* 🧑‍🏫 Drawing tutorials for kids
* 📱 Mobile app version

---

## 🛠️ Installation & Setup

### Prerequisites

* Python >= 3.10

### Steps

```bash
# Clone repository
git clone https://github.com/farhanmuhammadbashir-ship-it/SCD-Lab-Tasks-Farhan-2312407-BSCSD.git

# Navigate to project
cd SCD-Lab-Tasks-Farhan-2312407-BSCSD/ai-drawing-app

# Install backend dependencies
pip install -r requirements.txt

# Run backend server
python backend/app.py
```

---

## ▶️ Usage

* Open `frontend/index.html` in your browser (or use a local development server like Live Server).
* Draw any of the target objects (Apple, Car, Cat, House, Tree, Sun) on the canvas
* Click "Guess It!" to view the AI prediction instantly

---

## 📚 References

* https://quickdraw.withgoogle.com/
* https://github.com/googlecreativelab/quickdraw-dataset
* Russell & Norvig, Artificial Intelligence: A Modern Approach

---

## 👨‍💻 Author

**Farhan**
BS Computer Science – SZABIST University

---

## 📌 Conclusion

This project highlights how Machine Learning and AI can be used to create meaningful educational tools. By combining creativity with intelligent systems, the application provides a fun and impactful learning experience for children.
