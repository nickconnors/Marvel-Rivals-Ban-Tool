# Marvel Rivals Ban Tool
Leveraging a custom-trained detection model ([yolo11l](https://github.com/ultralytics/ultralytics)) and [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), grab enemy players' names from the Marvel Rivals competitive loading screen and retrieve their hero stats (unofficially - more on that below) via the [Tracker Network](https://tracker.gg/) API, giving you the competitive advantage during the ban phase. This does not read from Marvel Rivals process memory and therefore is undetectable by the anti-cheat. Contributions are welcomed!

## Setup

### Download Tesseract
Navigate to https://github.com/UB-Mannheim/tesseract/wiki and download the Tesseract installer. This project has been developed and tested on version 5.5.0. Please ensure that Tesseract is installed in the following directory:

    C:\Program Files\Tesseract-OCR\tesseract.exe

### Optional: Create Virtual Environment
Navigate to the root project directory and run the following commands:

    python 3.13.2 -m venv mrbt_env
    mrbt_env\Scripts\Activate.ps1

### Install Required Dependencies
Navigate to the root project directory and run the following command:

    pip install -r requirements.txt

## Usage
Navigate to the src directory and run the following command:

    python main.py

The script will wait until 'F8' is pressed. Press this key when all players' names are clearly visible. For example:

![](https://imgur.com/a/13isgvg)

Shortly after you should start seeing each enemy player's top 3 heroes (if applicable).
**Please Note:** The OCR has trouble picking up on non English characters and oddly formatted usernames (e.g., random spaces everywhere). Additionally, some users have opted to hide their stats. Obviously in these scenarios you will not be able to see the particular user's stats.

### Raw Player Stats
If you'd like to get the raw stats provided by the Tracker Network API, please see the following code example:

    from player import Player
	
	player  =  Player("Username")
	stats = player.get_career_stats(season=3)

## Training
The model in this repo is already pretrained (models/best.pt), but I have provided the training script and base model (models/yolo11l.pt) if you would like to custom train your. Much more detailed information to come in a future release, but to custom train your own model, you first need to create a `val` and `train` folder in the project root direct. Then within each of those create a `images` and `labels`. Populate accordingly with your training and validation sets. Labels are to be done in YOLO format with the classes `left_player` and `right_player`.

## Limitations

### OCR Accuracy
Tesseract does a decent job at picking up usernames with all English characters and normal formatting. When other characters are introduced as well as strange formatting, Tesseract will be unable to parse the player properly, resulting in either no player stats returned, or the wrong ones. I tried some other open source models with no luck. I also tried the Google Vision API, which slightly improved cases with multi-language characters, but not nearly enough to justify making this tool cost money to use.

### Lack of Truly Public Marvel Rivals API
There are a few public 3rd party Marvel Rivals APIs out there, but they are limited in capabilities. Tracker Network, however, has incredibly detailed statistics. The catch is their API technically isn't meant for public use. I checked the web requests when fetching my stats on their website and noticed that I could access their endpoint in my browser without any authentication. I was unable to accomplish this in python via the requests library, presumably due to something like Cloudflare. I was unable to bypass it. As a workaround, I concurrently use 6 different headless Selenium drivers. This approach is much slower and is unnecessarily heavyweight. With that being said, it executes more than quick enough to get the players' stats before the ban phase starts.