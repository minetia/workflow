# -*- coding: utf-8 -*-
import sys
import os

BASE_DIR = r"c:\lovesoong"
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

try:
    from routes import shared
    print("SUCCESS: routes.shared imported")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")
except Exception as e:
    print(f"FAILURE: {e}")
