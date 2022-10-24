# flake8
CONFIG_FILE_NAME_FLAKE8 = '.flake8'
CONFIG_FILE_CONTENT_FLAKE8 = '''[flake8]
ignore = E501
exclude = .git,__pycache__,old,build,dist,venv,*/migrations/*,*/settings/*
max-complexity = 10
per-file-ignores = __init__.py: F401, F403, F405
'''

# radon
CONFIG_FILE_NAME_RADON = 'radon.cfg'
CONFIG_FILE_CONTENT_RADON = '''[radon]
exclude = */venv/*
cc_min = C
'''

# bandit
CONFIG_FILE_NAME_BANDIT = '.bandit'
CONFIG_FILE_CONTENT_BANDIT = '''[bandit]
'''

# unit tests
CONFIG_FILE_NAME_TESTCASE = 'testcaserc.json'
CONFIG_FILE_CONTENT_TESTCASE = '''
{
    "apps": [],
    "keepdb": true
}
'''

# test coverage
CONFIG_FILE_NAME_COVERAGE = '.coveragerc'
CONFIG_FILE_CONTENT_COVERAGE = '''
[run]
source = .
omit = ./venv/*,*tests*,*apps.py,*manage.py,*__init__.py,*migrations*,*asgi*,*wsgi*,*admin.py,*urls.py

[report]
omit = ./venv/*,*tests*,*apps.py,*manage.py,*__init__.py,*migrations*,*asgi*,*wsgi*,*admin.py,*urls.py
'''

# lighthouse
CONFIG_FILE_NAME_LIGHTHOUSE = 'lighthouserc.json'
CONFIG_FILE_CONTENT_LIGHTHOUSE = '''
{
  "ci": {
    "collect": {
      "url": "http://127.0.0.1:8000"
    },
    "assert": {
      "assertions": {
        "categories:performance": [
          "error",
          {
            "minScore": 0.90
          }
        ],
        "categories:accessibility": [
          "error",
          {
            "minScore": 0.90
          }
        ],
        "categories:best-practices": [
          "error",
          {
            "minScore": 0.90
          }
        ],
        "categories:SEO": [
          "error",
          {
            "minScore": 0.90
          }
        ]
      }
    }
  }
}
'''
