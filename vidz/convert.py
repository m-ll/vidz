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

import subprocess

from colorama import init, deinit, Fore, Back, Style

class cConvert:
    def __init__( self, iFFmpeg, iSource, iScene ):
        self.mFFmpeg = iFFmpeg
        self.mSource = iSource
        self.mScene = iScene

    def RunClean( self ):
        if not self.mScene.Intervals():
            return
        elif len( self.mScene.Intervals() ) == 1:
            self._RunClean1()
        else:
            self._RunCleanN()
            self._RunConcat()

    def _RunClean1( self ):
        command = [ self.mFFmpeg, 
                    '-i', self.mSource.PathFile() ]

        interval = self.mScene.Intervals()[0]
        if interval.VMap() and interval.AMap():
            command += [ 'map', interval.VMap(), 'map', interval.AMap() ]

        command += ['-vcodec', 'copy', '-acodec', 'copy', 
                    '-ss', interval.SS(), 
                    '-to', interval.To(), 
                    self.mScene.OutputClean() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

    def _RunCleanN( self ):
        for interval, clean in zip( self.mScene.Intervals(), self.mScene.OutputParts() ):
            command = [ self.mFFmpeg, 
                        '-i', self.mSource.PathFile() ]

            if interval.VMap() and interval.AMap():
                command += [ 'map', interval.VMap(), 'map', interval.AMap() ]

            command += ['-vcodec', 'copy', '-acodec', 'copy', 
                        '-ss', interval.SS(), 
                        '-to', interval.To(), 
                        clean ]

            self._PrintHeader( command )
            cp = self._Run( command )
            self._PrintFooter( cp )

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

    def RunAvi( self ):
        if not self.mScene.OutputClean().exists():
            return
        
        command = [ self.mFFmpeg, 
                    '-i', self.mScene.OutputClean(), 
                    '-qscale:v', self.mScene.QScale(), 
                    '-vtag', 'XVID', 
                    self.mScene.OutputAvi() ]

        self._PrintHeader( command )
        cp = self._Run( command )
        self._PrintFooter( cp )

    #---

    def _PrintHeader( self, iCommand ):
        deinit()
        init( autoreset=False )
        print( Fore.YELLOW )
        print( *iCommand )
        print( Style.RESET_ALL )

    def _Run( self, iCommand ):
        # return 'xxxxxxxxxxxxxxxxxx'
        return subprocess.run( iCommand )

    def _PrintFooter( self, iCompletedProcess ):
        print( Fore.YELLOW )
        print( iCompletedProcess )
        print( Style.RESET_ALL )
        deinit()
        init( autoreset=True )
