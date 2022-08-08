import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { ColorThemeBtn } from '../../src/components';

describe('Snapshot testing of ColorThemeBtn component', () => {
  test('renders correctly', () => {
    const component = renderer.create(
      <ColorThemeBtn
        clickHandler={() => {
          return;
        }}
        currentTheme="dark"
        colorThemeIconUri="/images/nightmode.png"
      />,
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
