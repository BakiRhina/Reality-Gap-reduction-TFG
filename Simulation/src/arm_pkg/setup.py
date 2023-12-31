from setuptools import find_packages, setup

package_name = 'arm_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['launch/launch.py']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools'
        ],
    zip_safe=True,
    maintainer='kyu8',
    maintainer_email='guillemsenabre@gmail.com',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		'listener = arm_pkg.tests.joint_listener:main',
		'processor = arm_pkg.tests.joint_processor:main',
		'storage = arm_pkg.tests.joint_storage:main',
		'controller = arm_pkg.tests.joint_controller:main',
		'reset_controller = arm_pkg.tests.joint_position_reset:main',
		'gripper_test = arm_pkg.tests.data_gripper_test:main',
		'state_test = arm_pkg.tests.state_test:main',
		'robots_state = arm_pkg.drl.sub_modules.robots_state:main',
	    'sac = arm_pkg.drl.sac:main',
		'ddpg = arm_pkg.drl.sub_modules.ddpg:main',
        'main = arm_pkg.drl.main:main',
		'reward_function = arm_pkg.drl.sub_modules.reward_function:main',
        ],
    },
)
