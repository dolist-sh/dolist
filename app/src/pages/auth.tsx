import React from 'react';
import type { NextPage } from 'next';

const AuthPage: NextPage = () => {
  return (
    <div className="flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="flex flex-row justify-center align-middle">
        <button className=" px-3 py-2 border-2 text-sm border-dolist-darkblue rounded" type="button">
          {'Auth with Github'}
        </button>
      </div>
    </div>
  );
};

export default AuthPage;
