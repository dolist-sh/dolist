import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { DayPlanView } from '../../src/components';

describe('Snapshot testing of DayPlanView component', () => {
  test('renders correctly', () => {
    const component = renderer.create(<DayPlanView />);
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
