import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { RepoOverview } from '../../../src/components';

describe('Snapshot testing of ColorThemeBtn component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<RepoOverview githubLogoUri="/images/logo.png" />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
