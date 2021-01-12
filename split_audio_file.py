import os
import sys
import string
import argparse

from pydub import AudioSegment

raw_timestamps = []
segments = []

INVALID_CHARS = "\\/:*?\"<>|" # Windows invalid filename characters

sys.stdin.reconfigure(encoding='utf-8') # for non-english characters

# Filter out invalid characters from filename
def sanitize_filename(raw):
  return ''.join([c for c in raw if c not in INVALID_CHARS]).strip()

# Constraints timestamp to hh:mm:ss
def cleanup_timestamp(raw):
  return ''.join([c for c in raw if c in string.digits or c == ':'])

# Parses hh:mm:ss to milliseconds
def time_to_millis(raw):
  timestamp = list(map(int, raw.strip().split(':')))
  hr, mi, se = (0,0,0)
  if (len(timestamp) == 2): # mm:ss
    mi, se = timestamp
  elif (len(timestamp) == 3): # hh:mm:ss
    hr, mi, se = timestamp
  else: # Raise error
    raise ValueError(f"Incorrectly formatted timestamp: {raw}")
  return ((hr*60+mi)*60+se)*1000

parser = argparse.ArgumentParser(description="Split Audio file based on list of timestamps and filenames")
parser.add_argument('-dir',default="split_mp3",type=str, help="Directory to output split segments")
parser.add_argument('-prepend',default="",type=str, help="Prefix for files (before numeric identifier)")
parser.add_argument('-format',default="mp3",type=str, help="Audio output format for pydub to export")
parser.add_argument('source',type=str, help="Audio source")
args = parser.parse_args()

fname = f"{os.getcwd()}\\{args.source}"
prepend = args.prepend
folder = f"{os.getcwd()}\\{args.dir}"
output_format = args.format

if (not os.path.exists(folder)):
  os.makedirs(folder)

# Expected format:
#   hh:mm:ss <filename: name of this segment>
# Output format:
#   /<current_dir>/<-dir: specified folder>/<-prepend: specified prefix><index: segment input order>_<filename>.<-format: output format>
# e.g.
#   C:/tmp/split_mp3/TEST0_firstSegment.mp3

conut = 0
for line in sys.stdin:
  line = line.split()
  raw_timestamps.append([time_to_millis(cleanup_timestamp(line[0])), f"{folder}\\{prepend}{conut}_{sanitize_filename(' '.join(line[1:]))}.{output_format}"])
  conut += 1

# list(map(lambda x: print(x), raw_timestamps))
num_splits = len(raw_timestamps)

print(f"Loading audio file {fname}...")
audio_file = AudioSegment.from_mp3(fname)
print(f"Audio file loaded. Length: {len(audio_file)}ms", flush=True)

# End Cap
raw_timestamps.append([len(audio_file),"END"])

for i in range(num_splits):
  try:
    output_filename = raw_timestamps[i][1]
    # print(f"{raw_timestamps[i][0]} - {raw_timestamps[i+1][0]}: {output_filename}")
    if (not os.path.exists(output_filename)):
      audio_file[raw_timestamps[i][0]:raw_timestamps[i+1][0]].export(output_filename,format=output_format)
  except Exception as e:
    print("Exception encountered")