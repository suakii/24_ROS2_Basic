from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'gazebo_lab_a'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
     data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')), # Launch files
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')), # RViz config files
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='suakii',
    maintainer_email='suakii@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'circle = gazebo_lab_a.circle:main', # Python script
            'square = gazebo_lab_a.square:main', # Python script

        ],
    },
)
