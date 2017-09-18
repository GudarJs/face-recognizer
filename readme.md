# Face Recognizer - By GudarJs
Face Recognizer application to log the entries on residencial building.

## Install dependencies
In order to run this project you will need to install some dependencies.

### Opencv 3
1. Install Opencv dependencies
``` bash
sudo apt-get install build-essential libgtk2.0-dev libjpeg-dev  libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtbb-dev libeigen2-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev
```
2. Clone Opencv contrib modules repository to your computer.
``` bash
git clone https://github.com/opencv/opencv_contrib.git
```
3. Change to Opencv contrib modules directory.
``` bash
cd opencv_contrib
```
4. Change to the tag 3.0.0
``` bash
git checkout 3.0.0
```
5. Change to your home directory.
``` bash
cd  $HOME
```
6. Clone Opencv repository to your computer.
``` bash
git clone https://github.com/opencv/opencv.git
```
7. Change to Opencv directory.
``` bash
cd opencv
```
8. Change to the tag 3.0.0
``` bash
git checkout 3.0.0
```
9. create build directory and change to it.
``` bash
mkdir build && cd build
```
10. Use cmake to generate makefile.
``` bash
cmake -D CMAKE_BUILD_TYPE=RELEASE -D   CMAKE_INSTALL_PREFIX=/usr/local -D   INSTALL_C_EXAMPLES=ON -D   INSTALL_PYTHON_EXAMPLES=ON -D   OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D   BUILD_EXAMPLES=ON ..
```
**Look that opencv_contrib folder is specified in the above command with the option *OPENCV_EXTRA_MODULES_PATH*, so please feel free to change it.**  
11. Compile opencv with contrib modules.
``` bash
make -j4
```
**Note that -j4 is the number of my cpu's cores, so if yours are diferent please change it.**  
12. Install opencv.
``` bash
sudo make install
```

### Sqlite3 Database
Run the following command.
``` bash
sudo apt install sqlite
```

### Python modules
Run the following command.
``` bash
pip install -r requirements.txt
```

## Register a new person to recognize
Run the following command.
``` bash
bash register_person.sh
```
It will ask you for a name and it must be lowercase and separated by dashes. **ie. dario-guzman.**  

## Credits
The [AT&T Facedatabase](http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html), sometimes also referred to as ORL Database of Faces, contains ten different images of each of 40 distinct subjects. For some subjects, the images were taken at different times, varying the lighting, facial expressions (open / closed eyes, smiling / not smiling) and facial details (glasses / no glasses). All the images were taken against a dark homogeneous background with the subjects in an upright, frontal position (with tolerance for some side movement).

## License

[Apache 2.0 License](https://github.com/GudarJs/face-recognizer/blob/master/LICENSE)