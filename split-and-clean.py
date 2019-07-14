#!/usr/bin/env python3
#
# Copyright (c) 2019 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

import argparse
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from colorama import init, Fore, Back, Style
init( autoreset=True )

from vidz.convert import cConvert
from vidz.scene import cScene, cInterval
from vidz.source import cSource

#---

parser = argparse.ArgumentParser( description='Clean and convert .ts to .avi.' )
parser.add_argument( 'entries', metavar='Entries', nargs='*', help='One (or multiple) entry(ies) in the xml' )
args = parser.parse_args()

if not args.entries:
	print( Back.RED + 'At least 1 entry is required' )
	sys.exit()

#---

tree = ET.parse( 'data.xml' )
root = tree.getroot()

ffmpeg = Path( root.get( 'ffmpeg' ) )
if not ffmpeg.exists():
	print( Back.RED + f'ffmpeg binary path doesn\'t exist: {ffmpeg}' )
	sys.exit()

output = Path( root.get( 'output' ) )
if not output.exists():
	print( Back.RED + f'output path doesn\'t exist: {output}' )
	sys.exit()

#---

for entry in args.entries:
    xml_source = root.find( f'./source[@index="{entry}"]' )
    if xml_source is None:
        continue
    
    index = xml_source.get( 'index' )
    source = cSource()
    if not source.Build( index ):
        print( Back.RED + f'can\'t build source from index: {index}' )
        sys.exit()

    print( Fore.CYAN + f'source: {source.Index()}' )

    for xml_scene in xml_source.findall( 'scene' ):
        scene = cScene( source )
        scene.Name( xml_scene.get( 'name' ) )
        scene.QScale( xml_scene.get( 'qscale' ) )

        print( Fore.CYAN + f'scene: {scene.Name()}' )

        for xml_interval in xml_scene.findall( 'interval' ):
            interval = cInterval()
            interval.SS( xml_interval.get( 'ss' ) )
            interval.To( xml_interval.get( 'to' ) )
            interval.VMap( xml_interval.get( 'vmap' ) )
            interval.AMap( xml_interval.get( 'amap' ) )
            scene.AddInterval( interval )
        
        scene.BuildOutput( output )
        
        convert = cConvert( ffmpeg, source, scene )
        convert.RunClean()
        convert.RunAvi()
        