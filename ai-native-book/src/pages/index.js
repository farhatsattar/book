import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Reading - 5 min ⏱️
          </Link>
          <Link
            className="button button--outline button--lg"
            to="/docs/chapter1">
            Explore Chapters
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({ title, description, icon }) {
  return (
    <div className={clsx('col col--4', styles.featureCard)}>
      <div className={styles.featureCardInner}>
        <div className={styles.icon}>{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  const features = [
    {
      title: 'Physical AI Fundamentals',
      description: 'Learn the core concepts of embodied intelligence and physical AI systems.',
      icon: '🤖'
    },
    {
      title: 'Humanoid Robotics',
      description: 'Explore the design principles and implementation of humanoid robots.',
      icon: '🦾'
    },
    {
      title: 'AI Integration',
      description: 'Discover how AI systems integrate with physical robotics platforms.',
      icon: '🧠'
    }
  ];

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An AI-Native Textbook on Physical AI & Humanoid Robotics with RAG Integration">
      <HomepageHeader />
      <main>
        <section className={styles.featuresSection}>
          <div className="container">
            <div className="row">
              {features.map((feature, index) => (
                <FeatureCard
                  key={index}
                  title={feature.title}
                  description={feature.description}
                  icon={feature.icon}
                />
              ))}
            </div>
          </div>
        </section>

        <section className={styles.contentSection}>
          <div className="container">
            <div className="row">
              <div className="col col--6">
                <h2>Cutting-Edge Curriculum</h2>
                <p>
                  Our comprehensive textbook covers everything from theoretical foundations to
                  practical implementations in Physical AI and Humanoid Robotics. Each chapter
                  includes interactive elements and real-world applications.
                </p>
                <ul className={styles.bulletList}>
                  <li>Theoretical foundations of embodied intelligence</li>
                  <li>Practical implementation strategies</li>
                  <li>Case studies and real-world applications</li>
                  <li>Interactive learning elements</li>
                </ul>
              </div>
              <div className="col col--6">
                <div className={styles.card}>
                  <h3>AI-Powered Learning</h3>
                  <p>
                    Integrated RAG-powered chatbot provides instant answers to your questions,
                    making learning more interactive and efficient.
                  </p>
                  <div className={styles.botIcon}>💬</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}