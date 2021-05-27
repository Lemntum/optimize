# Introduction

The `optimize.py` script automates the process of losslessly optimizing the size of of many types of files. It does this by tying together the functionality of various external programs to make the process easier.

Currently optimizes:

* png (optionally convert png to webp)
* jpg
* webp
* zip
* gzip
* flac (and convert wav to flac)
* OpenDocument files

Additional options may be enabled for destructive optimizations, but they are never enabled by default. See the help (`-h`) for options.

The script will do its best to prevent accidently damaging files, but you should not rely on this. Always create a backup before running anything on your files.


# Usage

Read the help info for usage information.

	optimize.py -h


# Linux Install

First install the dependencies. Then the script can be run as-is through the Python 3 interpreter.

For example, on Debian:

	python3 optimize.py

On Arch, Python 3 is the default interpreter, but you may specify the version number if you'd like.

Optionally, add the script to a `scripts` directory and add it to your PATH so the script can easily be run from anywhere.


## Install Dependencies

Install the following dependencies using your favorite package manager:

* [Python 3](https://www.python.org/downloads/)
* [7zip](https://www.7-zip.org/)
* [AdvanceCOMP Utilities](https://www.advancemame.it/comp-readme)
* [cwebp](https://developers.google.com/speed/webp/docs/cwebp)
* [flac](https://xiph.org/flac/)
* [jpegoptim](https://github.com/tjko/jpegoptim)
* [optipng](http://optipng.sourceforge.net/)
<!--* pngcrush (not yet used)-->

On Arch:

	sudo pacman -S python python-pip p7zip advancecomp libwebp flac jpegoptim optipng

On Debian/Ubuntu:

	sudo apt install python3 python3-pip p7zip-full advancecomp webp flac jpegoptim optipng


## (Optional) Create a `scripts` directory

For convenience, create a script directory that will hold your private scripts and add it to your PATH. You can create the `scripts` directory wherever you'd like. The following example will assume it is placed at `~/.local/scripts`.

First, create the directory.

	mkdir ~/.local/scripts

Then move the script into the newly created directory.

	mv optimize.py ~/.local/scripts/optimize.py

Give the script executable permission.

	chmod +x ~/.local/scripts/optimize.py

Finally, add the `scripts` directory to your PATH. To do this permanently, open up `~/.profile` in your favorite text editor and add the following lines:

```sh
# set PATH so it includes user's private scripts if it exists
if [ -d "$HOME/.local/scripts" ] ; then
	PATH="$HOME/.local/scripts:$PATH"
fi
```

This will add the `scripts` directory to your PATH each time you log in. If you are already logged in, you will need to log out and back in for it to take effect. Or you can use [another option](https://www.howtogeek.com/658904/how-to-add-a-directory-to-your-path-in-linux/).

Now you can run the script anywhere by typing `optimize.py [files]`.



# Windows Install

Installing on Windows is simple, but the process of installing dependencies is not. Consider instead using the [Windows Subsystem for Linux Install](#windows-subsystem-for-linux) method. 

First, install the Python interpreter. Then install the necessary dependencies.

Once installer, the script can be run using the python interpreter. It is suggested to run the script through PowerShell so you can easily use wildcards as input.

```
py -3 optimize.py [files]
```

On a native Windows install, it is recommended to run the script using PowerShell so PowerShell shell expansions can be used.

Examples:

```powershell
py -3 optimize.py (get-item *)
py -3 optimize.py (get-item *.jpg)
```

## Install Dependancies

Most things will need to be installed in a variety of ways. Details are described below.

**WARNING:** Please read [Updating the Windows PATH](#updating-the-windows-path) before updating your PATH.

<!--
### Using the install script

The script `windows-install-dependancies.py` will attempt to retrieve and install all the dependancies. However, it has not been well tested and may be prone to failure. Additionally, it does not ensure that the most up-to-date version of each dependancy is installed.
-->

### Manual Installation

The safest way to install the dependancies on Windows is to manually install each item according to the directions below.

#### Python

A Python interpreter is necessary to run the Python script. It is suggested to use the official CPython interpreter. 

Download the most recent version of the Windows installer from the [Downloads page](https://www.python.org/downloads/). On Windows 7, you will need version 3.8.

Run the installer. Ensure the following Optional Features are checked:

* pip
* py launcher

And ensure the following Advanced Options are checked:

* "Associate files with Python (requires the py launcher)"
* "Add Python to environment variables"

Additional options may be enabled at your preference.

Complete the installation. If it succeeds, you should now be able to run Python scripts.


##### (Recommended) Python Magic

[Python Magic](https://pypi.org/project/python-magic/) is used to determine a file's type. It will be automatically installed by the script if it is not available. If Python Magic cannot be installed, it will fall back to the less reliable method of using a file's extension.

Optionally, you may manually install it. Use pip to install python-magic and the [Python Magic binaries](https://pypi.org/project/python-magic-bin/0.4.14/).

	python -m pip install python-magic python-magic-bin==0.4.14


##### (Recommended) Winreg

Python tool for interfacing with the Windows registry. Necessary for finding the location of 7zip.

Installation is handled automatically by the script if missing.

You can manually install using pip.

	python -m pip  install winreg



### Program Dependancies

Each program needs to be installed in its own special way. When installing programs, you can put them in any of 3 places.

1. Inside `C:\Program Files\`
2. Inside `%APPDATALOCAL%\`
3. Anywhere, as long as the executable is in your system's PATH.

The script will be able to locate the executables using the first two as long as they conform to the expected directory structure. The third is more reliable, unless your PATH variable becomes too long.

If you are having issues extracting an archive to `Program Files` or `%APPDATALOCAL%`, use 7zip. The native Windows archive extractor will fail if the UAC prompt activates.


#### 7zip

Source: https://www.7-zip.org/

Download the most recent Windows installer and run it. Install to the default location for best results.

Expected places:

* `C:\Program Files\7-zip\7z.exe`
* `%APPDATALOCAL%\7-zip\7z.exe`


#### AdvanceCOMP Tools (Advzip and Advpng)

Source: https://www.advancemame.it/download

1. Download the most recent release.

2. Create a folder labled `advancecomp` in the desired install location.

3. Extract the contents of the zip file to the `advancecomp` folder. The final structure should be either of:
    * `C:\Program Files\advancecomp\advzip.exe`
    * `%APPDATALOCAL%\advancecomp\advzip.exe`
  
        and
   
    * `C:\Program Files\advancecomp\advpng.exe`
    * `%APPDATALOCAL%\advancecomp\advpng.exe`


#### cwebp

Source: https://developers.google.com/speed/webp/docs/precompiled

Direct Source: https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html

<!-- https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.2.0-windows-x64.zip -->

1. Download the most recent Windows version that is not a release candidate. (The files should not have `-rc` in the title.)

2. Open the zip archive.

3. Extract the top level folder inside the archive to either `C:\Program Files` or `%APPDATALOCAL%`. 

4. Rename the extracted file to be simply `libwebp`. The final structure should be either:
    * `C:\Program Files\libwebp\bin\cwebp.exe`
    * `%APPDATALOCAL%\libwebp\bin\cwebp.exe`



<!--
## FFmpeg

FFmpeg is not yet used by the optimize script.

https://www.wikihow.com/Install-FFmpeg-on-Windows

1. Download from here: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
2. Extract
3. Move and rename extracted folder
4. Add new directory to the $PATH (setx /m PATH "C:\Program Files\ffmpeg\bin;%PATH%")
5. Remember to execute the name with a .exe on the end
-->

#### flac

Source: https://xiph.org/flac/

1. Download the most recent version of flac from the [official ftp](https://xiph.org/flac/download.html). The Windows version should be named with the naming scheme `flac-X.Y.Z-win.zip`.

2. Create a folder labled `flac` in the desired install location.

3. Open the zip file. The contents should be in their own folder.

4. Enter the top level folder and extract all of its contents to the created `flac` folder.

5. Inside the flac folder, create a `version.txt` file. Add the version information to its contents and save. The final structure should be either:
    * `C:\Program Files\flac\win64\flac.exe`
    * `%APPDATALOCAL%\flac\win64\flac.exe`


##### Updating flac

In the future if flac needs to be updated, download the new version and move the contents into the current flac directory, overwriting the contents. Update the version number in `version.txt`. The System PATH should not need to be updated.


#### jpegoptim

The [jpegoptim](https://github.com/tjko/jpegoptim) project does not include precompiled Windows binaries. Instead, download the unofficial precompiled binaries from here: https://github.com/XhmikosR/jpegoptim-windows/releases/

<!--[Chocolatey](https://chocolatey.org/packages/jpegoptim) has a package, but the upstream source no longer exists.-->

1. Download the most recent version from [here](https://github.com/XhmikosR/jpegoptim-windows/releases/) or compile the [original source](https://github.com/tjko/jpegoptim) yourself.

2. Open the zip archive.

3. Extract the top level folder inside the archive to either `C:\Program Files` or `%APPDATALOCAL%`. 
 
4. Rename the extracted folder to be named `jpegoptim`. The final structure should be either:
    * `C:\Program Files\jpegoptim\jpegoptim.exe`
    * `%APPDATALOCAL%\jpegoptim\jpegoptim.exe`


<!--
### Mozjpeg

https://github.com/mozilla/mozjpeg

Improved JPEG algorithm. May be superceded by [JPEG XL](https://en.wikipedia.org/wiki/JPEG_XL).

### JPEG XL (JXL)

* https://jpeg.org/jpegxl/
* https://gitlab.com/wg1/jpeg-xl

Supported by imagemagick. https://imagemagick.org/script/formats.php#supported
-->


#### optipng

Source: http://optipng.sourceforge.net/

Please note that the Windows version of OptiPNG is 32-bit only. As such, if you are running a 64-bit version of Windows and you want to place it inside the `Program Files` folder, it should go under the folder `Program Files (x86)` for 32-bit software.

1. Download the most recent version.

2. Open the zip archive.

3. Extract the top level folder inside the archive to either `C:\Program Files (x86)` or `%APPDATALOCAL%`. 
 
4. Rename the extracted folder to be named `optipng`. The final structure should be either:
    * `C:\Program Files (x86)\optipng\optipng.exe`
    * `%APPDATALOCAL%\optipng\optipng.exe`

<!--
### pngcrush (not yet used)

Source: (pending)


### PNGOUT

http://www.jonof.id.au/kenutils.html

May provide better compression, but is slower?
-->



### Updating the Windows PATH

Updating the PATH on Windows can be a special challenge. 

First you must consider if you wish to update the System or the User PATH. It is recommended that you update User PATH, because it is safer.

**CAUTION: Consider backing up your current PATH variable to restore later if something goes wrong.**


#### Update the System PATH Using the GUI

The easiest way to update the System PATH is through the GUI. From the desktop: 

1. Right Click "Computer"
2. Click "Properties" in the drop-down menu
3. Click "Advanced system settings"
4. Enter an administrator password at the AUC prompt.
5. Click to the "Advanced" tab
6. Click the button "Environment Variables..."
7. In the section labled "System variables", scroll down to find one with the name "Path"
8. Select "Path" by clicking on it, then click the button "Edit..."
9. In the field for "Variable value", add the new path location to the end. Seperate each location with a semicolon (`;`).
10. Click the button "OK" to make the change.
11. Click the button "OK" again to confirm the change.
12. Close out of the System Properties window. You can do this by clicking the button "OK".


#### Update the User PATH Using the GUI

Steps vary significantly for changing the user's PATH variable: https://docs.microsoft.com/en-US/troubleshoot/windows-client/performance/cannot-modify-user-environment-variables-system-properties#resolution

The following method has only been tested on Windows 7. Steps will differ between different versions of Windows.

A user's PATH can be updated through the User Accounts options.

1. Open the Control Panel
2. Click on "User Accounts and Family Safety"
3. Click on "User Accounts"
4. Select the account who's PATH you want to update.
5. Click "Change my environment variables"
6. Under the area labled "User variables for [user]", select the PATH variable.
7. Click the "Edit..." button.
8. Update the desired PATH under the field for "Variable value", and click "OK".
9. Close out of the Environment Variables window and the Control Panel.


#### Using `setx`

**WARNING: `setx` can only update a path up to 1024 characters in length. If it goes longer than this, it will be truncated.**

The intended way to update the Windows PATH is to use the `setx` command from the CMD. 

Open the CMD and run the command:

	setx /M PATH "%PATH%;C:\New\Path\Here"

The `setx` command *must* be run using cmd; **not** PowerShell. If run from PowerShell, shell expansion will not work and your entire PATH will be overwritten.

You likely will not have issues if running `setx` manually from CMD.

<!--
#### Other Methods

If you do encounter issues with the above methods not working, try using another method to update the PATH.

The safer way to edit the PATH may be directly throught the Registry. This can only ever be a temporary fix, as the PATH used by the registry is copied out from some mystery location and will be reset when the computer restarts. It *must* be set through the shell.
* https://stackoverflow.com/questions/35246896/adding-a-directory-to-the-system-path-variable-through-registry
* https://stackoverflow.com/questions/15434521/how-to-update-path-variable-permanently-using-php
* https://stackoverflow.com/questions/1919125/programmatically-adding-a-directory-to-windows-path-environment-variable?rq=1
-->
<!--
#### Automation Issues

NSIS installer will truncate the PATH if it is over 1024 bytes in length. (This limitation is present in the `setx` command as well.)
https://nsis.sourceforge.io/Path_Manipulation
https://stackoverflow.com/questions/31340823/update-path-environment-variable-using-nsis

There is a plugin which should be safer. https://nsis.sourceforge.io/EnVar_plug-in

This is lifted to 8192 bytes in the "Large Strings" build. https://nsis.sourceforge.io/Special_Builds

Someone wrote a special tool just for it. https://github.com/awaescher/PathEd

Even DotNet struggles with it. https://github.com/dotnet/runtime/issues/1442
-->

#### Troubleshooting

If you overwrite your existing PATH information, other tools may stop working. 

On Windows 7, the default PATH is:

	%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\

If you had Python installed, you can run the installer again to update the PATH for Python.


<!--

My PATH is:

	%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;C:\Program Files\dotnet\;C:\Program Files\ffmpeg\bin;C:\Program Files\flac\win64
-->
<!--
### Remove items from the Windows PATH

To remove a directory from PATH, use

	setx /M PATH "%PATH%;C:\Program Files (x86)\Git\bin;=%"

I haven't tested this. You can also try this: https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/
-->


## (Optional) Create batch script to launch the script

Create a new text file and rename it to `optimize.bat`. Add the lines:

```bat
@echo off
py -3 C:\Users\Username\scripts\optimize.py %*
```

Change the second line to be at the correct path where you put the script.

Save it. Now place the batch file somewhere in your PATH. 
[Update PATH](#updating-the-windows-path) if necessary.

Now you can run the script anywhere by using `optimize.bat [files]`.



# Windows Subsystem for Linux Install

Installing under WSL is untested, but should run without issues. This should also fix a number of issues that occur when running under Windows normally (PATH will not be truncated, aliasing will work correctly, color output will be available, better wildcard expansions available, and optimizers may be faster).

1. Install either Debian or Ubuntu through [WSL through the official means](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

2. Continue as normal through the [Linux Install](#linux-install). Use the Debian/Ubuntu command to install dependancies. 
    * If using openSUSE, you will need to find the correct package names and install them using [YaST](https://en.opensuse.org/YaST_Software_Management) or [zypper](https://doc.opensuse.org/documentation/leap/reference/html/book.opensuse.reference/cha-sw-cl.html).



# Troubleshooting

## Script fails to run

Ensure you have Python 3 installed and are using the Python 3 interpreter.

If on Windows, also make sure Python is in your PATH. You will have needed to install the py launcher to use `py` commands.


## A dependancy is installed, but the script can't find it

If running under Windows, ensure that the directory it is installed to matches exactly with the expected location. Make sure the directory holding the install was renamed accordingly. If it still does not work, try a different location, or adding it to your PATH instead.

If you still encounter issues, you may have to modify `optimize.py` to include the installed path.

Open it in any competent text or code editor (not Windows Notepad) and search for the line `# Find if programs exist on the system path or expected default locations, then add them.` to find the beginning of the section where locations are specified. Scroll down to where the optimizer you want is defined, and add your path to the list of checked paths.

For example:

```py
	flac = check_paths(
		which('flac.exe'),	
		#check_registry_location('flac.exe'),
		f"{programfiles}\\flac\\win64\\flac.exe", 
		f"{localappdata}\\flac\\win64\\flac.exe",
		f"{programfiles32}\\flac\\win32\\flac.exe"
	)
```

becomes

```py
	flac = check_paths(
		f"C:\\place\\installed\\flac.exe",
		which('flac.exe'),	
		#check_registry_location('flac.exe'),
		f"{programfiles}\\flac\\win64\\flac.exe", 
		f"{localappdata}\\flac\\win64\\flac.exe",
		f"{programfiles32}\\flac\\win32\\flac.exe"
	)
```

You will need to escape every backslash (`\`) in a Windows path.

If the issue *still* persists, then the issue is likely Windows. Try [installing through WSL](#windows-subsystem-for-linux-install) instead.


## AdvanceCOMP Tools (advzip/advpng) hangs on Windows

On Windows, advpng may hang after running. Open the Task Manager and check that `advpng.exe` is using no CPU.

If it is still using CPU, it means advpng is still running. Large image files may take a long time.

If it is not, return to the PowerShell window and press ctrl+c to cancel the process. It should output the finished file. 
