"""
StrictCode Vulnerability Test Suite
Triggers: AST001, AST004, AST003, DEP001, SEC001-SEC007
"""
import os
import json
import base64

# [DEP001] HALLUCINATED IMPORT
# 'colorama' is real, but 'colorama_super_secure_edition' is fake/malicious
import colorama_super_secure_edition 


# [AST001] MISSING DOCSTRING
# This function has no docstring
def risky_business():
    
    # [SEC001] AWS ACCESS KEY
    aws_key = "AKIAIOSFODNN7EXAMPLE"
    
    # [SEC002] AWS SECRET KEY
    aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # [SEC003] GOOGLE API KEY
    gcp_key = "AIzaSyD-ExampleKeyForGoogle-12345"
    
    # [SEC004] SLACK TOKEN
    slack_token = "xoxb-123456789012-1234567890123-45678901234567890123456789012345"
    
    # [SEC005] STRIPE KEY
    stripe_key = "sk_live_51LbTvSE4VC4i2M8k404"
    
    # [SEC006] OPENAI KEY
    openai_key = "sk-ExampleOpenAIKey1234567890"

    # [SEC007] GITHUB TOKEN
    gh_token = "ghp_ExampleGitHubPersonalAccessToken123"

    try:
        x = 1 / 0
    # [AST004] EMPTY EXCEPT BLOCK
    except:
        pass


# [AST003] CYCLOMATIC COMPLEXITY (>10)
# This function is too complex (too many branches)
def complex_spaghetti(x):
    if x == 1:
        return 1
    elif x == 2:
        return 2
    elif x == 3:
        return 3
    elif x == 4:
        return 4
    elif x == 5:
        return 5
    elif x == 6:
        return 6
    elif x == 7:
        return 7
    elif x == 8:
        return 8
    elif x == 9:
        return 9
    elif x == 10:
        return 10
    else:
        return 0
