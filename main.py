#!/usr/bin/env python

from PIL import Image, UnidentifiedImageError
import time, os
import argparse, sys
from io import BytesIO
import requests
import validators
import pathvalidate


def _resizeImage(image: Image.Image, max_size, wide: bool):
    """Resize the image without maintaining aspect ratio."""
    if wide:
        image = image.resize((terminalWidth // 2, max_size[1]), Image.LANCZOS)
    else:
        image.thumbnail(max_size, Image.LANCZOS)
    return image

def _formatSorter(format):
    if format["url"].endswith(".gif"):
        return format["dims"][0] * format["dims"][1]
    else:
        return -1

def _getTenorUrl(searchTerm: str, apiKey: str, limit: int = 1) -> str:
    url = f"https://g.tenor.com/v2/search?q={searchTerm}&key={apiKey}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        if len(data["results"]) == 0:
            print("didnt find anything on Tenor.")
            sys.exit(1)

        formats = list(data["results"][0]["media_formats"].values())
        return max(formats, key=_formatSorter)["url"]
    elif response.status_code == 400:
        print("the server could not understand the request because of invalid syntax")
        sys.exit(1)
    else:
        print(response.status_code)
        print(response.headers)
        print("Failed to fetch GIFs from Tenor")
        sys.exit(1)

def _downloadFromTenor(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download GIF from Tenor")
        sys.exit(1)

def _processGif(img, output_size: tuple[int, int], wide: bool) -> list[tuple[Image.Image, float]]:
    try:
        with img:
            frames = []
            try:
                while True:
                    # Get the current frame and resize it
                    frame = _resizeImage(img.copy(), output_size, wide)
                    
                    # Append the resized frame to the frames list
                    frames.append((frame, frame.info["duration"]))
                    
                    # Move to the next frame
                    img.seek(img.tell() + 1)
            except EOFError:
                pass  # that was the last frame

            return frames
    except (UnidentifiedImageError, IsADirectoryError, FileNotFoundError) as e:
        print(e)
        sys.exit(1)

def _printImage(image: Image.Image):
    pixels = image.load()

    rows = []

    for y in range(image.size[1]):
        row = ""

        for x in range(image.size[0]):
            pixel = pixels[x, y]
            r, g, b = pixel[0], pixel[1], pixel[2] # cant do a simple unpack, because sometimes theres also alpha channel
            row += f"\033[48;2;{r};{g};{b}m" + "  "
        
        rows.append(row)
    
    # print everything at once to prevent tearing when stopped
    print("\n".join(rows))

def run(frames: list[tuple[Image.Image, float]], delay: float):
    try:
        for i, frame in enumerate(frames):
            if i == 0: continue # skip first frame for some reason

            image = frame[0]

            _printImage(image)
            
            # go back at the start of the gif to overwrite the lines next frame
            print(f"\033[{image.size[1]}A", end="")

            time.sleep(delay or frame[1]/1000) # when delay is None, use delay from gif
    except KeyboardInterrupt:
        sys.exit(0)



if __name__ != "__main__": sys.exit()



parser = argparse.ArgumentParser(description="display a gif in the terminal", conflict_handler="resolve")

parser.add_argument(
    "gif",
    type=str,
    help="Path or url to the gif file to display."
)

parser.add_argument(
    "-f",
    "--forever",
    dest="forever",
    action='store_true',
    help="Keep looping the gif until ^C is pressed."
)

parser.add_argument(
    "-s",
    "--search",
    dest="search",
    action='store_true',
    help="Treat the gif argument as a search term for searching on Tenor."
)

parser.add_argument(
    "-d",
    "--delay",
    dest="delay",
    type=float,
    help="Delay between frames in seconds. When not specified, the delay is read from the gif file."
)

terminalWidth, terminalHeight = os.get_terminal_size()

parser.add_argument(
    "-w",
    "--width",
    dest="width",
    type=int,
    default=terminalWidth,
    help="Maximum width of the output."
)

parser.add_argument(
    "-h",
    "--height",
    dest="height",
    type=int,
    default=terminalHeight-1,
    help="Maximum height of the output."
)

parser.add_argument(
    "-ww",
    "--wide",
    dest="wide",
    action='store_true',
    help="Use the full width of the terminal."
)

args = parser.parse_args()

if args.search:
    url = _getTenorUrl(args.gif, "AIzaSyAgVX5sxv-5uBTfzLB_-IbcwufxwpheppM")
    gif = _downloadFromTenor(url)
    
    frames = _processGif(Image.open(BytesIO(gif)), (args.width, args.height), args.wide)
elif validators.url(args.gif):
    gif = _downloadFromTenor(args.gif)
    frames = _processGif(Image.open(BytesIO(gif)), (args.width, args.height), args.wide)
elif pathvalidate.is_valid_filepath(args.gif):
    frames = _processGif(Image.open(args.gif), (args.width, args.height), args.wide)
else:
    print("The gif argument is not valid")

# get height of the gif frame
height = frames[0][0].size[1]

# "allocate" this many empty lines
# this is to prevent issues with automatic scrolling
print("\n"*(height), end="")
print(f"\033[{height}A", end="")

# turn of echo
os.system("stty -echo")

# display the gif forever or once
if args.forever:
    while True:
        run(frames, args.delay)
else:
    run(frames, args.delay)
