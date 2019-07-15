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

## @package source
#  Manage source file

from pathlib import Path

## Manage source file
#
#  It can only manage a harddisk on drive f: and g:
#  and the structure inside must be like dvd (f:/LGDVR/000000XXREC/*.TS)
class cSource:

    ## The constructor
    def __init__( self ):
        self.mIndex = -1
        self.mPath = None
        self.mPathFile = None

    ## Build the path from the index
    #
    #  @param  iIndex  int   The index of the file to retrive
    #  @return         bool  The file (corresponding to the index) has been build and found
    def Build( self, iIndex ):
        self.mPath = Path( f'f:/LGDVR/000000{iIndex}REC' )
        source_pathfile = list( self.mPath.glob( '*.TS' ) )
        if source_pathfile:
            self.mIndex = iIndex
            self.mPathFile = Path( source_pathfile[0] )
            return True

        self.mPath = Path( f'g:/LGDVR/000000{iIndex}REC' )
        source_pathfile = list( self.mPath.glob( '*.TS' ) )
        if source_pathfile:
            self.mIndex = iIndex
            self.mPathFile = Path( source_pathfile[0] )
            return True

        return False

    ## Get the index
    #
    #  @return  int  The index
    def Index( self ):
        return self.mIndex
        
    ## Get the pathfile corresponding to the index
    #
    #  @return  pathlib.Path  The source pathfile
    def PathFile( self ):
        return self.mPathFile
        