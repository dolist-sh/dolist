import React from 'react';
import type { NextPage } from 'next';
import { TaskCard } from '../components';

const Homepage: NextPage = () => {
  return (
    <div className="flex flex-col w-11/12 m-auto">
      <TaskCard />
    </div>
  );
};

export default Homepage;
