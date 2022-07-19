import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { TaskCard } from '../../src/components';

describe('Snapshot testing of TaskCard component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<TaskCard />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
