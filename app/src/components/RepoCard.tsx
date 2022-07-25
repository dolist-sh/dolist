import * as React from 'react';

interface RepoCardProps {
  name: string;
  fullName: string;
}

const RepoCard: React.FC<RepoCardProps> = ({ name, fullName }: RepoCardProps) => {
  const clickHandler = (event) => {
    event.preventDefault();
    window.location.assign(`/tasklist/?repo=${fullName}`);
  };

  return (
    <div className="w-[680px] h-auto border-0 border-dolist-lightgray rounded m-auto mt-4 mb-4 p-4 bg-dolist-cream">
      <div className="flex felx-row justify-between pl-2 pr-2">
        <p>{name}</p>
        <button
          type="button"
          onClick={clickHandler}
          className="inline-flex items-center px-6 py-3 border border-transparent font-small text-xs rounded shadow-sm text-white bg-dolist-darkblue focus:outline-none focus:ring-2 focus:ring-offset-2 focus:dolist-brown"
        >
          Track tasks
        </button>
      </div>
    </div>
  );
};

export default RepoCard;
