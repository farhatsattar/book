// @ts-check
// `@type` JSDoc annotations allow IDEs and type-checking tools to autocomplete
// and validate type definitions, parameters, and return values.

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics TextBook',
  tagline: 'An AI-Native Textbook with RAG Integration',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/ai-native-book/',

  // GitHub pages deployment config.
  organizationName: 'farhatsattar', // Usually your GitHub org/user name.
  projectName: 'ai-native-book', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  markdown: {
    format: 'detect',
    mermaid: true,
  },
  onBrokenMarkdownImages: 'warn', // Handle broken images by warning instead of throwing errors

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-username/ai-native-book/tree/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics TextBook`,
          },
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            to: '/docs/chapter1',
            label: 'Chapters',
            position: 'left',
          },
          {
            to: '/blog',
            label: 'Blog',
            position: 'left',
          },
          {
            href: 'https://github.com/your-username/ai-native-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              {
                label: 'Chapter 1 - Introduction to Physical AI',
                to: '/docs/chapter1',
              },
              {
                label: 'Chapter 2 - Embodied Intelligence and Humanoid Robotics',
                to: '/docs/chapter2',
              },
              {
                label: 'Chapter 3 - Sensors and Actuators in Physical AI',
                to: '/docs/chapter3',
              },
              {
                label: 'Chapter 4 - ROS 2 and Robot Control Systems',
                to: '/docs/chapter4',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'ROS 2 Documentation',
                href: 'https://docs.ros.org/',
              },
              {
                label: 'Docusaurus',
                href: 'https://docusaurus.io',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-username/ai-native-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics — Essentials. Built with Docusaurus.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
    }),
};

module.exports = config;