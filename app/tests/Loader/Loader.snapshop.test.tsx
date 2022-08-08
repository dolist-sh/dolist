import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { Loader } from '../../src/components';

describe('Snapshot testing of Loader component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<Loader loaderColor="#E8E7E0" />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
