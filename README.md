
# Image Homography Streamlit App

## Description
This application is a Streamlit-based web app for creating homographies from uploaded images. Users can select points on the images, and the app calculates and applies the homography transformation.
![image](https://github.com/andoni-a/Homography_Streamlit/assets/148989111/d54f1ff8-6385-482b-b0ce-3fd7b325d454)

## Project Structure

```
Project-Folder/
│
├── src/                   # Source code
│   ├── app.py             # Main application file
│   ├── homography.py      # Homography related functions
│   └── point_selector.py  # Point selection functions
│
├── .gitignore             # Git ignore file
├── README.md              # Project README
└── requirements.txt       # Required Python packages
```

## Installation

1. Clone the repository:
   ```
   git clone [GitHub Repo URL]
   ```

2. Navigate to the project directory:
   ```
   cd [Project Folder]
   ```

3. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run src/app.py
   ```

2. Open your web browser and go to the address shown in the terminal (usually `http://localhost:8501`).

3. Follow the instructions in the app to upload images and perform homography transformations.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request.

## License
This project is open source and available under the [MIT License](LICENSE).
