import React from 'react';
import type { NextPage } from 'next';
import { DayPlanView, TaskArea } from '../components';

const Homepage: NextPage = () => {
  return (
    <div className="flex flex-row justify-between h-screen">
      <div className="basis-2/12 border-2 border-black">Menu area</div>
      <div className="basis-10/12">
        <div className="block overflow-hidden">
          <div className="h-4/12 p-6 border border-black">header</div>
          <div className="h-6/12 p-4 border border-black inline-flex flex-row w-full">
            <div className="w-1/2 h-[440px] mt-6 mb-6 mr-4 overflow-hidden border-2 border-black">
              <DayPlanView />
            </div>
            <div className="w-1/2 h-[440px] mt-6 mr-4 overflow-hidden border-2 border-black">
              <TaskArea />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
