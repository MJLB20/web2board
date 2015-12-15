#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------#
#                                                                       #
# This file is part of the web2board project                            #
#                                                                       #
# Copyright (C) 2015 Mundo Reader S.L.                                  #
#                                                                       #
# Date: November 2015                                                   #
# Author: Irene Sanz Nieto <irene.sanz@bq.com>                          #
#                                                                       #
# -----------------------------------------------------------------------#
import distutils
import json
import shutil
import zipfile
from distutils.dir_util import mkpath
from urllib2 import urlopen, URLError, HTTPError

from libs.PathConstants import *


##
# Class LibraryUpdater, created to check for downloaded libraries and update them if necessary
#

class LibraryUpdater:
    def __init__(self):
        # Select Sketchbook folder depending on OS
        if platform.system() == 'Linux':
            # self.pathToSketchbook = expanduser("~").decode('latin1')+'/Arduino/libraries'
            self.pathToSketchbook = base.sys_path.get_home_path() + '/Arduino'

        elif platform.system() == 'Windows' or platform.system() == 'Darwin':
            # self.pathToSketchbook = expanduser("~").decode('latin1')+'/Documents/Arduino/libraries'
            self.pathToSketchbook = base.sys_path.get_document_path() + '/Arduino'

        self.pathToMain = sys.path[0]
        if platform.system() == 'Darwin':
            if os.environ.get('PYTHONPATH') is not None:
                self.pathToMain = os.environ.get('PYTHONPATH')

    def updateWeb2BoardVersion(self):
        # Get bitbloqLibs version from config file

        self.__copyConfigInHomeIfNotExists()

        with open(RES_CONFIG_PATH) as json_data_file:
            data = json.load(json_data_file)
            versionTrue = str(data.get('bitbloqLibsVersion', "0.0.0"))

        with open(WEB2BOARD_CONFIG_PATH, "r+") as json_data_file:
            data = json.load(json_data_file)
            versionLocal = str(data['bitbloqLibsVersion'])
            if versionLocal != versionTrue:
                data['bitbloqLibsVersion'] = versionTrue

    def getBitbloqLibsVersion(self):
        # Get bitbloqLibs version from config file
        self.__copyConfigInHomeIfNotExists()
        with open(WEB2BOARD_CONFIG_PATH) as json_data_file:
            data = json.load(json_data_file)
            version = str(data['bitbloqLibsVersion'])
        return version

    def getBitbloqLibsName(self):
        # Get bitbloqLibs name from config file
        self.__copyConfigInHomeIfNotExists()
        with open(WEB2BOARD_CONFIG_PATH) as json_data_file:
            data = json.load(json_data_file)
            bitbloqLibsName = []
            try:
                bitbloqLibsName = data['bitbloqLibsName']
            except:
                print 'No bitbloqLibsName'
                pass
        return bitbloqLibsName

    def setBitbloqLibsVersion(self, newVersion):
        self.__copyConfigInHomeIfNotExists()
        jsonFile = open(WEB2BOARD_CONFIG_PATH, "r")
        data = json.load(jsonFile)
        jsonFile.close()

        data["bitbloqLibsVersion"] = newVersion

        jsonFile = open(WEB2BOARD_CONFIG_PATH, "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

    def setBitbloqLibsNames(self, bitbloqLibsNames):
        self.__copyConfigInHomeIfNotExists()
        jsonFile = open(WEB2BOARD_CONFIG_PATH, "r")
        data = json.load(jsonFile)
        jsonFile.close()

        data["bitbloqLibsName"] = bitbloqLibsNames

        jsonFile = open(WEB2BOARD_CONFIG_PATH, "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
        print "config ready"

    def __copyConfigInHomeIfNotExists(self):
        if not os.path.isfile(WEB2BOARD_CONFIG_PATH):
            shutil.copyfile(RES_CONFIG_PATH, WEB2BOARD_CONFIG_PATH)

    def downloadFile(self, url, path='.'):
        # Open the url
        try:
            f = urlopen(url)
            print "downloading " + url

            # Open our local file for writing
            with open(base.sys_path.get_tmp_path() + '/' + os.path.basename(url), "wb") as local_file:
                local_file.write(f.read())

                # handle errors
        except HTTPError, e:
            print "HTTP Error:", e.code, url
        except URLError, e:
            print "URL Error:", e.reason, url

    def downloadLibs(self):
        version = self.getBitbloqLibsVersion()
        print ('Downloading new libs, version', version)

        # Download bitbloqLibs
        url = ('https://github.com/bq/bitbloqLibs/archive/v' + version + '.zip')
        self.downloadFile(url)

        # Extract it to the correct dir
        with zipfile.ZipFile(base.sys_path.get_tmp_path() + '/' + 'v' + version + '.zip', "r") as z:
            z.extractall(base.sys_path.get_tmp_path())

        tmp_path = base.sys_path.get_tmp_path() + '/bitbloqLibs-' + version
        if int(version.replace('.', '')) <= 2:
            distutils.dir_util.copy_tree(tmp_path, self.pathToSketchbook + '/libraries/bitbloqLibs')
            bitbloqLibsNames = 'bitbloqLibs'
        elif int(version.replace('.', '')) > 2:
            for name in os.listdir(tmp_path):
                if os.path.isdir(tmp_path + '/' + name):
                    try:
                        distutils.dir_util.copy_tree(tmp_path, self.pathToSketchbook + '/libraries/')
                    except OSError as e:
                        logging.debug('Error: exception in copy_tree with ' + name)
                        logging.debug(e)

                        # shutil.copytree(tmp_path, self.pathToSketchbook+'/libraries/'+name)
            bitbloqLibsNames = [name for name in os.listdir(base.sys_path.get_tmp_path() + '/bitbloqLibs-' + version) if
                                os.path.isdir(
                                    os.path.join(base.sys_path.get_tmp_path() + '/bitbloqLibs-' + version, name))]
        else:
            raise RuntimeError("version not supported")

        # Store the names of the bitbloq libraries
        self.setBitbloqLibsNames(bitbloqLibsNames)

        # Remove .zip
        try:
            os.remove(base.sys_path.get_tmp_path() + '/' + 'v' + version + '.zip')
        except OSError as e:
            logging.debug('exception in os.remove')
            logging.debug(e)

        logging.info("Bitbloq libs downloaded")

    def libExists(self):
        self.updateWeb2BoardVersion()

        missingLibs = False
        libsNames = self.getBitbloqLibsName()
        if not os.path.exists(self.pathToSketchbook):
            os.makedirs(self.pathToSketchbook)
        if len(libsNames) < 1:
            missingLibs = True
        else:
            if libsNames == 'bitbloqLibs':
                libsNames = ['bitbloqLibs']
            for lib in libsNames:
                libPath = self.pathToSketchbook + os.sep + 'libraries' + os.sep + lib
                if not os.path.exists(libPath) or not os.listdir(libPath):
                    missingLibs = True
                    break

        if missingLibs:
            self.downloadLibs()
