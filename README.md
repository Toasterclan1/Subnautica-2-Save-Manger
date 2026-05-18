# Subnautica 2 Save Sharer
A simple Python Tkinter utility to read metadata from Subnautica 2 .sav files and package them into zip archives for easy sharing with other players.

Made by toasterclan1 (Discord: @toaster_clan_1 or @toasterclan1)

## Features
Parses save game files to extract the display name, game mode, and timestamp.

Simple GUI for selecting files and exporting them.

Packages the target save file into a compressed .zip folder automatically.

## Requirements
Python 3.x

Tkinter (usually included with standard Windows Python installations)

## How to Run
You can start the script via your terminal or command prompt:

Bash
python main.py
How to Use
Packaging a Save
Click Select File and locate your Subnautica 2 save game (.sav).

Verify the parsed file info displayed in the application UI.

Click Save to zip and select the folder where you want to output the compressed file.

## Importing a Shared Save
If someone sends you a zip file created with this tool:

Locate your Subnautica 2 save folder. It is typically found at:
C:\Users\[YourUsername]\AppData\Local\Subnautica2\Saved\SaveGames
(Note: You may need to enable "Show hidden files" in Windows Explorer to see the AppData folder).

Back up your existing saves before moving any new files over.

Extract the .sav file from the zip archive into your SaveGames folder.

Important: If the extracted file shares the same name as one of your current saves (e.g., savegame_0_1.sav), rename the incoming file to an unused slot (e.g., savegame_5_1.sav) so you do not overwrite your own progress.

## Support
If you run into issues or have questions, reach out on Discord: @toasterclan1.


# RoadMap

## By 25/05/2026

- **New Features such as importing zips**

- **Automatic File naming (in testing)**

## By 01/06/20

- **All Features Added, full release**