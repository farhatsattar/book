---
sidebar_position: 3
---

# Robot Control Architecture

## Introduction

![Robot Control Architecture Overview](/img/robot-control-architectures.svg)

*Figure 4.1: Overview of different robot control architectures showing centralized, distributed, and hierarchical approaches.*

Robot control architecture defines the organizational structure and communication patterns that govern how different components of a robotic system interact to achieve coordinated behavior. The choice of control architecture significantly impacts a robot's performance, reliability, scalability, and maintainability. This chapter explores the major approaches to robot control architecture, their characteristics, advantages, and appropriate use cases.

In the context of ROS 2, control architectures benefit from the framework's distributed communication capabilities, quality of service settings, and modular node design. Understanding these architectural patterns is essential for developing robust and efficient robotic systems.

## Centralized Control Architecture

### Overview

![Centralized Control Architecture](/img/centralized-control-arch.svg)

*Figure 4.2: Centralized control architecture with a single controller managing all robot functions.*

Centralized control architecture features a single, central controller that makes all high-level decisions and coordinates all robot activities. This controller typically has complete knowledge of the robot's state and environment, processing all sensor data and generating all control commands.

### Characteristics

- **Single Decision Maker**: One central controller handles all planning, decision-making, and coordination
- **Global State Knowledge**: The central controller maintains a complete model of the robot and environment
- **Unified Control Logic**: All control algorithms run in a single location
- **Simple Coordination**: Direct communication between the central controller and all subsystems

### Advantages

- **Consistent Decision-Making**: All decisions are made with global knowledge and consistent priorities
- **Coordinated Behavior**: Easy to ensure all subsystems work together harmoniously
- **Simplified State Management**: Single location for state estimation and tracking
- **Predictable Behavior**: Clear decision-making process with traceable logic

### Disadvantages

- **Single Point of Failure**: If the central controller fails, the entire system stops functioning
- **Scalability Limitations**: Performance degrades as the system grows in complexity
- **Computational Bottleneck**: All processing must go through a single controller
- **Communication Overhead**: All data must flow to and from the central controller

### ROS 2 Implementation

In ROS 2, centralized control can be implemented using a primary control node that subscribes to all sensor topics and publishes to all actuator topics. This node would implement all high-level control logic and coordinate the robot's behavior.

```python
# Example centralized controller node
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class CentralizedController(Node):
    def __init__(self):
        super().__init__('centralized_controller')

        # Subscriptions to all sensor data
        self.lidar_sub = self.create_subscription(
            LaserScan, 'lidar_scan', self.lidar_callback, 10)
        self.camera_sub = self.create_subscription(
            Image, 'camera_image', self.camera_callback, 10)

        # Publisher for robot commands
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # State management
        self.robot_state = {}

        # Control loop timer
        self.timer = self.create_timer(0.1, self.control_loop)

    def lidar_callback(self, msg):
        self.robot_state['lidar'] = msg.ranges

    def camera_callback(self, msg):
        self.robot_state['camera'] = msg.data

    def control_loop(self):
        # Implement centralized control logic
        cmd_vel = self.compute_control_action()
        self.cmd_vel_pub.publish(cmd_vel)
```

## Distributed Control Architecture

### Overview

![Distributed Control Architecture](/img/distributed-control-arch.svg)

*Figure 4.3: Distributed control architecture with multiple specialized controllers communicating peer-to-peer.*

Distributed control architecture spreads control functions across multiple specialized controllers, each responsible for a specific subsystem or task. These controllers communicate with each other to achieve coordinated behavior without a single central authority.

### Characteristics

- **Decentralized Decision-Making**: Multiple controllers make decisions independently
- **Specialized Functions**: Each controller focuses on specific tasks or subsystems
- **Local State Knowledge**: Controllers maintain knowledge relevant to their specific functions
- **Peer-to-Peer Communication**: Controllers communicate directly with relevant peers

### Advantages

- **Fault Tolerance**: Failure of one controller doesn't necessarily stop the entire system
- **Scalability**: Easy to add new controllers and capabilities
- **Parallel Processing**: Multiple controllers can operate simultaneously
- **Specialization**: Each controller can be optimized for its specific task

### Disadvantages

- **Coordination Complexity**: Ensuring controllers work together harmoniously is challenging
- **Potential Conflicts**: Controllers might make conflicting decisions
- **Communication Overhead**: Controllers must communicate frequently to maintain coordination
- **Consistency Challenges**: Maintaining consistent system state across controllers

### ROS 2 Implementation

Distributed control in ROS 2 leverages the framework's ability to create multiple nodes that communicate through topics, services, and actions. Each controller runs as a separate node with specific responsibilities.

```python
# Example distributed control nodes
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class NavigationController(Node):
    def __init__(self):
        super().__init__('navigation_controller')
        self.lidar_sub = self.create_subscription(
            LaserScan, 'lidar_scan', self.lidar_callback, 10)
        self.velocity_pub = self.create_publisher(Twist, 'desired_velocity', 10)

    def lidar_callback(self, msg):
        # Compute navigation commands based on lidar data
        # This is a placeholder for the actual navigation command computation
        cmd_vel = Twist()  # Create a default Twist message
        cmd_vel.linear.x = 0.3  # Move forward at 0.3 m/s
        cmd_vel.angular.z = 0.1  # Small angular adjustment
        self.velocity_pub.publish(cmd_vel)

class ManipulationController(Node):
    def __init__(self):
        super().__init__('manipulation_controller')
        self.object_sub = self.create_subscription(
            Float32, 'object_distance', self.object_callback, 10)
        self.gripper_pub = self.create_publisher(Float32, 'gripper_command', 10)

    def object_callback(self, msg):
        # Control manipulation based on object detection
        # This is a placeholder for the actual gripper command computation
        gripper_cmd = Float32()  # Create a default Float32 message
        if msg.data < 0.5:  # If object is closer than 0.5 meters
            gripper_cmd.data = 1.0  # Close gripper
        else:
            gripper_cmd.data = 0.0  # Open gripper
        self.gripper_pub.publish(gripper_cmd)

class CoordinationController(Node):
    def __init__(self):
        super().__init__('coordination_controller')
        # Subscribe to both controllers and coordinate their activities
        self.nav_cmd_sub = self.create_subscription(
            Twist, 'desired_velocity', self.nav_command_callback, 10)
        self.manip_cmd_sub = self.create_subscription(
            Float32, 'gripper_command', self.manip_command_callback, 10)
        # Publish final commands to actuators
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
```

## Hierarchical Control Architecture

### Overview

![Hierarchical Control Architecture](/img/hierarchical-control-arch.svg)

*Figure 4.4: Hierarchical control architecture with layered control structure and goal propagation.*

Hierarchical control architecture organizes control functions in layers, with higher-level controllers providing goals and constraints to lower-level controllers. This approach combines the coordination benefits of centralized control with the scalability of distributed control.

### Characteristics

- **Layered Structure**: Controllers organized in levels with clear authority relationships
- **Goal Propagation**: Higher-level controllers provide goals to lower-level controllers
- **Feedback Flow**: Lower-level controllers report status and constraints to higher levels
- **Abstraction Levels**: Different levels operate at different levels of abstraction

### Advantages

- **Scalability**: Can handle complex systems by breaking them into manageable layers
- **Maintainable Structure**: Clear separation of concerns between layers
- **Fault Isolation**: Problems in one layer don't necessarily affect others
- **Modularity**: Layers can be developed and tested independently

### Disadvantages

- **Communication Overhead**: Multiple layers require extensive communication
- **Coordination Delays**: Information must propagate through multiple layers
- **Complexity**: More complex to design and debug than simpler architectures
- **Dependency Management**: Layers must be carefully designed to avoid circular dependencies

### ROS 2 Implementation

Hierarchical control in ROS 2 can be implemented using action servers at different levels, where higher-level nodes send goals to lower-level action servers.

```python
# Example hierarchical control using ROS 2 actions
import rclpy
from rclpy.action import ActionServer, ActionClient
from rclpy.node import Node
from example_interfaces.action import NavigateToPose
from geometry_msgs.msg import Pose, Twist

class HighLevelController(Node):
    def __init__(self):
        super().__init__('high_level_controller')
        # Action client to send navigation goals to mid-level
        self.nav_client = ActionClient(
            self, NavigateToPose, 'mid_level_navigation')

    def execute_navigation_task(self, goal):
        # Send goal to mid-level controller
        self.nav_client.send_goal_async(goal)

class MidLevelController(Node):
    def __init__(self):
        super().__init__('mid_level_controller')
        # Action server to receive goals from high-level
        self.nav_server = ActionServer(
            self, NavigateToPose, 'mid_level_navigation', self.execute_nav_goal)
        # Action client to send detailed commands to low-level
        self.motion_client = ActionClient(
            self, NavigateToPose, 'low_level_motion_control')

    def execute_nav_goal(self, goal_handle):
        # Break down high-level goal into detailed motion commands
        detailed_goal = self.create_detailed_goal_from_request(goal_handle.request)
        self.motion_client.send_goal(detailed_goal)
        # Note: get_result() is async, should use callback or await
        # For example purposes, assuming the action completes successfully
        goal_handle.succeed()
        return NavigateToPose.Result()

    def create_detailed_goal_from_request(self, request):
        # This is a placeholder for the actual detailed goal creation
        # Create a new goal based on the high-level request
        detailed_goal = NavigateToPose.Goal()
        detailed_goal.pose = request.pose  # Use the same pose for simplicity
        return detailed_goal

class LowLevelController(Node):
    def __init__(self):
        super().__init__('low_level_controller')
        # Action server for detailed motion control
        self.motion_server = ActionServer(
            self, NavigateToPose, 'low_level_motion_control', self.execute_motion_goal)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def execute_motion_goal(self, goal_handle):
        # Execute low-level motion control
        # Convert goal to velocity commands
        cmd_vel = self.compute_velocity_commands_from_pose(goal_handle.request.pose)
        self.cmd_vel_pub.publish(cmd_vel)
        goal_handle.succeed()
        return NavigateToPose.Result()

    def compute_velocity_commands_from_pose(self, pose):
        # This is a placeholder for the actual velocity command computation
        cmd_vel = Twist()  # Create a default Twist message
        cmd_vel.linear.x = 0.2  # Move forward at 0.2 m/s
        cmd_vel.angular.z = 0.1  # Small angular adjustment
        return cmd_vel
```

## Behavior-Based Control Architecture

### Overview

![Behavior-Based Control Architecture](/img/behavior-based-control-arch.svg)

*Figure 4.5: Behavior-based control architecture with concurrent reactive behaviors and arbitration mechanism.*

Behavior-based control architecture decomposes robot behavior into a collection of simple, reactive behaviors that operate concurrently. Each behavior responds to specific environmental conditions or internal states, and a coordination mechanism arbitrates between potentially conflicting behaviors.

### Characteristics

- **Reactive Behaviors**: Simple, stimulus-response patterns
- **Concurrent Operation**: Multiple behaviors active simultaneously
- **Local Sensory Processing**: Each behavior processes relevant sensory information
- **Coordination Mechanism**: Arbitration between competing behaviors

### Advantages

- **Robustness**: Simple behaviors are reliable and predictable
- **Reactivity**: Fast response to environmental changes
- **Modularity**: Behaviors can be added, removed, or modified independently
- **Biological Inspiration**: Reflects how natural systems often operate

### Disadvantages

- **Coordination Complexity**: Difficult to ensure coherent overall behavior
- **Emergent Behavior**: Complex interactions between behaviors can be unpredictable
- **Limited Planning**: Not well-suited for complex, multi-step tasks
- **Debugging Difficulty**: Emergent behavior can be hard to understand and fix

### ROS 2 Implementation

Behavior-based control in ROS 2 can be implemented using multiple nodes that represent different behaviors, with a behavior arbitrator node that selects which behavior should control the robot at any given time.

```python
# Example behavior-based control
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Pose
import math

class AvoidObstacleBehavior(Node):
    def __init__(self):
        super().__init__('avoid_obstacle_behavior')
        self.lidar_sub = self.create_subscription(
            LaserScan, 'lidar_scan', self.lidar_callback, 10)
        self.behavior_pub = self.create_publisher(Twist, 'behavior_avoid_obstacle', 10)

    def lidar_callback(self, msg):
        # Check for obstacles in front of robot
        if min(msg.ranges[300:420]) < 1.0:  # Obstacle in front
            cmd_vel = Twist()
            cmd_vel.angular.z = 0.5  # Turn away from obstacle
            self.behavior_pub.publish(cmd_vel)

class GoToGoalBehavior(Node):
    def __init__(self):
        super().__init__('go_to_goal_behavior')
        self.goal_sub = self.create_subscription(
            Pose, 'goal_pose', self.goal_callback, 10)
        self.behavior_pub = self.create_publisher(Twist, 'behavior_go_to_goal', 10)

    def goal_callback(self, msg):
        # Compute velocity to move toward goal
        # This is a placeholder for the actual goal direction calculation
        cmd_vel = Twist()  # Create a default Twist message
        cmd_vel.linear.x = 0.5  # Move forward at 0.5 m/s
        self.behavior_pub.publish(cmd_vel)

class BehaviorArbitrator(Node):
    def __init__(self):
        super().__init__('behavior_arbitrator')
        self.avoid_sub = self.create_subscription(
            Twist, 'behavior_avoid_obstacle', self.avoid_callback, 10)
        self.goal_sub = self.create_subscription(
            Twist, 'behavior_go_to_goal', self.goal_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.avoid_cmd = Twist()
        self.goal_cmd = Twist()

    def avoid_callback(self, msg):
        self.avoid_cmd = msg
        self.compute_final_command()

    def goal_callback(self, msg):
        self.goal_cmd = msg
        self.compute_final_command()

    def compute_final_command(self):
        # Arbitrate between behaviors based on priority
        if self.avoid_cmd.angular.z != 0:  # Avoidance behavior active
            self.cmd_vel_pub.publish(self.avoid_cmd)
        else:
            self.cmd_vel_pub.publish(self.goal_cmd)
```

## Hybrid Control Architectures

### Overview

![Hybrid Control Architecture](/img/hybrid-control-arch.svg)

*Figure 4.6: Hybrid control architecture combining multiple architectural approaches.*

Hybrid control architectures combine elements from different architectural approaches to leverage the advantages of each while mitigating their individual disadvantages. These architectures often feature a central coordinator with distributed specialized controllers, or hierarchical structures with behavior-based components at lower levels.

### Characteristics

- **Mixed Approaches**: Combines multiple architectural patterns
- **Context-Dependent**: Different architectures used for different situations
- **Flexible Structure**: Can adapt control approach based on task requirements
- **Optimized Performance**: Uses best approach for each specific aspect

### Advantages

- **Best-of-Breed**: Leverages advantages of multiple approaches
- **Adaptability**: Can adjust architecture based on task requirements
- **Balanced Trade-offs**: Mitigates disadvantages of pure approaches
- **Task-Optimized**: Different parts of system use most appropriate control method

### Disadvantages

- **Complexity**: More complex to design, implement, and maintain
- **Integration Challenges**: Different architectural components must work together
- **Debugging Difficulty**: More complex interactions to understand
- **Coordination Overhead**: Multiple coordination mechanisms may be needed

## Real-Time Considerations in Control Architectures

### Timing Constraints

Robot control systems often have strict timing requirements that must be met for safe and effective operation. Different control architectures handle timing constraints differently:

- **Centralized**: Single timing bottleneck that must handle all control loops
- **Distributed**: Parallel timing paths but coordination delays
- **Hierarchical**: Timing requirements cascade through layers
- **Behavior-based**: Individual behaviors may have different timing needs

### Quality of Service in ROS 2

ROS 2's Quality of Service (QoS) settings are crucial for real-time robot control:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

# High-priority, real-time control messages
real_time_qos = QoSProfile(
    depth=1,  # Keep only latest message
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
    deadline=rclpy.duration.Duration(seconds=0.1)  # 100ms deadline
)

# For critical control commands
cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', real_time_qos)
```

### Middleware Selection

The choice of ROS middleware (DDS implementation) can significantly impact real-time performance:

- **Fast DDS**: Optimized for low-latency applications
- **Cyclone DDS**: Lightweight with good real-time characteristics
- **RTI Connext**: Commercial solution with strong real-time guarantees

## Choosing the Right Architecture

### Factors to Consider

When selecting a robot control architecture, consider the following factors:

1. **System Complexity**: Simple robots may benefit from centralized control, while complex systems may require distributed approaches
2. **Reliability Requirements**: Safety-critical systems may need redundant distributed architectures
3. **Real-time Constraints**: Timing requirements may favor specific architectural approaches
4. **Development Resources**: Different architectures have different development and maintenance costs
5. **Scalability Needs**: Future growth requirements should influence architectural choices

### Application-Specific Recommendations

- **Simple Mobile Robots**: Behavior-based or simple centralized control
- **Multi-Arm Manipulation**: Hierarchical control with coordination layers
- **Swarm Robotics**: Distributed control with local coordination
- **Humanoid Robots**: Hybrid architectures with specialized controllers
- **Industrial Automation**: Centralized or hierarchical control with real-time guarantees

## Integration with ROS 2 Ecosystem

### Launch Files for Architecture Management

ROS 2 launch files provide a powerful way to start and configure control architectures:

```python
# Example launch file for distributed control system
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Launch distributed control nodes
        Node(
            package='robot_control',
            executable='navigation_controller',
            name='navigation_controller',
            parameters=[{'use_sim_time': False}]
        ),
        Node(
            package='robot_control',
            executable='manipulation_controller',
            name='manipulation_controller',
            parameters=[{'use_sim_time': False}]
        ),
        Node(
            package='robot_control',
            executable='coordination_controller',
            name='coordination_controller',
            parameters=[{'use_sim_time': False}]
        ),
    ])
```

### Parameter Management

ROS 2's parameter system allows runtime configuration of control architectures:

```python
# Parameter declaration for control architecture
self.declare_parameter('control_mode', 'autonomous')
self.declare_parameter('navigation_speed', 0.5)
self.declare_parameter('safety_distance', 1.0)
```

## Key Terms

- **Centralized Control Architecture**: A control architecture where a single central controller makes all high-level decisions and coordinates all robot activities
- **Distributed Control Architecture**: A control architecture that spreads control functions across multiple specialized controllers without a single central authority
- **Hierarchical Control Architecture**: A control architecture that organizes control functions in layers, with higher-level controllers providing goals to lower-level controllers
- **Behavior-Based Control Architecture**: A control architecture that decomposes robot behavior into simple, reactive behaviors that operate concurrently
- **Hybrid Control Architecture**: A control architecture that combines elements from different architectural approaches to leverage their advantages
- **Action Server**: A ROS 2 component that handles long-running tasks with feedback and the ability to cancel
- **Action Client**: A ROS 2 component that sends goals to action servers
- **Launch File**: A ROS 2 file written in Python that specifies how to launch multiple nodes with specific configurations
- **Message Filters**: ROS 2 tools that provide synchronization of messages from different topics
- **Approximate Time Synchronizer**: A message filter that synchronizes messages based on timestamps within a specified tolerance
- **Quality of Service (QoS)**: Settings in ROS 2 that define communication behavior including reliability, durability, history, and deadline constraints
- **Real-Time Control**: Control systems that must respond to inputs within strict timing constraints
- **Middleware Selection**: The choice of underlying middleware implementation (DDS) that affects performance and real-time capabilities

## Summary

Robot control architecture is a fundamental design decision that significantly impacts a robot system's performance, reliability, and maintainability. The choice between centralized, distributed, hierarchical, behavior-based, or hybrid architectures depends on the specific requirements of the robotic application.

ROS 2 provides powerful tools and patterns that support all major control architectures, from simple centralized controllers to complex distributed systems. The framework's communication patterns, QoS settings, and tooling ecosystem make it an excellent platform for implementing any control architecture approach.

Understanding these architectural patterns and their implementation in ROS 2 is essential for developing effective robot control systems that can meet the challenges of real-world applications.

---

*Continue to [ROS 2 Integration with Physical AI](integration.md) to explore how ROS 2 connects AI algorithms with physical robot systems.*