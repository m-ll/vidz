#!/usr/bin/env python3
#
# Copyright (c) 2020 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

import argparse
import os
from pathlib import Path
import subprocess
import sys

from colorama import init, deinit, Fore, Back, Style
init( autoreset=True )

#---

parser = argparse.ArgumentParser( description='Concat vob files' )
parser.add_argument( '-i', '--input',  required=True, help='Folder where vob files are (or the one which contains VIDEO_TS)' )
parser.add_argument( '-o', '--output', help='Output vob file (default inside vidz)' )
args = parser.parse_args()

#---

source_dir = Path( args.input )
if not source_dir.exists():
    print( Back.RED + f'no source exists: {source_dir}' )
    sys.exit()

if source_dir.name != 'VIDEO_TS':
    source_dir /= 'VIDEO_TS'

if args.output is None:
    dest_dir = Path( '/' ) / 'mnt' / 'f' / 'vidz'
    if not dest_dir.exists():
        print( Back.RED + f'dest dir not exists: {dest_dir}' )
        sys.exit()
    concat_file = dest_dir / ( source_dir.parts[-2] + '-concat' )
    dest_file = dest_dir / source_dir.parts[-2]
    if dest_file.exists():
        print( Back.RED + f'dest exists: {dest_file}' )
        sys.exit()
else:
    dest_file = Path( args.output )
    if dest_file.exists():
        print( Back.RED + f'dest exists: {dest_file}' )
        sys.exit()
    concat_file = dest_file.parent / ( dest_file.stem + '-concat' )

concat_file = concat_file.with_suffix( '.vob' )
dest_file = dest_file.with_suffix( '.vob' )

print( f'source_dir: {source_dir}' )
print( f'concat_file : {concat_file}' )
print( f'dest_file : {dest_file}' )
print( '' )

#---

files = [ f for f in source_dir.glob( '*' ) if f.stat().st_size > 10**9 ]

def GetFiles( iFirstPathFile ):
    file_parts = iFirstPathFile.stem.split( '_' )
    files = []
    current_file = iFirstPathFile.parent / ( '_'.join( file_parts ) + '.VOB' )
    while current_file.exists():
        files.append( current_file )

        file_parts[-1] = str( int(file_parts[-1]) + 1 )
        current_file = iFirstPathFile.parent / ( '_'.join( file_parts ) + '.VOB' )
    
    return files

files = GetFiles( files[0] )

print( 'Files to be concat:')
for f in files:
    print( f'{f}: {f.stat().st_size}' )

#---

command = [ 'cat' ]
command += files

deinit()
init( autoreset=False )
print( Fore.YELLOW )
print( *command )
print( Style.RESET_ALL )

if not concat_file.exists():
    with concat_file.open( 'w' ) as fd:
        # completed_process = 'xxxxxxxxxxxxxxxxxx'
        completed_process = subprocess.run( command, stdout=fd )

print( Fore.YELLOW )
print( completed_process )
print( Style.RESET_ALL )
deinit()
init( autoreset=True )

#---

ffmpeg = Path.home() / 'work' / 'vidz' / 'ffmpeg-4.3.1-amd64-static' / 'ffmpeg'
command = [ ffmpeg, 
            '-probesize', '100M', 
            '-analyzeduration', str( 10 * 60 * 10**6 ), 
            '-i', concat_file, 
            '-map', '0:v', 
            '-map', '0:a:1', 
            '-map', '0:a:0', 
            '-map', '0:a:2?', 
            '-map', '0:a:3?', 
            '-map', '0:a:4?', 
            '-map', '0:a:5?', 
            '-map', '0:s', 
            '-map', '-0:0', 
            '-c', 'copy', 
            dest_file ]

deinit()
init( autoreset=False )
print( Fore.YELLOW )
print( *command )
print( Style.RESET_ALL )

# completed_process = 'xxxxxxxxxxxxxxxxxx'
completed_process = subprocess.run( command )

print( Fore.YELLOW )
print( completed_process )
print( Style.RESET_ALL )
deinit()
init( autoreset=True )
