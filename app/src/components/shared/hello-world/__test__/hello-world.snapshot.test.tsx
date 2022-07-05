import * as React from 'react';
import * as renderer from 'react-test-renderer';
import HelloWorld from '../hello-world';

describe('Snapshot testing of HelloWorld component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<HelloWorld />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
