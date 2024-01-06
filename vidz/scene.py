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
#  Manage scene

## Manage scene
#
#  A scene is one (or more) sequence(s) inside the source file
#  For example: if there are multiple episodes inside the source file,
#  each episode is (may be) a scene
class cScene:

    ## The constructor
    #
    #  @param  iVideo  cVideo  The video file
    def __init__( self, iVideo ):
        self.mVideo = iVideo

        self.mSource = None
        self.mIntervals = []

        # self.mOutputClean = None
        self.mSegments = []
        self.mOutputAvi = None

    ## Manage the source
    #
    #  @param  iSource  cSource  Set the source (if not None)
    #  @return          cSource  The previous/current source
    def Source( self, iSource=None ):
        if iSource is None:
            return self.mSource

        previous_value = self.mSource
        self.mSource = iSource
        return previous_value

    ## Get all the intervals
    #
    #  @return  int The intervals
    def Intervals( self ):
        return self.mIntervals

    ## Add a new interval
    #
    #  @param  iInterval  cInterval  The new interval
    def AddInterval( self, iInterval ):
        self.mIntervals.append( iInterval )

    #---

    ## Build all the output pathfiles
    #
    #  @param  iOutputRoot  pathlib.Path  The directory in which all the output files will be created
    def BuildOutput( self, iOutputRoot ):
        output_directory = iOutputRoot / f'tmp-{self.mVideo.Name()}'
        output_directory.mkdir( exist_ok=True )

        # self.mOutputClean = output_directory / f'{self.mVideo.Name()}.clean.ts'

        for i, interval in enumerate( self.mIntervals ):
            self.mSegments.append( output_directory / f'{self.mSource.Id()}-{self.mVideo.Name()}.{i+1}{self.mSource.PathFile().suffix}' )

    ## Get pathfile of the clean file (without ads)
    #
    #  @return  Path  The clean file
    # def OutputClean( self ):
    #     return self.mOutputClean

    ## Get pathfiles of all subfiles (1 for each interval)
    #
    #  @return  Path[]  The subfiles
    def Segments( self ):
        return self.mSegments

#---

## Manage interval
#
#  An interval if a part of a scene
#  It is useful for removing ads
class cInterval:

    ## The constructor
    def __init__( self ):
        self.mSS = None
        self.mTo = None
        self.mVMap = None
        self.mAMap = None

    ## Manage the start of the interval
    #
    #  @param  iSS  int  Set the start (if not None)
    #  @return      int  The previous/current start
    def SS( self, iSS=None ):
        if iSS is None:
            return self.mSS

        previous_value = self.mSS
        self.mSS = iSS
        return previous_value

    ## Manage the stop of the interval
    #
    #  @param  iTo  int  Set the stop (if not None)
    #  @return      int  The previous/current stop
    def To( self, iTo=None ):
        if iTo is None:
            return self.mTo

        previous_value = self.mTo
        self.mTo = iTo
        return previous_value

    ## Manage the video stream map
    #
    #  @param  iVMap  string  Set the map (if not None)
    #  @return        string  The previous/current map
    def VMap( self, iVMap=None ):
        if iVMap is None:
            return self.mVMap

        previous_value = self.mVMap
        self.mVMap = iVMap
        return previous_value

    ## Manage the audio stream map
    #
    #  It is used to select another sound track
    #  when the main one is not the french
    #  For example: '0:1' is to use the second audio stream
    #
    #  @param  iVMap  string  Set the map (if not None)
    #  @return        string  The previous/current map
    def AMap( self, iAMap=None ):
        if iAMap is None:
            return self.mAMap

        previous_value = self.mAMap
        self.mAMap = iAMap
        return previous_value
