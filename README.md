# vidz

Clean and convert .ts to .avi

# Initialization

- `git clone <repo>`
- `cd <repo>`
- `py -m venv .venv` *(.venv is the directory name)*
- `.\.venv\Scripts\activate` *(on windows)*
- *...we are now in the virtual environment, so all pip commands will apply to the .venv...*
- `py -m pip install -r requirements.txt`

*[common venv commands help](https://gist.github.com/m-ll/f2d92237b9b1aa47c0b8c79d880b8e56)*

# Usage

### Common

- `split-and-clean.py -i b8 -t`
- `split-and-clean.py -i b8`

### Split original file, concatenate parts and convert it

```
(.venv) .>split-and-clean.py -h

usage: split-and-clean.py [-h] [-i INPUT [INPUT ...]] [-t [TEST_SOUND]]

Clean and convert .ts to .avi.

options:
  -h, --help            show this help message and exit
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]
                        List of id in the xml
  -t [TEST_SOUND], -d [TEST_SOUND], --test-sound [TEST_SOUND]
                        Test sound on small interval
```

### Examples

- fully clean and convert the video  
`split-and-clean.py -i b8`
- convert 1min of the video starting at 10min  
`split-and-clean.py -i b8 -t`
- convert 1min of the video starting at 15min (if at 10min, it is not relevant)  
`split-and-clean.py -i b8 -t 15`
