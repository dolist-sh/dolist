import * as React from 'react';

const TaskCard: React.FC = () => {
  return (
    <div className="w-[560px] h-auto border-0 border-dolist-lightgray rounded m-auto mt-5 mb-5 bg-dolist-cream">
      <div className="w-11/12 h-full m-auto pt-3 pb-3">
        <div className="pt-2 pb-2">
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
        <div>Code block here</div>
      </div>
    </div>
  );
};

export default TaskCard;
