
 
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import SetEnvironmentVariable

 
def generate_launch_description():
 
      # Constants for paths to different files and folders
    gazebo_models_path = 'models'
    package_name = 'gazebo_lab_b'

    robot_name_in_model = 'turtlebot3_burger'
    sdf_model_path = 'models/turtlebot3_burger/model.sdf'
    world_file_path = 'worlds/wall_following.world'

     
    # Pose where we want to spawn the robot
    spawn_x_val = '0.0'
    spawn_y_val = '0.0'
    spawn_z_val = '0.0'
    spawn_yaw_val = '0.0'
 
    ############ You do not need to change anything below this line #############
    # Set the path to different files and folders.  
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')   
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    world_path = os.path.join(pkg_share, world_file_path)
    gazebo_models_path = os.path.join(pkg_share, gazebo_models_path)
    os.environ["GAZEBO_MODEL_PATH"] = gazebo_models_path
    
    pkg_turtlebot3_gazebo = FindPackageShare(package='turtlebot3_gazebo').find('turtlebot3_gazebo')

    sdf_model_path = os.path.join(pkg_turtlebot3_gazebo, sdf_model_path)
    
    # Launch configuration variables specific to simulation
    gui = LaunchConfiguration('gui')
    headless = LaunchConfiguration('headless')
    namespace = LaunchConfiguration('namespace')
    sdf_model = LaunchConfiguration('sdf_model')
    use_namespace = LaunchConfiguration('use_namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_simulator = LaunchConfiguration('use_simulator')
    world = LaunchConfiguration('world')

    #not work
    # if 'GAZEBO_MODEL_PATH' in os.environ:
    #     os.environ['GAZEBO_MODEL_PATH'] += ":" + gazebo_models_path
    # else :
    #   os.environ['GAZEBO_MODEL_PATH'] = gazebo_models_path

  # Declare the launch arguments  
    declare_namespace_cmd = DeclareLaunchArgument(
        name='namespace',
        default_value='',
        description='Top-level namespace')
 
    declare_use_namespace_cmd = DeclareLaunchArgument(
        name='use_namespace',
        default_value='false',
        description='Whether to apply a namespace to the navigation stack')
             
    declare_sdf_model_path_cmd = DeclareLaunchArgument(
        name='sdf_model', 
        default_value=sdf_model_path, 
        description='Absolute path to robot sdf file')
    
    declare_simulator_cmd = DeclareLaunchArgument(
        name='headless',
        default_value='False',
        description='Whether to execute gzclient')
        
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')
    
    declare_use_simulator_cmd = DeclareLaunchArgument(
        name='use_simulator',
        default_value='True',
        description='Whether to start the simulator')
 
    declare_world_cmd = DeclareLaunchArgument(
        name='world',
        default_value=world_path,
        description='Full path to the world model file to load')
    
    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        condition=IfCondition(use_simulator),
        launch_arguments={'world': world}.items())
    
    # Start Gazebo client    
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')),
        condition=IfCondition(PythonExpression([use_simulator, ' and not ', headless])))
    
    # Launch the robot
    spawn_entity_cmd = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-entity', robot_name_in_model, 
                '-file', sdf_model,
                    '-x', spawn_x_val,
                    '-y', spawn_y_val,
                    '-z', spawn_z_val,
                    '-Y', spawn_yaw_val],
                    output='screen')
 
    # modify for lecture 
    # Emergency braking node
    emergency_braking_node = Node(
            package='gazebo_lab_b',
            executable='wall_following',
            name='wall_following_node',
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen',
        )

    # RViz node
    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='odometry_rviz',
            arguments=['-d', os.path.join(FindPackageShare(package='gazebo_lab_b').find('gazebo_lab_b')
    , 'rviz', 'gazebo_lab_b.rviz')],
        )

    # Create the launch description and populate
    ld = LaunchDescription()
    
    # Declare the launch options
    #ld.add_action(SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=gazebo_models_path))
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_namespace_cmd)
    ld.add_action(declare_sdf_model_path_cmd)
    ld.add_action(declare_simulator_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_use_simulator_cmd)
    ld.add_action(declare_world_cmd)
    
    # Add any actions
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(spawn_entity_cmd)
    ld.add_action(emergency_braking_node)

    ld.add_action(rviz_node)

 
    return ld