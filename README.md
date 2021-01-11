# Audio Splitter python script

Quick and dirty python script to read via standard input some list of timestamps and segment names deliminating the start of each segment within a longer audio file.

## Prerequisites

- Install [pydub](https://pypi.org/project/pydub/) i.e. `pip install pydub`.
- Install ffmpeg

### Installing ffmpeg on Windows
Download binaries for ffmpeg and ffprobe here: https://ffbinaries.com/downloads.

Extract .exe binaries into a folder and add the folder into path environment variable.

# Sample Usage
```
PS> Get-Content audio_segment_timestamps.txt | python split_audio_file.py audio_file.mp3
bash> cat audio_segment_timestamps.txt | python split_audio_file.py audio_file.mp3

> python split_audio_file.py -h
usage: split_audio_file.py [-h] [-dir DIR] [-prepend PREPEND] [-format FORMAT] source

Split Audio file based on list of timestamps and filenames

positional arguments:
  source            Audio source

optional arguments:
  -h, --help        show this help message and exit
  -dir DIR          Directory to output split segments
  -prepend PREPEND  Prefix for files (before numeric identifier)
  -format FORMAT    Audio output format for pydub to export
```

## Audio Segment Timestamps config file format
```
hh:mm:ss name of segment
```

List of lines specifying the start time of this segment and its name separated by a whitespace.

## Output format
```
# Output format:
#   /<current_dir>/<-dir: specified folder>/<-prepend: specified prefix><index: segment input order>_<filename>.<-format: output format>
# e.g.
#   C:/tmp/split_mp3/TEST0_firstSegment.mp3
```
