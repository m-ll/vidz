#!/usr/bin/env python
#
# Copyright (c) 2019-23 m-ll. All Rights Reserved.
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
from vidz.video import cVideo

#---

parser = argparse.ArgumentParser( description='Clean and convert .ts to .avi.' )
parser.add_argument( '-i', '--input',                       nargs='+', default=[],  help='One (or multiple) entry(ies) id in the xml' )
parser.add_argument( '-t', '-d', '--test-sound', type=int,  nargs='?', const=10,    help='Test sound on small interval' )
args = parser.parse_args()

#---

data = Path( './data.xml' )
if not data.exists():
    print( Back.RED + f'data.xml file doesn\'t exist: {data}' )
    sys.exit()

tree = ET.parse( data )
root = tree.getroot()

ffmpeg = Path( root.get( 'ffmpeg' ) )
if not ffmpeg.exists():
    print( Back.RED + f'ffmpeg binary path doesn\'t exist: {ffmpeg}' )
    sys.exit()

ffprobe = Path( root.get( 'ffprobe' ) )
if not ffprobe.exists():
    print( Back.RED + f'ffprobe binary path doesn\'t exist: {ffprobe}' )
    sys.exit()

output = Path( root.get( 'output' ) )
if not output.exists():
    print( Back.RED + f'output path doesn\'t exist: {output}' )
    sys.exit()

#---

def BuildVideo( iXMLRoot, iEntry ):
    xml_videos = iXMLRoot.findall( f'./video[@id="{iEntry}"]' )
    if not xml_videos:
        print( Back.RED + f'no video for this id: {iEntry}' )
        return None
    if len( xml_videos ) > 1:
        print( Back.RED + f'multiple videos with same id: {iEntry}' )
        return None
    
    xml_video = xml_videos[0]

    video = cVideo( xml_video.get( 'id' ), xml_video.get( 'name' ), xml_video.get( 'qscale' ) )
    video.BuildOutput( output )

    print( Fore.CYAN + f'video: {video.Name()}' )

    scenes = []
    for xml_scene in xml_video.findall( 'scene' ):
        scene = cScene( video )

        source = cSource.Create( xml_scene )
        if not source.Build():
            print( Back.RED + f'can\'t build source: {iEntry}' )
            return None

        scene.Source( source )

        print( Fore.CYAN + f'scene: {scene.Source().PathFile()}' )

        for xml_interval in xml_scene.findall( 'interval' ):
            interval = cInterval()
            interval.SS( xml_interval.get( 'ss' ) )
            interval.To( xml_interval.get( 'to' ) )
            if args.test_sound is not None:
                tc_ss = interval.SS().split( ':' )
                tc_to = interval.SS().split( ':' ) # with tc_to = tc_ss, they will share the same data
                new_start = int( tc_ss[1] ) + args.test_sound
                if( new_start > 59 ):
                    new_start = 58
                tc_ss[1] = f'{ new_start }'
                tc_to[1] = f'{ new_start + 1 }' # add 1 min
                interval.SS( ':'.join( tc_ss ) )
                interval.To( ':'.join( tc_to ) )
            interval.VMap( xml_interval.get( 'vmap' ) )
            interval.AMap( xml_interval.get( 'amap' ) )
            scene.AddInterval( interval )
            
            if args.test_sound is not None:
                break
        
        scene.BuildOutput( output )
        scenes.append( scene )

    return video, scenes

for entry in args.input:
    video, scenes = BuildVideo( root, entry )
    if video is None:
        continue

    convert = cConvert( ffmpeg, ffprobe, video, scenes )
    convert.RunClean()
    convert.RunConvert()
