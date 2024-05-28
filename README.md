# FrameByFrame

Allows you to edit a video to remove dust and scratches. The video can then be re-encoded using various AI scaling models.

## Windows Installation

**Install Python 3.11.9:**

We require python < 3.12 because of a compatiblity problem with lmdb

Download [Python 3.11.9](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)

Open the downloaded file to install python

Select the "Use admin privileges when installing py.exe" option

Select the "Add python.exe to PATH" option

Click on "Install Now"

**Open Command Prompt as Administrator:**

Search for "Command Prompt" in the Start Menu, right-click it, and select "Run as administrator."

**Install ffmpeg:**

`winget install --id Gyan.FFmpeg`

Reboot the computer

**Open Command Prompt as Administrator:**

Search for "Command Prompt" in the Start Menu, right-click it, and select "Run as administrator."

**Change directory to where you download FrameByFrame:**

`cd path\to\FrameByFrame`

**Create the virtual environment:**

`python -m venv path\to\FrameByFrame\fbfenv`

**Activate the virtual environment:**

`path\to\FrameByFrame\fbfenv\Scripts\Activate.bat`

**Install required python modules:**

`pip install --upgrade -r requirements.txt`

**Run the application:**

`python ./src/FrameByFrame.py`

**To run the application in the future:**

Open a Command Prompt
 
`path\to\FrameByFrame\fbfenv\Scripts\Activate.bat`

`python path\to\FrameByFrame\src\FrameByFrame.py`

## Linux Install:

**To install on debian based systems:**

`sudo apt install python3.10-venv ffmpeg pip`

**To install on Arch Linux based systems:**

`sudo pacman -S python-virtualenv ffmpeg`

**Change directory to where you download FrameByFrame**

`cd path/to/FrameByFrame`

**Create a python virtual environment:**

`python3 -m venv fbfenv`

**Activate the virtual environment:**

`source fbfenv/bin/activate`

**Install the requied python modules:**

`pip install --upgrade -r requirements.txt`

**Run the application:**

`python ./src/FrameByFrame.py`

**To run the application in the future:**

`source path/to/FrameByFrame/fbfenv/bin/activate`

`python path/to/FrameByFrame/src/FrameByFrame.py`

# Usage:
Click on *File->Image Directory*

Then select the working directory for the video you want to work on.

Click on *File->Convert To Images*

Then select the video you want to work on

Click on *File-> Convert To Video*

Then select the video you are working on. This will convert the images back into a video using the settings in the application.

### Main controls:
**SSIM Threshold:** This is used when scanning the video to find similar images. The scanning will stop when the similarity of two images is greater than the SSIM threshold.

**Previous:** Moves to the previous frame in the video

**Scan:** This will scan through the video looking for pairs of frames that have a SSIM greater or equal to the current SSIM Threshold value.

**Next:** Moves to the next frame in the video

**Edit Image:** allows you to edit the frame being displayed on the left of the FrameByFrame window

**Mask: Allows:** you to mask off parts of an image. Masked areas will not be copied when copying images.

**Undo:** Allows you to undo an edit on a frame

**Copy:** Copies the frame displayed in the left of the window over then next frame in the video:

**Copy From:** selects the frame displayed in the left of the window.

**Copy To:** Copies the frame selected with **"Copy From"** over all frames up to and including the frame displayed in the left of the window

### Picture enhancement controls:
**Scaling:** Use this to select the scaling method you want applied to the video

**White Balance:** Selects whether or not to apply white balance to the video

**Enhance Colour:** When selected allows you to alter contrast and brightness of the video

### Encoder Controls:
**Preset:** Sets the ffmpeg x265 optimising preset

**Chroma:** Sets the ffmpeg x265 chroma subsampling

**CRF:** Sets the ffmpeg x265 constant rate factor

**Threads:** The number of simultaneouly generated frames. If you are using Hardware encoding then this must be set to 1 as Nvidia's CUDA library is not thread safe.

**Crop Top:** allows you to crop the top of the video

**Crop Left:** allows you to crop the left of the video

**Crop Right:** allows you to crop the righ of the video

**Crop Bottom:** allows you to crop the bottom of the video

### Editor controls
**Left Mouse Button:** copies pixels from previous frame to frame being edited

**Right Mouse Button:** copies pixels from next frame to frame being edited

**Middle Mouse Button:** Blends the pixels at the location of the cursor

**S:** Save the edited frame

**X:** Cancel editing the frame

**Plus (+) or Equals (=):** Increase the affected area when using mouse buttons

**Minus (-):** Decrease the affected area when using mouse buttons

# Scaling model Licences

[EDSR](https://github.com/Saafke/EDSR_Tensorflow) model is released under the Apache License 2.0 license

[FSRCNN](https://github.com/Saafke/FSRCNN_Tensorflow) model is released under the Apache License 2.0 license

[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN/tree/master) model is released under the BSD 3-Clause "New" or "Revised" License

[RealESRGAN_x4plus_anime_6B](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/anime_model.md) model is released under the BSD 3-Clause "New" or "Revised" License

[realesr-animevideov3](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/anime_video_model.md) model is released under the BSD 3-Clause "New" or "Revised" License

[Rybu](https://openmodeldb.info/models/4x-Rybu) model is released under the CC0-1.0 License

[UltraSharp](https://openmodeldb.info/models/4x-UltraSharp) model is released under the CC-BY-NC-SA-4.0 License


[realesr-animevideov3](https://github.com/xinntao/Real-ESRGAN/blob/master/docs/anime_video_model.md) model is released under the BSD 3-Clause "New" or "Revised" License

[Rybu](https://openmodeldb.info/models/4x-Rybu) model is released under the CC0-1.0 License

[UltraSharp](https://openmodeldb.info/models/4x-UltraSharp) model is released under the CC-BY-NC-SA-4.0 License
