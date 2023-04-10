#!/usr/bin/env python
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
import math
from pathlib import Path
import platform
import sys

from colorama import init, Fore, Back, Style
init( autoreset=True )

from vidz.convert import cConvert
from vidz.scene import cScene

#---

parser = argparse.ArgumentParser( description='Convert video to xvid.avi.' )
parser.add_argument( 'directory', metavar='Directory', nargs=1, help='The directory to convert videos' )
args = parser.parse_args()

#---

directory = Path( args.directory[0] ).resolve()
if not directory.exists():
	print( Back.RED + f'directory doesn\'t exist: {directory}' )
	sys.exit()

ffmpeg = Path( './ffmpeg-6.0-essentials_build-win64/bin/ffmpeg.exe' )
if not ffmpeg.exists():
	print( Back.RED + f'ffmpeg binary path doesn\'t exist: {ffmpeg}' )
	sys.exit()

#---

print( Fore.CYAN + f'source: {directory}' )

def sizeof_fmt( iSize, iSuffix='o' ):
    magnitude = int( math.floor( math.log( iSize, 1024 ) ) )
    val = iSize / math.pow( 1024, magnitude )
    if magnitude > 7:
        return '{:.1f}{}{}'.format( val, 'Y', iSuffix )
    return '{:3.1f} {}{}'.format( val, ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'][magnitude], iSuffix )

class cSceneSingle( cScene ):
    def Build( self, iPathFile ):
        self.mOutputClean = iPathFile
        self.mOutputAvi = iPathFile.with_suffix( '.avi' )

#---

results = []

for element in directory.rglob( '*' ):
    if not element.is_file():
        continue

    #                            Images                                                Data                                 DVD
    if element.suffix.lower() in [ '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.thm' ] + [ '.pdf', '.zip', '.pps', '.ini' ] + [ '.ifo', '.dat', '.bup', '.vob' ]:
        continue

    if element.suffix.lower() in [ '.avi' ]: #TODO: check XVID tag
        continue

    if element.suffix.lower() in [ '.mp4', '.mpeg4', '.mpg', '.3gp', '.mov', '.wmv', '.vro' ]:
        results.append( { 'pathfile': element, 'size': element.stat().st_size } )
        continue

    print( Fore.YELLOW + f'It\'s not an image/video/data: {element} [{sizeof_fmt(element.stat().st_size)}]' )

results = sorted( results, key=lambda iElement: iElement['size'], reverse=True )

#---

for result in results:
    pathfile = result['pathfile']
    size = result['size']
    print( f'Process: {pathfile} [{sizeof_fmt(size)}]' )

    scene = cSceneSingle( None )
    scene.QScale( 5 )
    scene.Build( pathfile )

    if scene.OutputAvi().exists():
        print( Fore.YELLOW + f'Convertion already exists: {pathfile} [{sizeof_fmt(pathfile.stat().st_size)}]' )
        continue

    convert = cConvert( ffmpeg, None, scene )
    # convert.RunConvert()

    # convert ~50Go mp4 to certainly + ~250Go avi -_-

#---

print()
full_size = sum( [ result['size'] for result in results ] )
print( f'size: {sizeof_fmt(full_size)}' )