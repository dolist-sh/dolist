import React from 'react';
import type { NextPage } from 'next';

const DashboardPage: NextPage = () => {
  return (
    <div className="flex flex-col w-full h-screen justify-start content-center">
      <div className="w-full h-[90px] border-b-[0.5px] border-dolist-lightgray dark:border-dolist-cream">
        <header className="flex flex-row w-5/6 h-full m-auto mt-0 mb-0 p-2">Header Area</header>
      </div>
      <div className="w-full h-1/4 mt-14 mb-5">
        <div className="w-5/6 h-full m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Start monitoring the repositories`}</h2>
          <div className="flex flex-row h-auto mt-5 justify-evenly border-2">
            <button>{`GH btn`}</button>
            <button>{`GL btn`}</button>
            <button>{`BicBucket BTN`}</button>
          </div>
        </div>
      </div>
      <div className="w-full h-2/4">
        <div className="w-5/6 h-full m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Monitored repositroies`}</h2>
          <div className="flex flex-row h-auto mt-5 justify-evenly border-2">
            <div>{`Repo 1`}</div>
            <div>{`Repo 2`}</div>
            <div>{`Repo 3`}</div>
            <div>{`Repo 4`}</div>
            <div>{`Repo 5`}</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
