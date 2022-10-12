import * as React from 'react';

interface RepoOverviewProps {
  githubLogoUri: string;
}

const RepoOverview: React.FC<RepoOverviewProps> = ({ githubLogoUri }: RepoOverviewProps) => {
  return (
    <div className="flex flex-col w-[30%] h-full p-3 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-dashed border-black dark:border-dolist-cream rounded">
      <div className="flex flex-row w-full h-1/4 justify-evenly">
        <div className="flex flex-row w-1/2">
          <img src={githubLogoUri} className="w-7 h-7 self-center mr-1" />
          <div className="flex flex-col">
            <h4 className="font-std font-bold text-[12px] text-black dark:text-dolist-cream">{`whathecker/api`}</h4>
            <p className="font-std font-bold text-[8.5px] text-dolist-gray dark:text-dolist-cream">
              {`branch: `}
              <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">{`main`}</span>
            </p>
          </div>
        </div>
        <div className="w-1/2 mt-1">
          <p className="text-[8.5px] font-std font-bold text-right text-dolist-gray dark:text-dolist-cream">
            {`from last commit: `}
            <span className="font-std font-bold underline text-dolist-darkblue dark:text-white">{`694949`}</span>
          </p>
        </div>
      </div>
      <div className="flex flex-col pt-5 ml-2 mr-2">
        <h4 className="font-std font-bold text-dolist-gray dark:text-dolist-cream text-[11px]">{`To-Do Report`}</h4>
        <div className="flex flex-row mt-2 justify-between ml-1 mr-1">
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Total`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`20`}</p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`New`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`2`}</p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Resolved`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`3`}</p>
          </div>
          <div className="flex flex-col">
            <h4 className="font-std text-dolist-gray dark:text-dolist-cream text-[11px] text-center">{`Old`}</h4>
            <p className="font-std font-bold text-black dark:text-white text-[11px] text-center underline">{`15`}</p>
          </div>
        </div>
      </div>
      <div className="flex flex-row pt-5 ml-2 mr-2 justify-evenly">
        <a className="w-1/2 font-std font-bold text-[10px] text-dolist-darkblue dark:text-white underline">{`view full report`}</a>
        <p className="w-1/2 font-std font-bold text-[10px] text-dolist-gray dark:text-white text-right">
          {`updated at: `}
          <span className="font-std text-[10px] text-dolist-lightgray dark:text-dolist-cream">{`--`}</span>
        </p>
      </div>
    </div>
  );
};

export default RepoOverview;
