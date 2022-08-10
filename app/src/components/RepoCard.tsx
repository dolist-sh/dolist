import * as React from 'react';

interface RepoCardProps {
  //name: string;
  fullName: string;
  //branch: string;
  githubLogoUri: string;
}

const RepoCard: React.FC<RepoCardProps> = ({ fullName, githubLogoUri }: RepoCardProps) => {
  return (
    <div className="w-[97%] h-auto border-[0.5px] border-dolist-lightgray dark:border-dolist-cream rounded m-auto mt-1 mb-2 p-2 bg-dolist-cream dark:bg-dolist-darkblue">
      <div className="flex felx-row pl-2 pr-2">
        <img src={githubLogoUri} className="w-6 h-6" />
        <p className="font-std font-bold text-[12px] text-black dark:text-white pl-2 self-center">{fullName}</p>
      </div>
    </div>
  );
};

export default RepoCard;
