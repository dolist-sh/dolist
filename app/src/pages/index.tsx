import React from 'react';
import type { NextPage } from 'next';
import { DayPlanView } from '../components';

const Homepage: NextPage = () => {
  return (
    <div className="flex flex-row h-screen">
      <div className="basis-1/4 border-2 border-black">Menu area</div>
      <div className="basis-1/2">
        <DayPlanView />
      </div>
      <div className="basis-1/4 border-2 border-black">Task area</div>
    </div>
  );
};

export default Homepage;
