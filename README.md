# About
Display gifs in the terminal

Also allows searching gifs on Tenor
# Installation
### Linux from source
Run the following command in your shell:
```sh
git clone https://github.com/VojtechNebes/gif-cli.git &&
cd yourrepository &&
chmod +x install.sh &&
sudo ./install.sh
```
# Usage
```
usage: gif-cli [--help] [-f] [-s] [-d DELAY] [-w WIDTH] [-h HEIGHT] gif

display a gif in the terminal

positional arguments:
  gif                   Path or url to the gif file to display.

options:
  --help                show this help message and exit
  -f, --forever         Keep looping the gif until ^C is pressed.
  -s, --search          Treat the gif argument as a search term for searching on Tenor.
  -d DELAY, --delay DELAY
                        Delay between frames in seconds. When not specified, the delay is read from the gif file.
  -w WIDTH, --width WIDTH
                        Maximum width of the output.
  -h HEIGHT, --height HEIGHT
                        Maximum height of the output.
```
### Examples
Open a .gif file and display it:
```sh
gif-cli "/path/to/your/file.gif"
```
Have the displayed gif only take up 20 lines vertically:
```sh
gif-cli "/path/to/your/file.gif -h 20"
```
Display a gif from the internet:
```sh
gif-cli "https://url.of.your/file.gif"
```
Loop the displayed gif forever:
```sh
gif-cli "/path/to/your/file.gif" -f
```
Search for gif on Tenor and display the first result:
```sh
gif-cli "galaxy brain meme" -s
```
