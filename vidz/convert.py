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

## @package scene
#  Manage conversion

import subprocess

from colorama import init, deinit, Fore, Back, Style

## The converter
#
#  Convert/export each scene of the source file to its own file
class cConvert:
    
    ## The constructor
    #
    #  @param  iFFmpeg  string   The ffmpeg command pathfile
    #  @param  iSource  cSource  The source file
    #  @param  iScene   cScene   The scene to convert
    def __init__( self, iFFmpeg, iFFprobe, iSource, iScene ):
        self.mFFmpeg = iFFmpeg
        self.mFFprobe = iFFprobe
        self.mSource = iSource
        self.mScene = iScene

    ## Create a 'clean' file (without ads) of the scene
    def RunClean( self ):
        if not self.mScene.Intervals():
            return
        elif len( self.mScene.Intervals() ) == 1:
            self._RunClean1()
        else:
            self._RunCleanN()
            self._RunConcat()

    ## Create a 'clean' file (without ads) of the scene (for 1 interval scene)
    def _RunClean1( self ):
        self._RunCleanInterval( self.mScene.Intervals()[0], self.mScene.OutputClean() )

    ## Create multiple 'clean' files of the scene (for a scene with multiple intervals)
    def _RunCleanN( self ):
        for interval, clean in zip( self.mScene.Intervals(), self.mScene.OutputParts() ):
            self._RunCleanInterval( interval, clean )

    ## Create a 'clean' file for an interval
    #
    #  @param  iInterval  cInterval     The interval to make a clean
    #  @param  iOutput    pathlib.Path  The output 'clean' file of the interval
    def _RunCleanInterval( self, iInterval, iOutput ):
        command = [ self.mFFmpeg, 
                    '-i', self.mSource.PathFile() ]

        if iInterval.VMap() and iInterval.AMap():
            command += [ '-map', iInterval.VMap(), '-map', iInterval.AMap() ]

        command += ['-vcodec', 'copy', '-acodec', 'copy', 
                    '-ss', iInterval.SS(), 
                    '-to', iInterval.To(), 
                    iOutput ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

    ## Concatenate multiple 'clean' files (from multiple intervals) of the scene
    def _RunConcat( self ):
        with open( self.mScene.OutputList(), 'w' ) as outfile:
            outfile.write( "# this is a comment\n" )
            for clean in self.mScene.OutputParts():
                outfile.write( f"file '{clean.name}'\n" )

        command = [ self.mFFmpeg, 
                    '-f', 'concat', 
                    '-safe', '0', 
                    '-i', self.mScene.OutputList(), 
                    '-c', 'copy', 
                    self.mScene.OutputClean() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

    ## Convert a 'clean' file (without ads) of the scene to an AVI-XVID file
    def RunConvert( self ):
        if not self.mScene.OutputClean().exists():
            return
        
        # Make convertion
        command = [ self.mFFmpeg, 
                    '-i', self.mScene.OutputClean(), 
                    '-qscale:v', str( self.mScene.QScale() ), 
                    '-vtag', 'XVID', 
                    self.mScene.OutputAviTmp() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )
        
        # Extract the video only
        command = [ self.mFFmpeg, 
                    '-i', self.mScene.OutputAviTmp(), 
                    '-c:v', 'copy', 
                    '-an', 
                    self.mScene.OutputAviWithoutSound() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )
        
        # Extract the sound only
        command = [ self.mFFmpeg, 
                    '-i', self.mScene.OutputAviTmp(),  
                    '-vn', 
                    '-c:a', 'copy', 
                    self.mScene.OutputMP3() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

        # Get length of video/audio (with ffprobe) to compute the ratio
        command = [ self.mFFprobe, 
                    '-i', self.mScene.OutputAviWithoutSound(), 
                    '-show_entries', 'format=duration', 
                    '-v', 'quiet', 
                    '-of', 'csv=p=0' # or maybe xml
                     ]
        print( f'\tffprobe: {self.mScene.OutputAviWithoutSound()}' )
        r = subprocess.run( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        # r = subprocess.run( command, capture_output=True ) # python 3.7 ...
        video_duration = float( r.stdout )
        print( f'\tduration: {video_duration}' )

        command = [ self.mFFprobe, 
                    '-i', self.mScene.OutputMP3(), 
                    '-show_entries', 'format=duration', 
                    '-v', 'quiet', 
                    '-of', 'csv=p=0' # or maybe xml
                     ]
        print( f'\tffprobe: {self.mScene.OutputMP3()}' )
        r = subprocess.run( command, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        # r = subprocess.run( command, capture_output=True ) # python 3.7 ...
        audio_duration = float( r.stdout )
        print( f'\tduration: {audio_duration}' )

        ratio = audio_duration / video_duration
        print( f'\tratio audio/video: {ratio}' )

        # Stretch the sound to match the video length
        command = [ self.mFFmpeg, 
                    '-i', self.mScene.OutputMP3(), 
                    '-filter:a', f'atempo={ratio}', 
                    self.mScene.OutputMP3Stretched() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

        # Merge video and sound to the final avi
        command = [ self.mFFmpeg, 
                    '-i', self.mScene.OutputAviWithoutSound(), 
                    '-i', self.mScene.OutputMP3Stretched(), 
                    '-c', 'copy', 
                    self.mScene.OutputAvi() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

    #---

    ## Print information before running a command
    #
    #  @param  iCommand  string[]  The command which will be executed
    def _PrintHeader( self, iCommand ):
        deinit()
        init( autoreset=False )
        print( Fore.YELLOW )
        print( *iCommand )
        print( Style.RESET_ALL )

    ## Execute a command
    #
    #  @param  iCommand  string[]  The command which will be executed
    def _Run( self, iCommand ):
        # return 'xxxxxxxxxxxxxxxxxx'
        return subprocess.run( iCommand )

    ## Print information after running a command
    #
    #  @param  iCompletedProcess  subprocess.cCompletedProcess  The result of the command which was executed
    def _PrintFooter( self, iCompletedProcess ):
        print( Fore.YELLOW )
        print( iCompletedProcess )
        print( Style.RESET_ALL )
        deinit()
        init( autoreset=True )
