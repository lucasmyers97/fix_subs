import argparse
import re
from datetime import datetime

def get_commandline_args():

    desc = "Realigns subtitles in .srt format"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--input_filename', help='.srt file with misaligned subtitles')
    parser.add_argument('--output_filename', help='.srt file with newly aligned subtitles')
    parser.add_argument('--ni', help='beginning subtitle line to match')
    parser.add_argument('--ti', help='actual time of beginning subtitle: HH:MM:SS,fff')
    parser.add_argument('--nf', help='final subtitle line to match')
    parser.add_argument('--tf', help='actual time of final subtitle: HH:MM:SS,fff')

    args = parser.parse_args()

    return (args.input_filename, args.output_filename, 
            args.ni, args.nf, args.ti, args.tf)



def get_original_time(n, text):

    pattern = r'^{}\n(\d{{2}}:\d{{2}}:\d{{2}},\d{{3}}) --> \d{{2}}:\d{{2}}:\d{{2}},\d{{3}}$'.format(n)
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1)



def main():

    (input_filename, output_filename, 
     ni, nf, ti_fixed, tf_fixed) = get_commandline_args()

    with open(input_filename) as f:
        text = f.read()
    
    ti = get_original_time(ni, text)
    tf = get_original_time(nf, text)
    
    time_pattern = '%H:%M:%S,%f'
    pattern = r'\d\d:\d\d:\d\d,\d\d\d'
    
    # have to use timedeltas to do the math
    t0 = datetime.strptime('00:00:00,000', time_pattern)
    t1 = datetime.strptime(ti, time_pattern) - t0
    t2 = datetime.strptime(tf, time_pattern) - t0
    s1 = datetime.strptime(ti_fixed, time_pattern) - t0
    s2 = datetime.strptime(tf_fixed, time_pattern) - t0
    
    m = (s1 - s2)/(t1 - t2)
    b = s1 - t1 * m
    
    def fix_time(t):
        t = datetime.strptime(t, time_pattern) - t0
        fixed_t = m * t + b
        return datetime.strftime(fixed_t + t0, time_pattern)[:-3]
    
    substitution = lambda p: fix_time(p.group(0))
    
    
    new_text = re.sub(pattern, substitution, text)
    
    with open(output_filename, 'w') as f:
        f.write(new_text)



if __name__ == '__main__':
    main()
