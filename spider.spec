# -*- mode: python -*-
a = Analysis(['spider.py'],
             pathex=['/Users/chexiaoyu/Spider_DUT_withoutPyquery'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='spider',
          debug=False,
          strip=None,
          upx=True,
          console=True )
app = BUNDLE(exe,
			 a.datas,
			 name='Spider.app')
