# Fix Subtitles

This script changes the subtitle times (linearly) in `.srt` files to better align with a video.
The middle of a `.srt` file might look like:
```
36
00:03:06,579 --> 00:03:09,284
<i>(woman)</i> He looks great.
That Al Conti is a genius.

37
00:03:10,500 --> 00:03:12,539
I am a genius.

38
00:03:13,586 --> 00:03:15,626
I am a genius!
```
Each dialogue line is numbered, has a beginning and an ending time (to the nearest millisecond) and has the text (possibly formatted).
To use this script, fine an easily-identifiable line near the beginning (e.g. "I am a genius") with the corresponding number (37), and then find the time in the actual video where it occurs (for me this is `00:03:10,500`).
Do the same for a line at the end.
The call signature is then:
``` bash
python subs.py [-h] [--input_filename INPUT_FILENAME] [--output_filename OUTPUT_FILENAME] [--ni NI] [--nf NF] [--ti TI] [--tf TF]
```
As an example:
``` bash
python python subs.py --input_filename off_subtitles.srt --output_filename fixed_subtitles.srt --ni 37 --ti 00:03:10,500 --nf 1349 --tf 01:37:57,250
```
