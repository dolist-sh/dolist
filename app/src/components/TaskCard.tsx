import * as React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { nightOwl } from 'react-syntax-highlighter/dist/cjs/styles/prism';

const TaskCard: React.FC = () => {
  return (
    <div className="w-[560px] h-auto border-0 border-dolist-lightgray rounded m-auto mt-14 mb-14 bg-dolist-cream">
      <div className="w-5/6 h-full m-auto pt-3 pb-3">
        <div className="pt-4 pb-2">
          <h3 className="text-lg font-bold">Add typing to createPerson method</h3>
        </div>
        <div className="flex flex-row justify-between pt-5 pb-5">
          <div className="text-left">
            <p className="text-xs">Type: TODO</p>
          </div>
          <div className="text-right">
            <p className="text-xs">Path: /src/input/example.py</p>
            <p className="text-xs">Line: 18</p>
          </div>
        </div>
        <div className="pb-3">
          <SyntaxHighlighter
            showLineNumbers
            wrapLongLines
            startingLineNumber={18}
            language="javascript"
            style={nightOwl}
          >{`// TODO: comment`}</SyntaxHighlighter>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
