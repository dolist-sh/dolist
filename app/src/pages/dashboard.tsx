import React, { useEffect, useState } from 'react';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Layout, AddRepoModal, MonitoredRepoOverview } from '../components';

import { getMonitoredRepos } from '../api';
import { useLayoutProps } from '../hooks';
import { MonitoredRepo } from '../types';

const DashboardPage: NextPage = () => {
  const { push } = useRouter();

  const layoutProps = useLayoutProps();
  const [modalOpenCounter, setModalOpenCounter] = useState(0);
  const [monitoredRepos, setMonitoredRepos] = useState<Array<MonitoredRepo[]>>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    !token
      ? push('/signin')
      : getMonitoredRepos(token).then((data) => {
          setMonitoredRepos(convertMreposToNestedArray(data));
        });
  }, []);

  const modalOpenHandler = (event: React.MouseEvent) => {
    event.preventDefault();
    const counter = modalOpenCounter + 1;
    setModalOpenCounter(counter);
  };

  function convertMreposToNestedArray(mrepos: MonitoredRepo[]): Array<MonitoredRepo[]> {
    const output = [];
    const remainder = mrepos.length % 2;

    for (let i = 0; i < mrepos.length - remainder; i += 2) {
      const nestedArr = [mrepos[i], mrepos[i + 1]];
      output.push(nestedArr);
    }

    if (remainder !== 0) {
      const nestedArr = [];
      for (let y = mrepos.length - remainder; y < mrepos.length; y++) {
        nestedArr.push(mrepos[y]);
      }
      output.push(nestedArr);
    }

    return output;
  }

  return (
    <Layout {...layoutProps}>
      <AddRepoModal githubLogoUri={layoutProps.githubLogoUri} openCounter={modalOpenCounter} />
      <div className="w-full h-1/4 pt-10 pb-5">
        <div className="w-5/6 h-full m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Start monitoring the repositories`}</h2>
          <div className="flex flex-row h-auto mt-5 ml-3 justify-start z-10">
            <button
              type="button"
              onClick={modalOpenHandler}
              className="flex flex-col w-[30%] h-full p-5 pt-7 pb-7 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-dashed border-black dark:border-dolist-cream rounded"
            >
              <div className="flex flex-col w-1/4 h-1/4 m-auto">
                <img src={layoutProps.addGithubLogoUri} className="w-7 h-7 ml-2 self-center" />
              </div>
              <p className="font-std font-bold text-xs text-black dark:text-dolist-cream pt-3">{`Monitor GitHub Repo`}</p>
            </button>
          </div>
        </div>
      </div>
      <div className="w-full h-3/4 pt-10 pb-5">
        <div className="w-5/6 min-h-full h-auto m-auto mt-0 mb-0">
          <h2 className="font-std font-bold text-black dark:text-dolist-cream">{`Monitored repositroies`}</h2>
          {monitoredRepos.map((nestedArr, index) => {
            return (
              <div key={index} className="flex flex-row h-auto mt-5 mb-5 ml-3 justify-evenly">
                {nestedArr.map((mrepo, index) => {
                  return <MonitoredRepoOverview mrepo={mrepo} key={index} githubLogoUri={layoutProps.githubLogoUri} />;
                })}
              </div>
            );
          })}
        </div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
