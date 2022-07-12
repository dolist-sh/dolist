import React from 'react';
import type { NextPage } from 'next';
import { DayPlanView, TaskArea } from '../components';

const Homepage: NextPage = () => {
  return (
    <div className="flex flex-row h-screen">
      <div className="basis-1/4 border-2 border-black">Menu area</div>
      <div className="basis-1/2">
        <DayPlanView />
      </div>
      <div className="basis-1/4">
        <TaskArea />
      </div>
    </div>
  );
};

export default Homepage;
