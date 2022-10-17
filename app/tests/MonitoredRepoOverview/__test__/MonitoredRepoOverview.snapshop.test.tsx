import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { MonitoredRepoOverview } from '../../../src/components';
import { MonitoredRepo } from '../../../src/types';

describe('Snapshot testing of MonitoredRepoOverview component', () => {
  const mrepo: MonitoredRepo = {
    id: '0397827a-fda3-4149-ab8a-6dee5a6a0ca4',
    name: 'api',
    fullName: 'whathecker/api',
    defaultBranch: 'master',
    language: 'JavaScript',
    lastCommit: '8ef75d85b75ef3349e6e829bb28943cc88b0168b',
    userId: '68202eee-a8b5-4348-a146-55cef2c2bb52',
    provider: 'github',
    visibility: 'private',
    status: 'active',
    createdAt: 1666018951,
    lastUpdated: 1666018951,
    parsedComments: [],
  };

  test('renders correctly', () => {
    const component = renderer.create(<MonitoredRepoOverview mrepo={mrepo} githubLogoUri="/images/logo.png" />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
