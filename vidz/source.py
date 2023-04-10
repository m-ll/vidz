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
import random

## Manage source file
class cSource:

    ## Create a source
    #
    #  @param  iXMLNode  xml.etree.ElementTree.Element      The node of the source
    #  @return           cSource  The source depending of the node
    #  @return           None     No source was found for the node
    def Create( iXMLNode ):
        dvd = iXMLNode.get( 'dvd' )
        if dvd is not None:
            return cSourceDVD( dvd )

        pathfile = iXMLNode.get( 'file' )
        if pathfile is not None:
            return cSourceFile( pathfile )

        return None

    #---

    ## The constructor
    #
    #  @param  iId  int  The id of the source
    def __init__( self, iId ):
        self.mId = iId
        self.mPathFile = None

    ## Build the source path
    #
    #  @return  bool  The file has been build and found
    def Build( self ):
        return False

    ## Get the id
    #
    #  @return  string  The id
    def Id( self ):
        return self.mId
        
    ## Get the pathfile
    #
    #  @return  pathlib.Path  The source pathfile
    def PathFile( self ):
        return self.mPathFile
        
#---

## Manage dvd source file
#
#  It can only manage a harddisk on drive f: / g: / h:
#  and the structure inside must be like dvd (f:/LGDVR/000000XXREC/*.TS)
class cSourceDVD( cSource ):

    ## The constructor
    #
    #  @param  iId  int  The id of the source
    def __init__( self, iId ):
        super().__init__( iId )

    ## Build the source path
    #
    #  @return  bool  The file has been build and found
    def Build( self ):
        path = Path( 'F:' ) / 'LGDVR' / f'000000{self.Id()}REC'
        source_pathfile = list( path.glob( '*.TS' ) )
        if source_pathfile:
            self.mPathFile = Path( source_pathfile[0] )
            return True

        path = Path( 'G:' ) / 'LGDVR' / f'000000{self.Id()}REC'
        source_pathfile = list( path.glob( '*.TS' ) )
        if source_pathfile:
            self.mPathFile = Path( source_pathfile[0] )
            return True

        path = Path( 'H:' ) / 'LGDVR' / f'000000{self.Id()}REC'
        source_pathfile = list( path.glob( '*.TS' ) )
        if source_pathfile:
            self.mPathFile = Path( source_pathfile[0] )
            return True

        return False

#---

## Manage regular source file
class cSourceFile( cSource ):

    ## The constructor
    #
    #  @param  iId     int     The id of the source
    #  @param  iInput  string  The input pathfile
    def __init__( self, iInput ):
        super().__init__( random.randint( 1000, 9999 ) )
        self.mInput = iInput

    ## Build the source path
    #
    #  @return  bool  The file has been build and found
    def Build( self ):
        path = Path( self.mInput )
        if not path.exists():
            return False
        
        self.mPathFile = path

        return True
