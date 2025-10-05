# imgdown 📸

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg )](https://www.python.org/downloads/ )
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg )](https://opensource.org/licenses/MIT )
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg )](https://github.com/psf/black )

A fast and powerful asynchronous image downloader for your command line. Download hundreds of images in seconds, not minutes.

![imgdown Usage Demonstration](https://i.imgur.com/TqBw1aF.gif )
*(Illustrative usage GIF)*

## ✨ Features

*   **Extremely Fast:** Uses `asyncio` and `aiohttp` to perform dozens of concurrent downloads.
*   **Intelligent:** Automatically detects the correct file extension (`.jpg`, `.png`, `.gif`, etc. ).
*   **Flexible:** Provide URLs directly, from a text file, or both.
*   **Organized:** Saves everything to a default folder (`~/Pictures/imgdown_downloads`) or a location of your choice.
*   **Safe:** Avoids duplicate downloads and non-image files.

## 📦 Installation

The recommended way to install a Python command-line tool is with `pipx`. It installs the package in an isolated environment and makes the command globally available, without messing with your system dependencies.

1.  **Install `pipx` (if you don't have it yet):**
    ```bash
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```
    *(You might need to restart your terminal after this step)*

2.  **Install `imgdown` with `pipx`:**
    ```bash
    pipx install git+https://github.com/joao-pedro-farias/image_downloader_cli.git
    ```

That's it! The `imgdown` command is now available anywhere in your terminal.

## 🚀 How to Use

`imgdown` is very easy to use. You can pass URLs directly as arguments or point to a text file.

### Basic Usage

**Download a few images by passing URLs directly:**
```bash
imgdown https://i.imgur.com/S4aG26D.jpeg https://i.imgur.com/W7a3j45.png
```

### Downloading from a File

Create a file named `urls.txt` with one URL per line:

```
# urls.txt

# Comments are ignored
https://images.unsplash.com/photo-1533738363-b7f9aef128ce
https://images.unsplash.com/photo-1574158622682-e40e69841006

# Blank lines are also ignored
https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e
```

Now, use the `-f` or `--file` flag:
```bash
imgdown -f urls.txt
```

### Combining Everything

You can pass direct URLs and a file at the same time. `imgdown` is smart enough to remove any duplicates.

```bash
imgdown -f urls.txt https://i.imgur.com/another-image.gif
```

### Advanced Options

**Specify a destination folder (`-o` or `--output` ):**
```bash
imgdown -f urls.txt -o ./my_cat_pictures
```

**Control the number of concurrent downloads (`-c` or `--concurrent`):**
If you're on a slow connection or downloading from a sensitive server, you can reduce the number of parallel downloads.

```bash
# Download a maximum of 3 images at a time
imgdown -f urls.txt -c 3
```

### Getting Help

To see all available options at any time:
```bash
imgdown --help
```

---

Developed with ❤️ by João Pedro Farias.

