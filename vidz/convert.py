#
# Copyright (c) 2019-23 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

## @package scene
#  Manage conversion

import json
import subprocess

from colorama import init, deinit, Fore, Back, Style

## The converter
#
#  Convert/export each scene of the source file to its own file
class cConvert:

    ## The constructor
    #
    #  @param  iFFmpeg  string   The ffmpeg command pathfile
    #  @param  iVideo   cVideo   The video file
    #  @param  iScenes  cScene[] The scenes to convert
    def __init__( self, iFFmpeg, iFFprobe, iVideo, iScenes ):
        self.mFFmpeg = iFFmpeg
        self.mVideo = iVideo
        self.mScenes = iScenes

    #---

    ## Create a 'clean' file (without ads) of the scene
    def RunClean( self ):
        if len( self.mScenes ) == 1 and len( self.mScenes[0].Intervals() ) == 1:
            return

        for scene in self.mScenes:
            for interval, segment in zip( scene.Intervals(), scene.Segments() ):
                self._RunCleanInterval( scene, interval, segment )

    def _GetAMapParameters( self, iInterval ):
        # All audio streams
        if iInterval.AMap() is None:
            return [ '-map', '0:a' ]

        # Legacy: only 1 audio stream
        if iInterval.AMap().startswith( '0:' ):
            return [ '-map', iInterval.AMap() ]

        indexes = iInterval.AMap().split( ',' )
        maps = []
        for index in indexes:
            maps.append( '-map' )
            maps.append( '0:a:' + index )
        return maps

    def _GetVMapParameters( self, iInterval ):
        # All video streams
        if iInterval.VMap() is None:
            return [ '-map', '0:v' ]

        # Legacy: only 1 video stream
        return [ '-map', iInterval.VMap() ]

    ## Create a 'clean' file for an interval
    #
    #  @param  iInterval  cInterval     The interval to make a clean
    #  @param  iOutput    pathlib.Path  The output 'clean' file of the interval
    def _RunCleanInterval( self, iScene, iInterval, iOutput ):
        command = [ self.mFFmpeg,
                    '-i', iScene.Source().PathFile(),
                        #TODO: add options to get subtitle streams, but do it for each command
                        # '-probesize', '100M',
                        # '-analyzeduration', str( 10 * 60 * 10**6 ),
                    *self._GetVMapParameters( iInterval ),
                    *self._GetAMapParameters( iInterval ),
                    '-c', 'copy',
                    '-ss', iInterval.SS(),
                    '-to', iInterval.To(),
                    iOutput ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

    #---

    ## Convert a 'clean' file (without ads) of the scene to an AVI-XVID file
    def RunConvert( self ):
        if len( self.mScenes ) == 1 and len( self.mScenes[0].Intervals() ) == 1:
            scene = self.mScenes[0]
            interval = self.mScenes[0].Intervals()[0]

            # Make convertion
            command = [ self.mFFmpeg,
                        '-i', scene.Source().PathFile(),
                        *self._GetVMapParameters( interval ),
                        *self._GetAMapParameters( interval ),
                        '-ss', interval.SS(),
                        '-to', interval.To(),
                        '-qscale:v', str( self.mVideo.QScale() ),
                        '-acodec', 'mp3',
                        '-vtag', 'XVID',
                        self.mVideo.OutputAvi() ]

            self._PrintHeader( command )
            cp = self._Run( command )
            self._PrintFooter( cp )
        else:
            with open( self.mVideo.SegmentList(), 'w' ) as outfile:
                outfile.write( "# this is a comment\n" )
                for scene in self.mScenes:
                    for segment in scene.Segments():
                        outfile.write( f"file '{segment.name}'\n" )

            # Make concat & convertion
            command = [ self.mFFmpeg,
                        '-f', 'concat',
                        '-safe', '0',
                        '-i', self.mVideo.SegmentList(),
                        '-map', '0',
                        '-qscale:v', str( self.mVideo.QScale() ),
                        '-acodec', 'mp3',
                        '-vtag', 'XVID',
                        '-fflags', '+genpts', '-async', '1',
                        self.mVideo.OutputAvi() ]

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
