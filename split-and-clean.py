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
from vidz.concat import cConcat
from vidz.scene import cScene, cInterval
from vidz.source import cSource

#---

parser = argparse.ArgumentParser( description='Clean and convert .ts to .avi.' )
parser.add_argument( '-i', '--input',                       nargs='+', default=[],  help='One (or multiple) entry(ies) id in the xml' )
parser.add_argument( '-t', '-d', '--test-sound', type=int,  nargs='?', const=10,    help='Test sound on small interval' )
parser.add_argument( '-c', '--concat',                      nargs='+', default=[],  help='Concatenate following entry(ies) ("source-id"-"scene-index")' )
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

def BuildSourceScenes( iXMLRoot, iEntry ):
    xml_sources = iXMLRoot.findall( f'./source[@id="{iEntry}"]' )
    if not xml_sources:
        print( Back.RED + f'no source for this id: {iEntry}' )
        return None
    if len( xml_sources ) > 1:
        print( Back.RED + f'multiple sources with same id: {iEntry}' )
        return None

    xml_source = xml_sources[0]

    source = cSource.Create( xml_source )
    if not source.Build():
        print( Back.RED + f'can\'t build source: {iEntry}' )
        sys.exit()

    print( Fore.CYAN + f'source: {source.PathFile()}' )

    scenes = []
    for xml_scene in xml_source.findall( 'scene' ):
        scene = cScene( source )
        scene.Name( xml_scene.get( 'name' ) )
        scene.QScale( xml_scene.get( 'qscale' ) )

        print( Fore.CYAN + f'scene: {scene.Name()}' )

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
    
    return source, scenes

#---

for entry in args.input:
    source, scenes = BuildSourceScenes( root, entry )
    if source is None:
        continue

    for scene in scenes:
        convert = cConvert( ffmpeg, ffprobe, source, scene )
        convert.RunClean()
        convert.RunConvert()

#---

scenes = []
for entry in args.concat:
    scene_index = 0
    tabs = entry.split( '-' )
    if len( tabs ):
        source_id = tabs.pop( 0 )
    if len( tabs ):
        scene_index = int( tabs.pop( 0 ) )

    source, source_scenes = BuildSourceScenes( root, source_id )
    if source is None:
        continue

    if not 0 <= scene_index < len( source_scenes ):
        print( Back.RED + f'wrong scene index: {scene_index}/{len( source_scenes )-1}' )
        sys.exit()
        
    scenes.append( source_scenes[scene_index] )

concat = cConcat( ffmpeg, ffprobe, scenes )
concat.RunConcat()
