import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { RepoCard } from '../../src/components';

describe('Snapshot testing of RepoCard component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<RepoCard name="test" fullName="test/yunjae" />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
