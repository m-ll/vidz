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
import xml.etree.ElementTree as ET

from colorama import init, deinit, Fore, Back, Style
init( autoreset=True )

#---

parser = argparse.ArgumentParser( description='Concat vob files' )
parser.add_argument( '-i', '--input', nargs='+', default=[],  help='One (or multiple) entry(ies) id in the xml' )
parser.add_argument( '-d', action='store_true', help='Test a segment to check sound streams (to find french one)' )
args = parser.parse_args()

#---

data = Path( './data-vob.xml' )
if not data.exists():
    print( Back.RED + f'data-vob.xml file doesn\'t exist: {data}' )
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

## Manage one source dvd
class cSource:
    ## The constructor
    #
    #  @param  iId  int  The id of the source
    def __init__( self, iId ):
        self.mId = iId
        self.mPath = None
        self.mName = '' # Folder name starting with the id

    def __str__(self):
        strings = []
        strings.append( f'[cSource] self.mId: {self.mId}' )
        strings.append( f'[cSource] self.mPath: {self.mPath}' )
        strings.append( f'[cSource] self.mName: {self.mName}' )

        return "\n".join( strings )

    def GetId( self ):
        return self.mId

    def GetPath( self ):
        return self.mPath

    ## Build source
    def Build( self ):
        path = Path( f'/mnt/g/' )
        paths = [ p for p in path.rglob( '*' ) if p.is_dir() and p.name.startswith( self.mId + '.' ) ]
        if len( paths) != 1:
            return

        path = paths[0] / 'VIDEO_TS'
        if not path.exists():
            return

        self.mName = path.parts[-2]
        self.mPath = path

## Manage consecutive files
class cConsecutiveFiles:
    ## The constructor
    #
    #  @param  iSource  cSource  The source of the video
    def __init__( self ):
        self.mFiles = []
    
    def GetFiles( self ):
        return self.mFiles

    ## Build all the files from the first one
    #
    #  @param  iFirstPathFile   pathlib.Path    The path of the first vob part
    def Build( self, iFirstPathFile ):
        file_parts = iFirstPathFile.stem.split( '_' )
        self.mFiles = []
        current_file = iFirstPathFile.parent / ( '_'.join( file_parts ) + '.VOB' )
        while current_file.exists():
            self.mFiles.append( current_file )

            file_parts[-1] = str( int(file_parts[-1]) + 1 )
            current_file = iFirstPathFile.parent / ( '_'.join( file_parts ) + '.VOB' )

## Manage one video file
class cVideo:
    ## The constructor
    #
    #  @param  iSource  cSource  The source of the video
    def __init__( self, iSource, iName, iQScale ):
        self.mSource = iSource
        self.mName = iName
        self.mQScale = int(iQScale)
        self.mFiles = []

        self.mOutputConcat = None
        self.mOutputAvi = None

    def __str__(self):
        strings = []
        strings.append( f'[cVideo] self.mName: {self.mName}' )
        strings.append( f'[cVideo] self.mQScale: {self.mQScale}' )
        strings.append( f'[cVideo] self.mOutputConcat: {self.mOutputConcat}' )
        strings.append( f'[cVideo] self.mOutputAvi: {self.mOutputAvi}' )

        strings.append( f'[cVideo] self.mFiles:' )
        for consecutive_file in self.mFiles:
            for single_file in consecutive_file.GetFiles():
                strings.append( f"[cVideo] \t{single_file}" )

        return "\n".join( strings )

    def GetSource( self ):
        return self.mSource

    def GetQScale( self ):
        return self.mQScale

    def GetFiles( self ):
        return self.mFiles

    def GetAllFiles( self ):
        all_files = []
        for consecutive_file in self.mFiles:
            all_files += consecutive_file.GetFiles()

        return all_files

    def AddFiles( self, iVTS, iPosition ):
        first_file = self.mSource.GetPath() / f'VTS_{iVTS:02}_{iPosition}.VOB'
        if not first_file.exists():
            return

        consecutive_files = cConsecutiveFiles()
        consecutive_files.Build( first_file )

        self.mFiles.append( consecutive_files )

    #---

    def BuildOutput( self, iOutputRoot ):
        self.mOutputConcat = iOutputRoot / ( self.mName + '.concat.vob' )
        self.mOutputAvi = iOutputRoot / ( self.mName + '.avi' )

    def GetOutputConcat( self ):
        return self.mOutputConcat
    def GetOutputAvi( self ):
        return self.mOutputAvi

#---

## Concat vob files from the first one
class cConcat:
    ## The constructor
    def __init__( self, iVideo ):
        self.mVideo = iVideo
    
    ## Concat all the files
    def Concat( self ):
        if self.mVideo.GetOutputConcat().exists():
            return

        all_files = self.mVideo.GetAllFiles()
        if not all_files:
            return

        command = [ 'cat' ]
        command += all_files

        with self.mVideo.GetOutputConcat().open( 'w' ) as fd:
            deinit()
            init( autoreset=False )
            print( Fore.YELLOW )
            print( *command )
            print( Style.RESET_ALL )

            # completed_process = 'xxxxxxxxxxxxxxxxxx'
            completed_process = subprocess.run( command, stdout=fd )

            print( Fore.YELLOW )
            print( completed_process )
            print( Style.RESET_ALL )
            deinit()
            init( autoreset=True )

#---

## Convert vob file to avi
class cConvert:
    ## The constructor
    def __init__( self, iVideo, iFFmpeg ):
        self.mVideo = iVideo
        self.mFFmpeg = iFFmpeg

        self.mDebugStart = []
        self.mDebugStop = []
        self.mAudioStreams = [ '-map', '0:a' ]
        self.mUnknownStreams = []

    ## Build data
    def Build( self, iFirstAudio, iUnknownStreams, iDebug ):
        if iFirstAudio is not None:
            self.mAudioStreams = [ '-map', f'0:a:{iFirstAudio}' ]
            for i in range( 6 ):
                if i < iFirstAudio:
                    self.mAudioStreams += [ '-map', f'0:a:{i}' ]
                elif i > iFirstAudio:
                    self.mAudioStreams += [ '-map', f'0:a:{i}?' ]

        for unknown_stream in iUnknownStreams:
            self.mUnknownStreams = [ '-map', f'-0:{unknown_stream}']

        if iDebug:
            self.mDebugStart = [ '-ss', '00:10:00.000' ]
            self.mDebugStop = [ '-to', '00:15:00.000' ]

    def Convert( self ):
        command = [ self.mFFmpeg, 
                    '-probesize', '100M', 
                    '-analyzeduration', str( 10 * 60 * 10**6 ), 
                    '-i', self.mVideo.GetOutputConcat(), 
                    *self.mDebugStart, 
                    *self.mDebugStop, 
                    '-map', '0:v', 
                    *self.mAudioStreams, 
                    # '-map', '0:s', 
                    *self.mUnknownStreams, 
                    '-vf', 'yadif', # https://ffmpeg.org/ffmpeg-filters.html#yadif-1
                    '-qscale:v', str( self.mVideo.GetQScale() ), '-vtag', 'XVID', 
                    '-c:a', 'copy', 
                    self.mVideo.GetOutputAvi() ]

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

#---

# https://www.internalpointers.com/post/convert-vob-files-mkv-ffmpeg

for entry in args.input:
    xml_sources = root.findall( f'./source[@id="{entry}"]' )
    if not xml_sources:
        print( Back.RED + f'no source for this id: {entry}' )
        break
    if len( xml_sources ) > 1:
        print( Back.RED + f'multiple sources with same id: {entry}' )
        break

    xml_source = xml_sources[0]
    source = cSource( xml_source.get( 'id' ) )
    # source.Build()

    print( source )

    for xml_video in xml_source.findall( 'video' ):
        video = cVideo( source, xml_video.get( 'name' ), xml_video.get( 'qscale' ) )
        video.BuildOutput( output )

        # for xml_file in xml_video.findall( 'file' ):
        #     video.AddFiles( int(xml_file.get( 'vts' )), int(xml_file.get( 'position' )) )

        print( video )

        # concat = cConcat( video )
        # concat.Concat()

        #---

        first_audio = int( xml_video.get( 'first-audio' ) ) if xml_video.get( 'first-audio' ) is not None else None
        unknown_streams = map( int, xml_video.get( 'unknown-streams' ).split( ',' ) ) if xml_video.get( 'unknown-streams' ) is not None else []

        convert = cConvert( video, ffmpeg )
        convert.Build( first_audio, unknown_streams, args.d )
        convert.Convert()
