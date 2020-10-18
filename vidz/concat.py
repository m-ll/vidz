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

## @package scene
#  Manage concatenation

from pathlib import Path
import os
import subprocess
import tempfile

from colorama import init, deinit, Fore, Back, Style

## The concatenater
#
#  Concatenate multiple files
class cConcat:
    
    ## The constructor
    #
    #  @param  iFFmpeg  string   The ffmpeg command pathfile
    #  @param  iSource  cSource  The source file
    #  @param  iScenes  cScene[] The scenes to concat
    def __init__( self, iFFmpeg, iFFprobe, iScenes ):
        self.mFFmpeg = iFFmpeg
        self.mFFprobe = iFFprobe
        self.mScenes = iScenes

        self.mConcatPathFile = None
        self.mConfig = []
        self._Build()

    ## Concatenate multiple 'output' files (from multiple scene)
    def RunConcat( self ):
        if not self.mScenes:
            return
        
        with tempfile.NamedTemporaryFile( 'w', newline='', encoding='utf-8' ) as fp:
            for line in self.mConfig:
                fp.write( line )
            
            fp.seek( 0 )

            command = [ self.mFFmpeg, 
                        '-f', 'concat', 
                        '-safe', '0', 
                        '-i', fp.name, 
                        '-c', 'copy', 
                        self.mConcatPathFile ]

            self._PrintHeader( command )
            cp = self._Run( command )
            self._PrintFooter( cp )

    #---

    ## Build/init all internal stuff
    def _Build( self ):
        if not self.mScenes:
            return
        
        self.mConfig.append( '# This is a comment\n' )
        for scene in self.mScenes:
            self.mConfig.append( f"file '{scene.OutputAvi()}'\n" )
        
        all_stems = []
        for scene in self.mScenes:
            all_stems.append( scene.OutputAvi().stem )
            
        common_prefix = os.path.commonprefix( all_stems )
        
        all_suffixes = []
        for scene in self.mScenes:
            all_suffixes.append( '[' + scene.OutputAvi().stem.replace( common_prefix, '' ) + ']' )
        
        new_name = common_prefix + '+'.join( all_suffixes ) + self.mScenes[0].OutputAvi().suffix

        self.mConcatPathFile = self.mScenes[0].OutputAvi().parent / new_name
        # print( self.mConcatPathFile )

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
