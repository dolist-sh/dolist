import * as React from 'react';
import Link from 'next/link';
import { useCommentsPerType } from '../hooks';
import { getShortSha1 } from '../utils';
import { MonitoredRepo } from '../types';

interface MonitoredRepoOverviewProps {
  githubLogoUri: string;
  mrepo: MonitoredRepo;
}

const MonitoredRepoOverview: React.FC<MonitoredRepoOverviewProps> = ({
  githubLogoUri,
  mrepo,
}: MonitoredRepoOverviewProps) => {
  /**
   *
   * @param input: Unix timestamp
   * @returns string representation of the timestamp
   */
  function getReadableTime(timestamp: number): string {
    const months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ];

    const dateObj = new Date(timestamp * 1000); //JavaScript counts epoch in Milliseconds

    const year = dateObj.getFullYear();
    const month = months[dateObj.getMonth()];
    const date = dateObj.getDate();
    const minute = dateObj.getMinutes();
    const hour = dateObj.getHours();

    return `${hour < 10 ? `0${hour}` : hour}:${minute < 10 ? `0${minute}` : minute}, ${month} ${date}, ${year}`;
  }

  const filteredComments = useCommentsPerType(mrepo);

  return (
    <div className="flex flex-col w-[45%] h-[200px] p-3 pl-2 pr-2 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-dashed border-black dark:border-dolist-cream rounded">
      <div className="flex flex-row w-[95%] h-1/4 m-auto justify-evenly">
        <div className="flex flex-row w-1/2">
          <img src={githubLogoUri} className="w-7 h-7 self-center mr-1" />
          <div className="flex flex-col">
            <h4 className="font-std font-bold text-[12px] text-black dark:text-dolist-cream">{mrepo.fullName}</h4>
            <p className="font-std font-bold text-[8.5px] text-dolist-gray dark:text-dolist-cream">
              {`branch: `}
              <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">
                {mrepo.defaultBranch}
              </span>
            </p>
          </div>
        </div>
        <div className="w-1/2 mt-1">
          <p className="text-[8.5px] font-std font-bold text-right text-dolist-gray dark:text-dolist-cream">
            {`from last commit: `}
            <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">
              {mrepo.lastCommit ? getShortSha1(mrepo.lastCommit) : '--'}
            </span>
          </p>
        </div>
      </div>
      <div className="flex flex-col pt-7 pl-6 pr-6">
        <h4 className="font-std font-bold text-dolist-gray dark:text-dolist-cream text-[11px]">{`To-Do Report`}</h4>
        <div className="flex flex-row mt-2 justify-between ml-1 mr-1">
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Total`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">
              {mrepo.parsedComments.length > 0 ? mrepo.parsedComments.length : '--'}
            </p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`New`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">
              {filteredComments.newComments.length > 0 ? filteredComments.newComments.length : '--'}
            </p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Resolved`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">
              {filteredComments.resolvedComments.length > 0 ? filteredComments.resolvedComments.length : '--'}
            </p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Old`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">
              {filteredComments.oldComments.length > 0 ? filteredComments.oldComments.length : '--'}
            </p>
          </div>
        </div>
      </div>
      <div className="flex flex-row pt-10 ml-3 mr-3 justify-evenly">
        <Link href={`/report/${mrepo.id}`}>
          <a className="w-1/2 font-std font-bold text-[9px] text-dolist-darkblue dark:text-white underline">{`view full report`}</a>
        </Link>
        <p className="w-1/2 font-std font-bold text-[9px] text-dolist-gray dark:text-white text-right">
          {`updated at: `}
          <span className="font-std text-[8px] text-dolist-lightgray dark:text-dolist-cream">
            {mrepo.lastUpdated ? getReadableTime(mrepo.lastUpdated) : '--'}
          </span>
        </p>
      </div>
    </div>
  );
};

export default MonitoredRepoOverview;
