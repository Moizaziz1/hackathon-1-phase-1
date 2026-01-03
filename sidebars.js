// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    'index',
    {
      type: 'category',
      label: 'Modules',
      items: [
        {
          type: 'category',
          label: 'ROS 2 Fundamentals',
          items: [
            'modules/ros2-fundamentals/index',
            'modules/ros2-fundamentals/concepts',
            {
              type: 'category',
              label: 'Hands-on Labs',
              items: [
                'modules/ros2-fundamentals/hands-on-labs/lab-1',
              ],
            },
            'modules/ros2-fundamentals/resources',
          ],
        },
        {
          type: 'category',
          label: 'Simulation & Digital Twins',
          items: [
            'modules/simulation-digital-twins/index',
            'modules/simulation-digital-twins/concepts',
            {
              type: 'category',
              label: 'Hands-on Labs',
              items: [
                'modules/simulation-digital-twins/hands-on-labs/lab-1',
              ],
            },
            'modules/simulation-digital-twins/resources',
          ],
        },
        {
          type: 'category',
          label: 'AI Perception & Navigation',
          items: [
            'modules/ai-perception-navigation/index',
            'modules/ai-perception-navigation/concepts',
            {
              type: 'category',
              label: 'Hands-on Labs',
              items: [
                'modules/ai-perception-navigation/hands-on-labs/lab-1',
              ],
            },
            'modules/ai-perception-navigation/resources',
          ],
        },
        {
          type: 'category',
          label: 'Vision-Language-Action Systems',
          items: [
            'modules/vision-language-action/index',
            'modules/vision-language-action/concepts',
            {
              type: 'category',
              label: 'Hands-on Labs',
              items: [
                'modules/vision-language-action/hands-on-labs/lab-1',
              ],
            },
            'modules/vision-language-action/resources',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: [
        'capstone-project/index',
        'capstone-project/requirements',
        'capstone-project/system-architecture',
        'capstone-project/implementation-guide',
        'capstone-project/validation',
      ],
    },
    {
      type: 'category',
      label: 'Tutorials',
      items: [
        'tutorials/setup-guide',
      ],
    },
  ],
};

export default sidebars;