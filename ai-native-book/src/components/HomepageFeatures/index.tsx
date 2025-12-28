import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'ROS 2 Integration',
    Svg: require('@site/static/img/ros.svg').default,
    description: (
      <>
        Comprehensive coverage of ROS 2 concepts, architecture, and practical applications
        for robotics development and control systems.
      </>
    ),
  },
  {
    title: 'Physical AI Concepts',
    Svg: require('@site/static/img/embo.svg').default,
    description: (
      <>
        Deep dive into the intersection of artificial intelligence and physical systems,
        including perception, reasoning, and control algorithms.
      </>
    ),
  },
  {
    title: 'Embodied Intelligence',
    Svg: require('@site/static/img/phai.svg').default,
    description: (
      <>
        Explore how AI systems can be embodied in physical robots, enabling real-world
        interaction and autonomous decision-making.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.featureItem)}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
