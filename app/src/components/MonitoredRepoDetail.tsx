import * as React from 'react';
import { useState, useEffect } from 'react';
import { TaskCard } from '../components';
import { useCommentsPerType } from '../hooks';
import { getShortSha1 } from '../utils';
import { MonitoredRepo, ParsedComment } from '../types';

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
  const filteredCommments = useCommentsPerType(repo);

  const [selectedFilter, setSelectedFilter] = useState<'total' | 'new' | 'resolved' | 'old'>('total');
  const [commentList, setCommentList] = useState<ParsedComment[]>(repo.parsedComments);

  const filterClickHandler = (event): void => {
    event.preventDefault();
    setSelectedFilter(event.target.getAttribute('data-filter-type'));
  };

  useEffect(() => {
    selectedFilter === 'total' ? setCommentList(repo.parsedComments) : null;
    selectedFilter === 'new' ? setCommentList(filteredCommments.newComments) : null;
    selectedFilter === 'resolved' ? setCommentList(filteredCommments.resolvedComments) : null;
    selectedFilter === 'old' ? setCommentList(filteredCommments.oldComments) : null;
  }, [selectedFilter]);

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
          <a
            className={`cursor-pointer text-xs font-std text-dolist-gray dark:text-dolist-cream pr-6 ${
              selectedFilter === 'total' ? 'font-bold' : null
            }`}
            data-filter-type="total"
            onClick={filterClickHandler}
          >{`Total ${repo.parsedComments.length}`}</a>
          <a
            className={`cursor-pointer text-xs font-std text-dolist-gray dark:text-dolist-cream pr-6 ${
              selectedFilter === 'new' ? 'font-bold' : null
            }`}
            data-filter-type="new"
            onClick={filterClickHandler}
          >{`New ${filteredCommments.newComments.length}`}</a>
          <a
            className={`cursor-pointer text-xs font-std text-dolist-gray dark:text-dolist-cream pr-6 ${
              selectedFilter === 'resolved' ? 'font-bold' : null
            }`}
            data-filter-type="resolved"
            onClick={filterClickHandler}
          >{`Resolved ${filteredCommments.resolvedComments.length}`}</a>
          <a
            className={`cursor-pointer text-xs font-std text-dolist-gray dark:text-dolist-cream pr-6 ${
              selectedFilter === 'old' ? 'font-bold' : null
            }`}
            data-filter-type="old"
            onClick={filterClickHandler}
          >{`Old ${filteredCommments.oldComments.length}`}</a>
        </div>
      </div>
      <div className="flex flex-col w-[76%] m-auto mt-9">
        {repo
          ? commentList.map((comment, index) => {
              return (
                <TaskCard
                  key={index}
                  theme={theme}
                  title={comment.title}
                  status={comment.status}
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
