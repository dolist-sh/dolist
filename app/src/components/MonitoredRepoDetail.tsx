import * as React from 'react';
import { TaskCard } from '../components';
import { getShortSha1 } from '../utils';
import { MonitoredRepo } from '../types';

interface MonitoredRepoDetailProps {
  theme: string;
  repo: MonitoredRepo;
  githubLogoUri: string;
}

const MonitoredRepoDetail: React.FC<MonitoredRepoDetailProps> = ({
  theme,
  repo,
  githubLogoUri,
}: MonitoredRepoDetailProps) => {
  return (
    <>
      <div className="flex flex-row w-[80%] m-auto mt-7 pl-6 pr-6 justify-evenly">
        <div className="flex flex-row w-1/2">
          <img src={githubLogoUri} className="w-9 h-9 self-center mr-3" />
          <div className="flex flex-col">
            <h4 className="font-std font-bold text-[14px] text-black dark:text-dolist-cream">
              {repo ? repo.fullName : '--'}
            </h4>
            <p className="font-std font-bold text-[10px] text-dolist-gray dark:text-dolist-cream">
              {`branch: `}
              <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">
                {repo ? repo.defaultBranch : '--'}
              </span>
            </p>
          </div>
        </div>
        <div className="flex flex-row-reverse w-1/2">
          <p className="text-[11px] font-std font-bold text-right text-dolist-gray dark:text-dolist-cream">
            {`from last commit: `}
            <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">
              {repo && repo.lastCommit ? getShortSha1(repo.lastCommit) : '--'}
            </span>
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
      <div className="flex flex-col w-[76%] m-auto mt-9">
        {repo
          ? repo.parsedComments.map((comment, index) => {
              return (
                <TaskCard
                  key={index}
                  theme={theme}
                  title={comment.title}
                  commentStyle={comment.commentStyle}
                  type={comment.type}
                  fullComment={comment.fullComment}
                  path={comment.filePath}
                  lineNumber={comment.lineNumber}
                />
              );
            })
          : null}
      </div>
    </>
  );
};

export default MonitoredRepoDetail;
