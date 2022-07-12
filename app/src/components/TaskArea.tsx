import * as React from 'react';

const TaskItem: React.FC = () => {
  return (
    <div className="flex flex-col h-28 m-auto mt-3 mb-3 border border-gray-200 rounded">
      <div>First Row</div>
      <div>Second Row</div>
    </div>
  );
};

const TaskArea: React.FC = () => {
  return (
    <div className="flex flex-col justify-start border border-gray-200 h-full">
      <div className="basis-1/12 p-7 border-b border-gray-200">
        <p>{"Today's focus"}</p>
      </div>
      <div className="basis-11/12 pt-2 pl-5 pr-5 inline-block h-full">
        {/** TASK ITEMS AREA */}
        <div className="w-full h-4/6 mb-2 overflow-scroll">
          <TaskItem />
          <TaskItem />
          <TaskItem />
          <TaskItem />
          <TaskItem />
        </div>
        {/** ADD TASK INPUT AREA */}
        <div className="h-[45px] border border-gray-200">
          <input className="w-full h-full pl-5 m-auto" placeholder="Add a plan to your day..." />
        </div>
      </div>
    </div>
  );
};

export default TaskArea;
