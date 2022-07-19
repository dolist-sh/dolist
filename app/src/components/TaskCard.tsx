import * as React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { nightOwl } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import { getLanguage } from '../utils';

interface TaskCardProps {
  title: string;
  commentStyle: string;
  type: string;
  fullComment: string[];
  path: string;
  lineNumber: number;
}

const TaskCard: React.FC<TaskCardProps> = ({ title, type, fullComment, path, lineNumber }: TaskCardProps) => {
  const codeStrings = fullComment.join('\n');
  const language = getLanguage(path);

  return (
    <div className="w-[680px] h-auto border-0 border-dolist-lightgray rounded m-auto mt-14 mb-14 bg-dolist-cream">
      <div className="w-5/6 h-full m-auto pt-3 pb-3">
        <div className="pt-4 pb-2">
          <h3 className="text-lg font-bold">{`${title}`}</h3>
        </div>
        <div className="flex flex-row justify-between pt-5 pb-5">
          <div className="text-left">
            <p className="text-xs">{`Type: ${type}`}</p>
          </div>
          <div className="text-right">
            <p className="text-xs">{`Path: ${path}`}</p>
            <p className="text-xs">{`Line: ${lineNumber}`}</p>
          </div>
        </div>
        <div className="pb-3">
          <SyntaxHighlighter
            showLineNumbers
            wrapLongLines
            startingLineNumber={lineNumber}
            language={language}
            style={nightOwl}
          >
            {codeStrings}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
