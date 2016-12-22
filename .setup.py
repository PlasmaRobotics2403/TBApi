# A file used to generate upload packages for TBApi.  Not meant for home-use.

from setuptools import setup

setup(name='tbapi',
      version='1.0.0',
      description='A Python Library for connection to The Blue Alliance API v2 | Created by Plasma Robotics, Team 2403',
      url='https://github.com/PlasmaRobotics2403/TBA-PythonAPI',
      author='Plasma Robotics | FRC Team 2403',
      author_email='plasma2403@gmail.com',
      license='MIT',
      packages=['tbapi'],
      install_requires=['requests','datetime','numpy'],
      zip_safe=False)
