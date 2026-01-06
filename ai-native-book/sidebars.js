// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'index',
    'chatbot-integration',
    {
      type: 'category',
      label: 'Chapter 1 - Introduction to Physical AI',
      items: [
        'chapter1/index',
        'chapter1/concepts',
        'chapter1/history',
        'chapter1/comparison',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2 - Embodied Intelligence and Humanoid Robotics',
      items: [
        'chapter2/index',
        'chapter2/embodied-foundations',
        'chapter2/humanoid-design',
        'chapter2/applications',
        'chapter2/challenges',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3 - Sensors and Actuators in Physical AI',
      items: [
        'chapter3/index',
        'chapter3/sensor-fundamentals',
        'chapter3/actuator-technologies',
        'chapter3/integration',
        'chapter3/applications',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4 - ROS 2 and Robot Control Systems',
      items: [
        'chapter4/index',
        'chapter4/ros2-fundamentals',
        'chapter4/control-architecture',
        'chapter4/integration',
        'chapter4/applications',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5 - AI Perception and Action Integration',
      items: [
        'chapter5/index',
        'chapter5/perception-action-loop',
        'chapter5/sensor-integration',
        'chapter5/ai-perception',
        'chapter5/action-systems',
        'chapter5/integration-architectures',
        'chapter5/case-studies',
        'chapter5/challenges-future',
      ],
    },
  ],
};

module.exports = sidebars;