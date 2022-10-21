import React, { useEffect, useContext } from 'react';
import { GlobalContext } from '../contexts/global';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Layout, TaskCard } from '../components';
import { useLayoutProps } from '../hooks';

const ReportPage: NextPage = () => {
  const layoutProps = useLayoutProps();
  const { state } = useContext(GlobalContext);
  const { push } = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    !token ? push('/signin') : null;
  }, []);

  return (
    <Layout {...layoutProps}>
      <div className="flex flex-row w-[80%] m-auto mt-7 pl-6 pr-6 justify-evenly">
        <div className="flex flex-row w-1/2">
          <img src={layoutProps.githubLogoUri} className="w-9 h-9 self-center mr-3" />
          <div className="flex flex-col">
            <h4 className="font-std font-bold text-[14px] text-black dark:text-dolist-cream">{'whathekcer/api'}</h4>
            <p className="font-std font-bold text-[10px] text-dolist-gray dark:text-dolist-cream">
              {`branch: `}
              <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">{'main'}</span>
            </p>
          </div>
        </div>
        <div className="flex flex-row-reverse w-1/2">
          <p className="text-[11px] font-std font-bold text-right text-dolist-gray dark:text-dolist-cream">
            {`from last commit: `}
            <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">{'--'}</span>
          </p>
        </div>
      </div>
      <div className="flex flex-col w-[76%] m-auto mt-9 border-b border-dolist-lightgray dark:border-dolist-cream">
        <div className="flex flex-row pl-2 pb-2">
          <p className="cursor-pointer text-xs font-std font-bold text-dolist-gray dark:text-dolist-cream pr-6">{`Total (20)`}</p>
          <p className="cursor-pointer text-xs font-std hover:font-bold text-dolist-gray dark:text-dolist-cream pr-6">{`New (2)`}</p>
          <p className="cursor-pointer text-xs font-std hover:font-bold text-dolist-gray dark:text-dolist-cream pr-6">{`Resolved (5)`}</p>
          <p className="cursor-pointer text-xs font-std hover:font-bold text-dolist-gray dark:text-dolist-cream pr-6">{`Old (15)`}</p>
        </div>
      </div>
      <div className="flex flex-col w-[76%] m-auto mt-9 border-b border-dolist-lightgray dark:border-dolist-cream">
        <TaskCard
          theme={state.theme}
          title="Hello Worlld"
          commentStyle="oneline"
          type="TODO"
          fullComment={['Hello World']}
          path="src/example.ts"
          lineNumber={20}
        />
      </div>
    </Layout>
  );
};

export default ReportPage;
