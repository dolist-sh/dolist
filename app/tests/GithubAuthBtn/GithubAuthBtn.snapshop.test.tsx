import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { GithubAuthBtn } from '../../src/components';

describe('Snapshot testing of GithubAuthBtn component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<GithubAuthBtn oauthUri="http://test.oauth" logoUri="/images/logo.png" />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
