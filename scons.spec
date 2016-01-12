# -*- mode: python -*-
import sys
import os

sys.path.append(os.getcwd())
from libs import utils
from libs.PathsManager import PathsManager
block_cipher = None

a = Analysis([PathsManager.EXTERNAL_RESOURCES_PATH + os.sep +'sconsScript.py'],
             pathex=[os.getcwd()],
             binaries=None,
             datas=None,
             hiddenimports=['UserList', 'UserString', 'ConfigParser'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

a.datas += utils.findFilesForPyInstaller("platformio", ["*", "**/*"])
a.datas += utils.findFilesForPyInstaller("res", ["*", "**/*"])
# a.datas += utils.findFilesForPyInstaller("Test/resources", ["*", "**/*"])

# a.datas += utils.findFilesForPyInstaller("scons", ["*", "**/*"])

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='sconsScript',
          debug=False,
          strip=None,
          upx=True,
          console=True)