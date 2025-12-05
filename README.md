 # LensCorrect Repository

Welcome to the LensCorrect repository, a Python-based application that corrects lens distortions in photographs of a checkerboard pattern. This tool utilizes OpenCV for image processing and BeautifulSoup for XML parsing.

## Getting Started

To get started with LensCorrect, follow these steps:

1. Install the required packages by running `pip install -r Pipfile`. Ensure you have Python 3.9 installed on your system.

2. Place a checkerboard image in the current directory and run the following command to capture the calibration data (intrinsic parameters and distortion coefficients):

```sh
python getcalibration.py [image_name]
```
Replace `[image_name]` with the name of your checkerboard image file. The calibration data will be saved as "intrinsics.xml".

3. Run the main correction script to process images in the current directory and remove lens distortions:

```sh
python correct.py
```
This script reads the calibration data from "intrinsics.xml" and applies the corrections to all images (except those with "-improved" in their names) that follow the naming convention `[image_name].png`. Corrected images will be saved as `[image_name]-improved.png`.

## How It Works

The LensCorrect application first captures calibration data from a checkerboard image using OpenCV's chessboard corner detection and camera calibration algorithms. This data includes the intrinsic parameters (camera matrix) and distortion coefficients for the lens used to capture the images.

Next, the correction script reads the captured calibration data and iterates through all images in the current directory. For each image, it applies the inverse distortion and rectification operations using the OpenCV functions cv2.remap() and cv2.initUndistortRectifyMap(), respectively. The corrected images are then saved with a "-improved" suffix.

## Dependencies

- [numpy](https://numpy.org/) - Numerical Python library
- [opencv-python](https://pypi.org/project/opencv-python/) - OpenCV bindings for Python
- [bs4](https://pypi.org/project/beautifulsoup4/) - Beautiful Soup for parsing XML data
- [lxml](https://pypi.org/project/lxml/) - A fast, extensible library for working with XML and HTML documents in Python

## Contributing

We welcome contributions to improve LensCorrect! If you find a bug or have suggestions for new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use and modify it as needed, but be sure to respect the license terms.

## Acknowledgements

We would like to acknowledge the following resources that were used in developing LensCorrect:

- [OpenCV's chessboard corner detection and camera calibration tutorial](https://docs.opencv.org/4.5.3/dd/d89/tutorial_py_calib3d.html)
- [Python Golden Chessboard](https://github.com/kjellmk/GoldenChessboard) - A simple OpenCV script for calibrating a camera with a checkerboard pattern

Happy lens correction! 📸 🔍