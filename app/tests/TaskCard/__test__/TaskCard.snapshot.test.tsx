import * as React from 'react';
import * as renderer from 'react-test-renderer';
import { TaskCard } from '../../../src/components';

describe('Snapshot testing of TaskCard component', () => {
  const testData = {
    theme: 'dark',
    type: 'TODO',
    commentStyle: 'oneline',
    title: 'This should be parsed',
    status: 'New',
    fullComment: ['// TODO: This should be parsed'],
    path: '/Users/yunjae/Desktop/engineering/comment-parser/input/folder_b/folder_b.ts',
    lineNumber: 1,
  };

  test('renders correctly', () => {
    const component = renderer.create(
      <TaskCard
        theme={testData.theme}
        type={testData.type}
        title={testData.title}
        status={testData.status}
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
