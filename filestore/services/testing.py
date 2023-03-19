import time
import subprocess

YEAH = ''


def upload(stream):
    """Upload a file, returns location on disk"""
    directory = 'downloads'
    process = subprocess.Popen(
        ['python',
            './filestore/asydown/asydown.py',
            '--streams=1',
            f'--destdir={directory}',
            stream],
        stdout=subprocess.PIPE
    )
    YEAH = None
    for line in process.stdout:
        print(line.decode().strip())
        if YEAH is None:
            YEAH = str(line.decode())
    # python ./filestore/asydown/asydown.py --streams=1 --destdir='downloads'
    #  'https://w.wallhaven.cc/full/5w/wallhaven-5wg9j9.jpg'

    # Decode the output from bytes to string
    # output_str = output.decode('utf-8')

    # Print the output
    # print(output.)
    return YEAH


inc = upload('https://w.wallhaven.cc/full/ey/wallhaven-eyvzwo.jpg')

time.sleep(0.5)
print('you need this: ', inc)
if inc is None:
    print('failure')