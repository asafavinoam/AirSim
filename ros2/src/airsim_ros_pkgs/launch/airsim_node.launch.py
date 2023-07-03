import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    output = DeclareLaunchArgument(
        "output",
        default_value='log')

    publish_clock = DeclareLaunchArgument(
        "publish_clock",
        default_value='False')

    is_vulkan = DeclareLaunchArgument(
        "is_vulkan",
        default_value='True')
    
    is_enu = DeclareLaunchArgument(
        "is_enu",
        default_value='False')

    host = DeclareLaunchArgument(
        "host",
        default_value='localhost')
    
    publish_odom_tf = DeclareLaunchArgument(
        "publish_odom_tf",
        default_value='True')

    publish_gps_tf = DeclareLaunchArgument(
        "publish_gps_tf",
        default_value='False')

    publish_imu_tf = DeclareLaunchArgument(
        "publish_imu_tf",
        default_value='False')
  
    airsim_node = Node(
            package='airsim_ros_pkgs',
            executable='airsim_node',
            name='airsim_node',
            output='screen',
            parameters=[{
                'is_vulkan': False,
                'update_airsim_img_response_every_n_sec': 0.05,
                'update_airsim_control_every_n_sec': 0.01,
                'update_lidar_every_n_sec': 0.01,
                'publish_clock': LaunchConfiguration('publish_clock'),
                'host_ip': LaunchConfiguration('host'),
                'publish_odom_tf': LaunchConfiguration('publish_odom_tf'),
                'coordinate_system_enu': LaunchConfiguration('is_enu'),
            }])

    gps_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='GpsTransformAirSim',
        condition=IfCondition(LaunchConfiguration('publish_gps_tf')),
        arguments=['0', '0', '0', '0', '0', '0', 'Probot', 'Probot/Gps']
    )

    imu_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='ImuTransformAirSim',
        condition=IfCondition(LaunchConfiguration('publish_imu_tf')),
        arguments=['0', '0', '0', '0', '0', '0', 'Probot', 'Probot/Imu']
    )

    static_transforms = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('airsim_ros_pkgs'), 'launch/static_transforms.launch.py')
        ),
        condition=IfCondition(LaunchConfiguration('publish_odom_tf'))
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(output)
    ld.add_action(publish_clock)
    ld.add_action(is_vulkan)
    ld.add_action(is_enu)
    ld.add_action(host)
    ld.add_action(publish_odom_tf)
    ld.add_action(publish_gps_tf)
    ld.add_action(publish_imu_tf)

    ld.add_action(static_transforms)  
    ld.add_action(airsim_node)
    ld.add_action(gps_tf)
    ld.add_action(imu_tf)

    return ld
