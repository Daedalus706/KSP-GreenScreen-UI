# KSP-GreenScreen-UI
This is the repository for the UI overlay I used in [this](https://www.youtube.com/watch?v=kptUQBFPhzQ) video for [Kerbal Space Program](https://kerbalspaceprogram.com/). This is <ins>NOT</ins> a mod for KSP. This program opens a new window that displays the UI elements infront of a green background. The window can then be captured by recording software like [OBS](https://obsproject.com) and leyed ontop of the game footage.

# Installation
This program needs additional software to work.

- The code is written in Python so it needs [Python 3](https://www.python.org) (latest version recommended) to run. If you have never used Python before, make sure to select the `add to PATH enviroment variable` checkbox during installation.

- The program needs the third party library [pygame](https://www.pygame.org). To install pygame run `pip install pygame` or `python -m pip install pygame` in a consol window. If this does not work, python is either not installed or added to PATH. In the second case follow [these](https://realpython.com/add-python-to-path/) steps

- To get the telemetry data from the game, the program also needs the mod [Simpit Revamped](https://forum.kerbalspaceprogram.com/topic/204852-112x-simpit-revamped-simpit-20/). Just follow the installation guide on the forum page.

- Simpit Revamped is made for communication between KSP and a micro controller like an Arduino. However we want to use it to communicat with another program, so we need another thirs party software to create virtual COM ports. I use [com0com](https://sourceforge.net/projects/com0com/). Again, just follow the installation steps of com0com. You might need to restart the computer to finish the installation. After that two new virtual COM-ports should be available (COM5 and COM6 by default). Select one in the Settings.cfg file of Simpit Revamped `\GameData\KerbalSimpit\Settings.cfg` and the other in `KSP-GreenScreen-UI\Settings.cfg`

After all the steps above are complete, you are ready to go.

# Using KSP-GreenScreen-UI with OBS
The following steps are for OBS 20.2.3. The UI of OBS might be different in other versions, so the steps 3 and 4  might differ.

1. Start KSP and launch a craft and make sure the KerbalSimpit Status is `WAITING_HANDSHAKE`. 

2. Run `KSP_GeenScreen_UI.py` inside the `KSP-GerrnScreen-UI` folder

3. Add OBS source
    - Start OBS
    - click the `+` icon in the `Sources` tab to add a new source 
    - select `Window Capture`
    - click `OK`
    - select Window: `[python.exe] KSP GreenSecreen UI`

4. Remove the green background 
    - right click on `Window Capture` (or however you renamed the source) in the Sources tab
    - click on `Filters`
    - click on the `+` icon under `Effect Filters`
    - Select `Color Key` and press `Ok`
    - If any green artefacts are visible change the `Similarity` slider


# Settings
In the `Settings.cfg` file of KSP-GreenScreen-UI you can set the width and height of the window and the target frame rate. But keep in mind that a higher frame rate does not mean that the UI elements update faster. 

To change the update rate of the UI elements, change the `RefreshRate` in `Settings.cfg` file in the KerbalSimpit folder. This value is the refresh rate in milliseconds, so for example a refresh rate of 20 FPS equals 50 ms. 

Also the baud rate of both settings files need to be euqal. A boud rate of 112500 is recommended.

# Notes and known issues
Known issues:
- If you leave a scene (reverting a flight or going back to the KSC) the UI elements stop working correctly. In this case, restart the program.
- Restarting the program after the error above, the UI elements might still not work correctly. In this case restart again.