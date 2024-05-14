from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turtlesim_lab_a'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')), # Launch files
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
            'open_loop_circle = turtlesim_lab_a.open_loop_circle:main',
            'open_loop_square = turtlesim_lab_a.open_loop_square:main',  
            'closed_loop_square = turtlesim_lab_a.closed_loop_square:main',
        ],
    },
)
