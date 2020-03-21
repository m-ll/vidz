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
#  Manage scene

## Manage scene
#
#  A scene is one (or more) sequence(s) inside the source file
#  For example: if there are multiple episodes inside the source file,
#  each episode is (may be) a scene
class cScene:
    
    ## The constructor
    #
    #  @param  iSource  cSource  The source file
    def __init__( self, iSource ):
        self.mSource = iSource
        
        self.mName = ''
        self.mQScale = -1
        self.mIntervals = []
        
        self.mOutputDirectory = None
        self.mOutputClean = None
        self.mOutputList = None
        self.mOutputParts = []
        self.mOutputAvi = None

    ## Manage the name of the scene
    #
    #  @param  iName  string  Set the name of the scene (if not None)
    #  @return        string  The previous/current name of the scene
    def Name( self, iName=None ):
        if iName is None:
            return self.mName
        
        previous_value = self.mName
        self.mName = iName
        return previous_value
    
    ## Manage the qscale
    #
    #  @param  iQScale  int  Set the qscale (if not None)
    #  @return          int  The previous/current qscale
    def QScale( self, iQScale=None ):
        if iQScale is None:
            return self.mQScale
        
        previous_value = self.mQScale
        self.mQScale = int( iQScale )
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
        self.mOutputDirectory = iOutputRoot / f'tmp-{self.mSource.Id()}-{self.mName}'
        self.mOutputDirectory.mkdir( exist_ok=True )
        self.mOutputAvi = iOutputRoot / f'{self.mName}.avi'

        self.mOutputClean = self.mOutputDirectory / f'{self.mName}.clean.ts'
        self.mOutputList = self.mOutputDirectory / f'{self.mName}.list.txt'
        
        for i, interval in enumerate( self.mIntervals ):
            self.mOutputParts.append( self.mOutputDirectory / f'{self.mName}.{i+1}.ts' )

    ## Get pathfile of the clean file (without ads)
    #
    #  @return  Path  The clean file
    def OutputClean( self ):
        return self.mOutputClean
        
    ## Get pathfiles of all subfiles (1 for each interval)
    #
    #  @return  Path[]  The subfiles
    def OutputParts( self ):
        return self.mOutputParts
        
    ## Get pathfile of the list file (a txt file containing 1 line for each subfile)
    #
    #  @return  Path  The list file
    def OutputList( self ):
        return self.mOutputList
        
    ## Get pathfile of the avi (final) file
    #
    #  @return  Path  The avi file
    def OutputAvi( self ):
        return self.mOutputAvi

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
    