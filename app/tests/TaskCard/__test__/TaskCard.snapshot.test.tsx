import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { TaskCard } from '../../../src/components';

describe('Snapshot testing of TaskCard component', () => {
  const testData = {
    type: 'TODO',
    commentStyle: 'oneline',
    title: 'This should be parsed',
    fullComment: ['// TODO: This should be parsed'],
    path: '/Users/yunjae/Desktop/engineering/comment-parser/input/folder_b/folder_b.ts',
    lineNumber: 1,
  };

  test('renders correctly', () => {
    const component = renderer.create(
      <TaskCard
        type={testData.type}
        title={testData.title}
        commentStyle={testData.commentStyle}
        fullComment={testData.fullComment}
        path={testData.path}
        lineNumber={testData.lineNumber}
      />,
    );
    const tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });
});
