import * as React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { nightOwl, oneLight } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import { getLanguage } from '../utils';

interface TaskCardProps {
  theme: string;
  title: string;
  commentStyle: string;
  type: string;
  status: string;
  fullComment: string[];
  path: string;
  lineNumber: number;
}

const TaskCard: React.FC<TaskCardProps> = ({
  theme,
  title,
  type,
  status,
  fullComment,
  path,
  lineNumber,
}: TaskCardProps) => {
  const codeStrings = fullComment.join('');
  const language = getLanguage(path);

  function getStatusColor(status: string): string | null {
    let result = null;

    status === 'New' ? (result = 'text-orange-600') : null;
    status === 'Old' ? (result = 'text-red-600') : null;
    return result;
  }

  return (
    <div className="w-[97%] h-auto m-auto mt-4 mb-4 bg-dolist-cream dark:bg-dolist-darkblue border-[0.5px] border-black dark:border-dolist-cream rounded">
      <div className="w-[92%] h-full m-auto pt-5 pb-5">
        <div className="relative pt-4 pb-3 border-b border-dolist-lightgray dark:border-dolist-cream">
          {status === 'New' || status === 'Old' ? (
            <p className={`absolute text-base text-[9px] top-[-1.5px] ${getStatusColor(status)}`}>{status}</p>
          ) : null}
          <h3 className="text-base font-bold text-black dark:text-white">{`${title}`}</h3>
          <p className="text-[11px] pl-[1px] pt-1 text-dolist-gray dark:text-dolist-cream">{`Type: ${type}`}</p>
        </div>
      </div>
      <div className="flex flex-row w-[92%] h-full m-auto pt-3 pb-3 mb-9 border-b border-dolist-lightgray dark:border-dolist-cream">
        <div className="flex flex-col w-1/2 h-200px">
          <div className="pb-3">
            {/** TODO: fix multiline highlighting issue */}
            <SyntaxHighlighter
              showLineNumbers
              wrapLongLines
              startingLineNumber={lineNumber}
              language={language}
              style={theme === 'dark' ? oneLight : nightOwl}
            >
              {codeStrings}
            </SyntaxHighlighter>
          </div>
          <div>
            <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">{'Note'}</p>
            <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{'--'}</p>
          </div>
        </div>
        <div className="flex flex-col w-1/2 h-200px ml-5">
          <div className="flex flex-row w-full m-auto">
            <div className="w-[32%] ml-[0.5%] mr-[0.5%]">
              <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">{'File Path'}</p>
              <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{path}</p>
            </div>
            <div className="w-[32%] ml-[0.5%] mr-[0.5%]">
              <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">
                {'Appeared in Commit'}
              </p>
              <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{'85bdeb1'}</p>
            </div>
            <div className="w-[32%] ml-[0.5%] mr-[0.5%]">
              <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">{'Created by'}</p>
              <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{'Yunjae Oh'}</p>
            </div>
          </div>
          <div className="flex flex-row w-full m-auto">
            <div className="w-[32%] ml-[0.5%] mr-[0.5%]">
              <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">
                {'Linked Ticket'}
              </p>
              <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{'--'}</p>
            </div>
            <div className="w-[32%] ml-[0.5%] mr-[0.5%]">
              <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">
                {'Resolved in Commit'}
              </p>
              <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{'--'}</p>
            </div>
            <div className="w-[32%] ml-[0.5%] mr-[0.5%]">
              <p className="font-std font-bold text-[12px] text-dolist-gray dark:text-dolist-cream">{'Resolved by'}</p>
              <p className="font-std text-[11px] text-dolist-gray dark:text-dolist-cream">{'--'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
