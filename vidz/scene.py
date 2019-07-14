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

class cScene:
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

    def Name( self, iName=None ):
        if iName is None:
            return self.mName
        
        previous_value = self.mName
        self.mName = iName
        return previous_value
    
    def QScale( self, iQScale=None ):
        if iQScale is None:
            return self.mQScale
        
        previous_value = self.mQScale
        self.mQScale = iQScale
        return previous_value

    def Intervals( self ):
        return self.mIntervals
    
    def AddInterval( self, iInterval ):
        self.mIntervals.append( iInterval )
        
    #---
    
    def BuildOutput( self, iOutputRoot ):
        self.mOutputDirectory = iOutputRoot / f'index{self.mSource.Index()}-{self.mName}'
        self.mOutputDirectory.mkdir( exist_ok=True )

        self.mOutputClean = self.mOutputDirectory / f'{self.mName}.clean.ts'
        self.mOutputList = self.mOutputDirectory / f'{self.mName}.list.txt'
        self.mOutputAvi = self.mOutputDirectory / f'{self.mName}.avi'
        
        for i, interval in enumerate( self.mIntervals ):
            self.mOutputParts.append( self.mOutputDirectory / f'{self.mName}.{i+1}.ts' )

    def OutputClean( self ):
        return self.mOutputClean
        
    def OutputParts( self ):
        return self.mOutputParts
        
    def OutputList( self ):
        return self.mOutputList
        
    def OutputAvi( self ):
        return self.mOutputAvi
        


class cInterval:
    def __init__( self ):
        self.mSS = None
        self.mTo = None
        self.mVMap = None
        self.mAMap = None
    
    def SS( self, iSS=None ):
        if iSS is None:
            return self.mSS
        
        previous_value = self.mSS
        self.mSS = iSS
        return previous_value

    def To( self, iTo=None ):
        if iTo is None:
            return self.mTo
        
        previous_value = self.mTo
        self.mTo = iTo
        return previous_value
    
    def VMap( self, iVMap=None ):
        if iVMap is None:
            return self.mVMap
        
        previous_value = self.mVMap
        self.mVMap = iVMap
        return previous_value
    
    def AMap( self, iAMap=None ):
        if iAMap is None:
            return self.mAMap
        
        previous_value = self.mAMap
        self.mAMap = iAMap
        return previous_value
    