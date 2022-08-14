import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { RepoCard } from '../../../src/components';
import { Repo } from '../../../src/types';

describe('Snapshot testing of RepoCard component', () => {
  test('renders correctly', () => {
    const repo: Repo = {
      id: 120345,
      name: 'test',
      fullName: '/user/test',
      defaultBranch: 'main',
      language: 'javascript',
      url: 'https://test-uri.com',
      provider: 'github',
      visibility: 'private',
    };

    const componentNotSelectedState = renderer.create(
      <RepoCard
        selectHandler={() => {
          return;
        }}
        isSelected={false}
        repository={repo}
        githubLogoUri="/images/github.png"
      />,
    );

    const componentSelectedState = renderer.create(
      <RepoCard
        selectHandler={() => {
          return;
        }}
        isSelected={true}
        repository={repo}
        githubLogoUri="/images/github.png"
      />,
    );

    const treeNotSelectedState = componentNotSelectedState.toJSON();
    const treeSelectedState = componentSelectedState.toJSON();

    expect(treeNotSelectedState).toMatchSnapshot();
    expect(treeSelectedState).toMatchSnapshot();
  });
});
