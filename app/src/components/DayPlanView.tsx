/* This example requires Tailwind CSS v2.0+ */
import * as React from 'react';

const DayHeader: React.FC = () => {
  return (
    <header className="relative z-20 flex flex-none items-center justify-between border-b border-gray-200 py-4 px-6">
      <div>
        <h1 className="text-lg font-semibold leading-6 text-gray-900">
          <time dateTime="2022-01-22" className="sm:hidden">
            Jan 22, 2022
          </time>
          <time dateTime="2022-01-22" className="hidden sm:inline">
            January 22, 2022
          </time>
        </h1>
        <p className="mt-1 text-sm text-gray-500">Saturday</p>
      </div>
    </header>
  );
};

interface DayRowProps {
  time: string;
}

const DayRow: React.FC<DayRowProps> = ({ time }: DayRowProps) => {
  return (
    <>
      <div>
        <div className="sticky left-0 -mt-2.5 -ml-14 w-14 pr-2 text-right text-xs leading-5 text-gray-400">{time}</div>
      </div>
      <div />
    </>
  );
};

const DayGrid: React.FC = () => {
  const dayRows = [
    '12AM',
    '1AM',
    '2AM',
    '3AM',
    '4AM',
    '5AM',
    '6AM',
    '7AM',
    '8AM',
    '9AM',
    '10AM',
    '11AM',
    '12PM',
    '1PM',
    '2PM',
    '3PM',
    '4PM',
    '5PM',
    '6PM',
    '7PM',
    '8PM',
    '9PM',
    '10PM',
    '11PM',
  ];

  return (
    <div className="inline-flex flex-auto overflow-scroll bg-white">
      <div className="flex flex-auto flex-col">
        <div className="flex w-full flex-auto">
          <div className="w-14 flex-none bg-white ring-1 ring-gray-100" />
          <div className="grid flex-auto grid-cols-1 grid-rows-1">
            {/* Horizontal lines */}
            <div
              className="col-start-1 col-end-2 row-start-1 grid divide-y divide-gray-100"
              style={{ gridTemplateRows: 'repeat(48, minmax(3.5rem, 1fr))' }}
            >
              <div className="row-end-1 h-7"></div>
              {dayRows.map((day, index) => {
                return <DayRow key={index} time={day} />;
              })}
            </div>
            {/* Horizontal lines */}
          </div>
        </div>
      </div>
    </div>
  );
};

const DayPlanView: React.FC = () => {
  return (
    <div className="flex h-full flex-col">
      <DayHeader />
      <DayGrid />
    </div>
  );
};

export default DayPlanView;
