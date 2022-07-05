import * as React from 'react';
import HelloWorld from '../hello-world';
import { shallow } from 'enzyme';

describe('Snapshot testing of HelloWorld component', () => {
  test('renders correctly', () => {
    const tree = shallow(<HelloWorld />);
    expect(tree).toMatchSnapshot();
  });
});
