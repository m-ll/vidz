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

from pathlib import Path

class cSource:
    def __init__( self ):
        self.mIndex = -1
        self.mPath = None
        self.mPathFile = None

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

    def Index( self ):
        return self.mIndex
        
    def PathFile( self ):
        return self.mPathFile
        