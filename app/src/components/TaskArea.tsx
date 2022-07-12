import * as React from 'react';

const TaskItem: React.FC = () => {
  return (
    <div className="flex flex-col w-5/6 h-28 m-auto mt-3 mb-3 border border-gray-200 rounded">
      <div>First Row</div>
      <div>Second Row</div>
    </div>
  );
};

const TaskArea: React.FC = () => {
  return (
    <div className="flex flex-col justify-start h-full border border-gray-200">
      <div className="basis-1/12 p-7 border-b border-gray-200">
        <p>{"Today's focus"}</p>
      </div>
      <div className="basis-11/12 pt-7 pl-5 pr-5 border border-gray-200 rounded">
        <div className="flex flex-col justify-start h-full">
          {/** TASK ITEMS AREA */}
          <div className="basis-11/12 max-h-96 border border-gray-200 overflow-scroll">
            <TaskItem />
            <TaskItem />
            <TaskItem />
            <TaskItem />
            <TaskItem />
          </div>
          {/** ADD TASK INPUT AREA */}
          <div className="basis-1/12 border border-gray-200">
            <input className="w-full h-full pl-5 m-auto" placeholder="Add a plan to your day..." />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskArea;
