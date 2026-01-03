import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Physical AI',
    Svg: require('@site/static/img/robot.svg').default,
    description: (
      <>
        Learn about the fundamentals of Physical AI and how it enables robots to interact with the real world.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    Svg: require('@site/static/img/humanoid.svg').default,
    description: (
      <>
        Explore the design, control, and implementation of humanoid robots for various applications.
      </>
    ),
  },
  {
    title: 'Embodied Intelligence',
    Svg: require('@site/static/img/brain.svg').default,
    description: (
      <>
        Discover how robots can develop intelligence through physical interaction with their environment.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
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

export default function HomepageFeatures() {
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