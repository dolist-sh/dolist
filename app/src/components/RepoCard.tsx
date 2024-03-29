import * as React from 'react';
import { Repo } from '../types';

interface RepoCardProps {
  repository: Repo;
  isMonitored: boolean;
  isSelected: boolean;
  githubLogoUri: string;
  selectHandler: (repo: Repo) => void;
}

const RepoCard: React.FC<RepoCardProps> = ({
  repository,
  githubLogoUri,
  selectHandler,
  isSelected,
  isMonitored,
}: RepoCardProps) => {
  return (
    <div className="flex flex-row justify-between w-[97%] h-auto border-[0.5px] border-dolist-lightgray rounded m-auto mt-1 mb-2 p-2 bg-dolist-cream dark:bg-dolist-darkblue">
      <div className="flex flex-row pl-2 pr-2 justify-start">
        <img src={githubLogoUri} className="w-6 h-6" />
        <p className="font-std font-bold text-[12px] text-black dark:text-white pl-2 self-center">
          {repository.fullName}
        </p>
      </div>
      <div className="flex flex-row self-center mr-2">
        <input
          type="checkbox"
          disabled={isMonitored == true ? true : false}
          checked={isMonitored == true ? true : isSelected}
          onChange={() => selectHandler(repository)}
          className={`bg-transparent h-4 w-4  ${
            isMonitored ? 'text-dolist-gray' : 'text-dolist-green'
          } border-[0.5px] border-dolist-lightgray self-center rounded-[2px]`}
        />
      </div>
    </div>
  );
};

export default RepoCard;
