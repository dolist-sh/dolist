import * as React from 'react';

interface RepoCardProps {
  name: string;
}

const RepoCard: React.FC<RepoCardProps> = ({ name }: RepoCardProps) => {
  return (
    <div className="w-[680px] h-auto border-0 border-dolist-lightgray rounded m-auto mt-4 mb-4 p-4 bg-dolist-cream">
      <div className="flex felx-row justify-between pl-2 pr-2">
        <p>{name}</p>
        <button>Track tasks</button>
      </div>
    </div>
  );
};

export default RepoCard;
