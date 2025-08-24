# PDF Workbook Processor

This repository contains a Python prototype that converts PDF-based workbooks into structured question/answer data. It can be used as a backend utility for an Android or web application.

## Usage

1. Install dependencies:
   ```bash
   pip install pypdf
   ```
2. Generate question/answer pairs from two PDF files:
   ```bash
   python pdf_workbook.py questions.pdf answers.pdf output_dir
   ```
   The resulting `pairs.json` file inside `output_dir` contains an array of question/answer objects.

## Android Sample App

The `android/` directory contains a minimal Android project written in Kotlin/Jetpack Compose. It demonstrates how to load the `pairs.json` file from the app's assets and present each question with a button to reveal the answer.

1. Generate `pairs.json` using the Python script above.
2. Copy the resulting file into `android/app/src/main/assets/`.
3. Open the `android/` folder in Android Studio and run the project on a device or emulator.

## Notes
- The splitting logic is heuristic and assumes that each problem in the PDF starts with a number such as `1.` or `2.` at the beginning of a line.
- For complex layouts or scanned images, additional OCR and layout analysis will be required.
