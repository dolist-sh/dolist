import React from 'react';
import type { NextPage } from 'next';
import { TaskCard } from '../components';

//import json_data from '../.data/output-2022-7-18-1658164458.json';

const TaskListPage: NextPage = () => {
  const json_data = [];

  return (
    <div className="flex flex-col w-11/12 m-auto">
      {json_data.map((comment, index) => (
        <TaskCard
          key={index}
          type={comment.type}
          title={comment.title}
          commentStyle={comment.commentStyle}
          fullComment={comment.fullComment}
          path={comment.path}
          lineNumber={comment.lineNumber}
        />
      ))}
    </div>
  );
};

export default TaskListPage;
