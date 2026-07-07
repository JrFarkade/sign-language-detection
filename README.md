# 🖐️ Real-Time Sign Language to Text & Speech Converter

A real-time American Sign Language (ASL) finger-spelling translator that captures gestures via a webcam, converts them into English letters, builds full sentences with spell-checking suggestions, and reads them aloud using text-to-speech.

---

## 👨‍💻 About This Project

This project was developed as a **Minor Project** for my B.Tech curriculum. 

### Why I Built This
During my coursework in Artificial Intelligence and Computer Vision, I wanted to build something that wasn't just a toy model or a clean Kaggle dataset project. I wanted to tackle a real-world problem: the communication barrier between hearing/speech-impaired individuals and the rest of the world. 

Most people don't know sign language, which isolates deaf and mute individuals in everyday situations. Building a software-only translator that runs on any cheap laptop with a basic webcam felt like a meaningful challenge that combined deep learning, computer vision, and graphical interfaces into a functional helper tool.

---

## ⚠️ Problem Statement

People who are deaf or mute rely on sign language as their primary means of expression. However, since the general public lacks sign language training, simple tasks—like ordering food, checking in at a counter, or asking for directions—can be highly frustrating.

While there are translation solutions, they often have major drawbacks:
1. **Hardware dependence**: Many require electronic glove sensors, which are expensive, fragile, and hard to carry around.
2. **Environmental noise**: Traditional image classification struggles with background clutter, varying skin tones, and changing lighting.

This project aims to solve these issues by building a low-cost, software-only application that processes webcam feeds, abstracts hand shapes into clean skeletons, and translates gestures reliably under any environment.

---

## 🔍 Project Overview

The converter works using a multi-stage pipeline:

1. **Video Frame Capture**: The webcam captures live BGR frames, which are flipped horizontally to mirror user actions.
2. **Hand Detection**: A primary hand tracking module locates the hand boundaries and crops the hand region.
3. **Skeleton Projection**: A secondary hand tracking module plots the 21 joint landmark coordinates from the cropped hand. These coordinates are projected onto a blank 400x400 white canvas as a standardized green-and-red line drawing.
4. **CNN Group Classification**: The vector skeleton canvas is fed into a Convolutional Neural Network (CNN) that predicts one of **8 general shape groups**.
5. **Programmatic Disambiguation**: Once a group is predicted, custom Python rules (such as checking finger extensions or x/y coordinate distances) resolve the exact letter (A to Z) or trigger controls like Space and Backspace.
6. **Sentence Builder & Suggestions**: Words are compiled in a text buffer. The spell-checking engine scans the current word and displays correction options.
7. **Audio Synthesis**: The user can click a button to read the translated sentence aloud.

---

## ✨ Features

* **Real-time Camera Feed**: Real-time webcam frame acquisition and hand boundary cropping.
* **Lighting-Independent Vectors**: Converts hands into green-and-red connection skeletons, eliminating skin tone, shadow, and background noise.
* **Hybrid Classification**: Solves confusing letter shapes (like closed fists in `A`, `S`, `M`, and `N`) by predicting broad CNN groups first and checking joint metrics in Python second.
* **Sentence Assembly**: Integrates Space and Backspace gestures to edit sentences directly on-screen.
* **Live Word Autocorrect**: Suggests words dynamically. Clicking a suggestion replaces misspelled text with the correct spelling.
* **Voice Output**: Reads the finished sentences aloud using offline system voices.

---

## 🛠️ Technologies Used

* **Python 3.x**: Primary language for UI layout, control logic, and mathematical slicing.
* **OpenCV (`opencv-python`)**: Captures video frames, flips inputs, and crops hand regions.
* **cvzone / MediaPipe**: Locates the 21 joint coordinates and tracks bounding box ranges.
* **Keras & TensorFlow**: Runs model predictions on the vector skeletons.
* **Tkinter**: Builds the graphical dashboard, buttons, and text output panels.
* **PyEnchant**: Provides live spellcheck suggestion lookup dictionaries (`en-US`).
* **pyttsx3**: Converts written text to offline synthesized speech.
* **NumPy**: Standardizes canvas matrices, rescales inputs, and handles image array shapes.

---

## 📊 Dataset Preparation

The dataset consists of standardized **skeleton images** captured from real-world hand signs.

### Collection Process
Using `data_collection_final.py`:
1. The camera feed detects the hand region and extracts its bounding box.
2. The joint coordinates are drawn on a white background image canvas (`white.jpg`).
3. Pressing `'n'` switches the output folder from `A` to `Z`.
4. Pressing `'a'` records skeleton images to disk every 3 frames, creating a total of 180 samples per letter class.

### Directory Organization
The images are saved locally inside `AtoZ_3.1/` under their respective folders:
```
AtoZ_3.1/
├── A/
│   ├── 0.jpg
│   └── ... [Up to 179.jpg]
├── B/
└── [C to Z Folders]
```

---

## 🧠 Model Training

The CNN classifier model (`model/cnn8grps_rad1_model.h5`) maps preprocessed vector skeletons into groups.

### Training Strategy
Instead of training a neural network to predict 26 letters directly—which often fails because closed-fist gestures like `A`, `S`, `M`, and `N` are structurally similar—we trained the model to identify **8 general shape categories**:
* **Group 0**: `A, E, M, N, S, T`
* **Group 1**: `B, D, F, I, K, R, U, V, W` (and Space/Backspace controls)
* **Group 2**: `C, O`
* **Group 3**: `G, H`
* **Group 4**: `L`
* **Group 5**: `P, Q, Z`
* **Group 6**: `X`
* **Group 7**: `Y, J`

### Python Coordinate Rules (Disambiguation)
Once the CNN outputs the group classification, the code runs specific landmark evaluations in Python:
* **Group 0 Differentiator**: Evaluates the position of the thumb joint (`pts[4][0]`) relative to the index finger to separate `A`, `S`, `T`, `E`, `M`, and `N`.
* **Group 1 Differentiator**: Checks finger extensions (comparing tip height vs. joint height) to separate letters like `B`, `D`, `F`, and `I`.
* **Group 2 Differentiator**: Evaluates the distance between the index tip (`pts[8]`) and the thumb tip (`pts[4]`) to classify `C` or `O`.

---

## 📁 Project Structure

Here is the folder structure of the repository:

```
sign-anguage-detection/
├── model/                        # Holds the trained Keras model
│   └── cnn8grps_rad1_model.h5    # CNN classifier (8 groups)
├── assets/                       # UI screenshots and graphs
├── AtoZ_3.1/                     # Skeleton image dataset (folders A-Z)
│
├── app.py                        # Desktop dashboard application (GUI)
├── prediction_wo_gui.py          # Terminal-based sign language predictor
├── data_collection_final.py      # Skeleton image dataset creator
├── data_collection_binary.py     # Binary & Grayscale dataset creator
├── white.jpg                     # Base white canvas image template
│
├── requirements.txt              # Project package list
└── .gitignore                    # Local files to ignore
```

---

## 🚀 Installation

### 1. Prerequisites
Make sure you have Python 3.8 to 3.11 installed. You also need a webcam.

### 2. Clone the Repository
```bash
git clone https://github.com/jrfarkade/sign-language-detection.git
cd sign-language-detection
```

### 3. Install Required Libraries
```bash
pip install -r requirements.txt
```
*Note: If you are running on Linux and get a PyEnchant dictionary error, install the system dictionary packages:*
```bash
sudo apt-get install myspell-en-us hunspell-en-us
```

---

## 💻 Usage

### Run the Real-Time GUI Application
To launch the interactive translator GUI:
```bash
python app.py
```
* Hold your hand within the webcam bounding box. The right screen will draw your hand's skeleton, and the predicted letter will print.
* Click the suggestions under **Suggestions** to correct word spelling.
* Click **Speak** to read the sentence aloud. Click **Clear** to reset the window.

### Run the Console Predictor (No GUI)
To test predictions in the terminal using standard OpenCV windows:
```bash
python prediction_wo_gui.py
```
*(Press `Esc` to quit).*

### Gather Training Data
To record new skeleton datasets:
```bash
python data_collection_final.py
```
* Press `'n'` to switch the target letter folder.
* Press `'a'` to toggle recording.

---

## 📈 Results

* **Processing Frame Rate**: Achieves 30+ FPS on mid-range laptops because processing vector lines requires much less CPU power than full RGB image classification.
* **High Accuracy**: The combination of CNN group prediction and geometric landmark checking successfully eliminates letter-swapping errors.
* **Auto-Correction**: Live spellcheck recommendations successfully correct typed words, making communication smooth.

---

## 🛠️ Challenges Faced

* **cvzone Return Differences**: The return signature of `findHands()` varies between list and tuple structures across different system versions. I resolved this by adding a type check:
  ```python
  hands = hands_res[0] if isinstance(hands_res, tuple) else hands_res
  ```
* **Edge Slicing Crashes**: Cropping coordinates when hands went close to the edge of the frame caused empty arrays. Added boundary clamping bounds (`max(0, ...)` and `min(..., ...)`) to resolve this.
* **Console Page Encoding Errors**: TensorFlow predictions printed unicode progress bars, raising encoding crashes on Windows cmd. Suppressed predictions logging with `verbose=0`.

---

## 🔮 Future Improvements

* **Two-Hand Sign Support**: Expand tracking to monitor both hands for complex gesture symbols.
* **Fluid Sentence Translation**: Integrate recurrent layers (LSTMs) or attention modules to translate continuous fluid signing rather than finger-spelling.
* **Mobile Web Deployment**: Port model binaries using TensorFlow Lite to host the translator on web platforms or mobile apps.

---

## 🎓 Learning Outcomes

Through building this project, I:
* Learned how to preprocess video streams and implement hand boundary clamping.
* Understood how to normalize input structures (such as mapping hands to vector skeletons) to eliminate real-world background noise.
* Discovered the benefits of hybrid classification (CNN + geometric coordinate rules) over direct multi-class deep learning.
* Gained experience with Tkinter GUI architectures, pyttsx3 offline text-to-speech, and PyEnchant spell-check integrations.

---

## 🖼️ Media & Screenshots

*Placeholder sections to insert screenshots once added to the repository:*

#### Primary Tkinter Dashboard UI
> *Add a screenshot showing the live video feed, skeleton panel, text output, and suggestions buttons.*
> `![GUI Screenshot](assets/app_screenshot.png)`

#### Preprocessing Comparison (Raw vs Skeleton)
> *Add a visualization of the raw hand crop alongside the mapped skeleton canvas.*
> `![Preprocessing Step](assets/preprocess_screenshot.png)`

---

## ✍️ Author

* **Jr Farkade**
* B.Tech AI Engineering
* [GitHub Profile](https://github.com/jrfarkade)
* [LinkedIn Profile](https://linkedin.com/in/jrfarkade)
