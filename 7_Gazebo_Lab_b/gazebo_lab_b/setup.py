from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'gazebo_lab_b'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')), # Launch files
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')), # RViz config files
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')), # World files
        #(os.path.join('share', package_name, 'models'), glob('models/**/*', recursive=True)), # model files
        
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='',
    maintainer_email='',
    description='',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'emergency_braking = gazebo_lab_b.emergency_braking:main',
            'wall_following = gazebo_lab_b.wall_following:main',
        ],
    },
)