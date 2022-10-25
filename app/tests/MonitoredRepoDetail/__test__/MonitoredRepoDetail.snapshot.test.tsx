import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { MonitoredRepoDetail } from '../../../src/components';
import { MonitoredRepo } from '../../../src/types';

describe('Snapshot testing of MonitoredRepoDetail component', () => {
  const testData = {
    theme: 'dark',
    repo: {
      createdAt: 1664701600,
      defaultBranch: 'main',
      fullName: 'whathecker/assignment-restapi',
      id: 'f5e6ce58-636f-4cc9-b150-46754e70cd46',
      language: 'Python',
      lastCommit: 'bfae0103c24a05e8d77601bad8bf647b2500663f',
      lastUpdated: 1666007886,
      name: 'assignment-restapi',
      parsedComments: [],
      provider: 'github',
      status: 'active',
      userId: '68202eee-a8b5-4348-a146-55cef2c2bb52',
      visibility: 'public',
    } as MonitoredRepo,
    githubLogoUri: 'http://awesomelogo',
  };

  test('renders correctly', () => {
    const component = renderer.create(
      <MonitoredRepoDetail theme={testData.theme} repo={testData.repo} githubLogoUri={testData.githubLogoUri} />,
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
