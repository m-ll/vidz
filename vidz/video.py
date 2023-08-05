#
# Copyright (c) 2019-23 m-ll. All Rights Reserved.
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# 2b13c8312f53d4b9202b6c8c0f0e790d10044f9a00d8bab3edf3cd287457c979
# 29c355784a3921aa290371da87bce9c1617b8584ca6ac6fb17fb37ba4a07d191
#

## @package video
#  Manage video file

from pathlib import Path

## Manage one video file
class cVideo:

    ## The constructor
    #
    #  @param  iId  int  The id of the video
    def __init__( self, iId, iName, iQScale ):
        self.mId = iId
        self.mName = iName

        self.mQScale = int( iQScale )

        # self.mOutputClean = None
        self.mSegmentList = None
        self.mOutputAvi = None

    ## Get the id
    #
    #  @return  string  The id
    def Id( self ):
        return self.mId

    ## Get the name
    #
    #  @return  string  The name
    def Name( self ):
        return self.mName

    ## Manage the qscale
    #
    #  @return          int  The qscale
    def QScale( self ):
        return self.mQScale

    ## Build all the output pathfiles
    #
    #  @param  iOutputRoot  pathlib.Path  The directory in which all the output files will be created
    def BuildOutput( self, iOutputRoot ):
        output_directory = iOutputRoot / f'tmp-{self.mName}'
        output_directory.mkdir( exist_ok=True )

        self.mSegmentList = output_directory / f'{self.mName}.list.txt'

        self.mOutputAvi = iOutputRoot / f'{self.mName}.avi'

    ## Get pathfile of the list file (a txt file containing 1 line for each subfile)
    #
    #  @return  Path  The list file
    def SegmentList( self ):
        return self.mSegmentList

    ## Get pathfile of the avi (final) file
    #
    #  @return  Path  The avi file
    def OutputAvi( self ):
        return self.mOutputAvi

#---
