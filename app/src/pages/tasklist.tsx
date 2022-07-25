import React, { useEffect } from 'react';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { TaskCard } from '../components';
import { getRepoTasks } from '../api';

//import json_data from '../.data/output-2022-7-18-1658164458.json';

const TaskListPage: NextPage = () => {
  const { query } = useRouter();
  const json_data = [];

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (query.repo) {
      getRepoTasks(token, query.repo as string).then((data) => {
        console.log(data);
      });
    }
  }, [query]);

  return (
    <div className="flex flex-col w-11/12 m-auto">
      <h1>Welcome to DoList.sh</h1>
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
