---
sidebar_position: 2
---

# ROS 2 Fundamentals

## Introduction

ROS 2 (Robot Operating System 2) is the next generation of the Robot Operating System, designed to provide a flexible framework for writing robot software. Unlike traditional operating systems, ROS 2 is a middleware that provides services such as hardware abstraction, device drivers, libraries, visualizers, message-passing, and package management. It enables the development of complex robotic systems by facilitating communication between different software components.

ROS 2 addresses many of the limitations of the original ROS, including improved security, real-time capabilities, and better support for commercial applications. It's designed to work in distributed systems, making it ideal for robot control applications where different components need to communicate seamlessly.

## ROS 2 Architecture

### Nodes

Nodes are the fundamental building blocks of any ROS 2 application. A node is a process that performs computation and is designed to be a modular component of a larger robot application. Each node typically performs a specific task or set of tasks, such as sensor data processing, control algorithm execution, or user interface management.

In ROS 2, nodes are implemented as objects that inherit from the `rclcpp::Node` class (in C++) or the `rclpy.Node` class (in Python). This design allows nodes to access ROS 2 functionality such as creating publishers, subscribers, services, and actions.

Key characteristics of ROS 2 nodes:
- Each node runs in its own process
- Nodes can be written in different programming languages
- Nodes communicate with each other through topics, services, and actions
- Nodes can be launched together using launch files

### Communication Patterns

ROS 2 provides three main communication patterns for nodes to interact:

#### Topics and Messages

Topics enable asynchronous, many-to-many communication between nodes using a publish-subscribe pattern. Publishers send messages to a topic, and subscribers receive messages from the topic. Multiple publishers can publish to the same topic, and multiple subscribers can subscribe to the same topic.

Messages are the data structures that are passed between nodes through topics. They have a specific type and contain the actual data being communicated. Message types are defined using the Interface Definition Language (IDL) and are compiled into language-specific structures.

#### Services

Services provide synchronous, request-response communication between nodes. A client sends a request to a server, and the server responds with a result. This pattern is useful for operations that require a direct response, such as configuration changes or action requests.

Service interfaces define the structure of the request and response messages. Like topics, services use IDL to define the interface, which is then compiled for different programming languages.

#### Actions

Actions are designed for long-running tasks that require feedback and the ability to cancel. They combine the features of topics and services, providing goal requests, feedback during execution, and final results. Actions are ideal for tasks like navigation, manipulation, or any process that takes a significant amount of time to complete.

## Quality of Service (QoS) Settings

ROS 2 introduces Quality of Service (QoS) settings that allow fine-tuning of communication behavior. QoS settings include:

- **Reliability**: Whether messages should be reliably delivered (RELIABLE) or best-effort (BEST_EFFORT)
- **Durability**: Whether late-joining subscribers should receive old messages (TRANSIENT_LOCAL) or only new ones (VOLATILE)
- **History**: How many messages to keep in the queue (KEEP_ALL or KEEP_LAST)
- **Depth**: The size of the message queue when using KEEP_LAST

These settings are crucial for robot applications where different types of data have different requirements for timeliness, reliability, and persistence.

## Launch System

The ROS 2 launch system provides a way to start multiple nodes together with specific configurations. Launch files are written in Python and can include:

- Node definitions with parameters
- Parameter file loading
- Remapping of topics and services
- Conditional launching based on environment variables
- Integration with system services

This system is essential for deploying complex robotic systems where multiple components need to be started in a coordinated manner.

## Parameter System

ROS 2 includes a robust parameter system that allows runtime configuration of nodes. Parameters can be:

- Declared within nodes with types and constraints
- Set at launch time from parameter files
- Modified at runtime through the parameter service
- Shared between nodes using parameter services

The parameter system is critical for robot applications where configuration needs to be adjusted based on the environment or operational requirements.

## Real-Time Considerations

ROS 2 is designed with real-time systems in mind, offering features that are important for robot control:

- **Real-time safe code**: Libraries and tools for writing real-time safe code
- **Deadline and lifespan QoS**: Settings for managing timing constraints
- **RMW (ROS Middleware) interface**: Abstraction layer that allows different middleware implementations optimized for real-time performance
- **Memory management**: Tools and practices for avoiding dynamic memory allocation in real-time contexts

## Security Features

ROS 2 includes built-in security features that are essential for commercial and industrial applications:

- **Authentication**: Verification of node identity
- **Authorization**: Control over what nodes can do
- **Encryption**: Protection of data in transit
- **Access control**: Fine-grained permissions for different operations

These features make ROS 2 suitable for applications where security is a critical concern.

## ROS 2 vs. ROS 1

ROS 2 was developed to address the limitations of the original ROS (ROS 1):

- **Distributed systems**: ROS 2 works better in distributed environments
- **Security**: Built-in security features are available in ROS 2
- **Real-time**: Better support for real-time applications
- **Multiple DDS implementations**: Support for different middleware implementations
- **Official support**: ROS 2 has official support and maintenance
- **Modern C++**: Uses modern C++ practices and standards

## Practical Applications in Robot Control

ROS 2's architecture makes it particularly suitable for robot control systems:

1. **Modular design**: Different control components can be developed as separate nodes
2. **Language flexibility**: Control algorithms can be implemented in the most suitable language
3. **Communication patterns**: Different types of robot control tasks can use appropriate communication patterns
4. **Integration**: Easy integration with sensors, actuators, and AI algorithms
5. **Tooling**: Rich ecosystem of tools for debugging, visualization, and testing

## Key Terms

- **Node**: A process that performs computation in ROS 2
- **Topic**: A named bus over which nodes exchange messages
- **Message**: A simple data structure, comprising typed fields
- **Publisher**: A node that sends messages on a topic
- **Subscriber**: A node that receives messages from a topic
- **Service**: A communication pattern for request-response interactions
- **Action**: A communication pattern for long-running tasks with feedback
- **QoS (Quality of Service)**: Settings that define communication behavior
- **RMW (ROS Middleware)**: The interface between ROS 2 and underlying middleware

## Summary

ROS 2 provides a comprehensive framework for robot control systems, offering flexible communication patterns, robust tooling, and features designed for real-world applications. Its architecture enables the development of complex, distributed robot systems where different components can communicate effectively while maintaining modularity and maintainability.

Understanding these fundamentals is essential for developing robot control systems that leverage the power of ROS 2's architecture and ecosystem.

---

*Continue to [Robot Control Architecture](control-architecture.md) to explore different approaches to organizing robot control systems.*