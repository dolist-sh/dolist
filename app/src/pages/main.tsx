import React, { useEffect } from 'react';
import type { NextPage } from 'next';
import { getUser } from '../api';

const AppMainPage: NextPage = () => {
  useEffect(() => {
    const token = localStorage.getItem('token');

    getUser(token).then((data) => {
      // TODO: Do something with the data
      console.log(data);
    });
  });

  return (
    <div className="flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="flex flex-row justify-center align-middle">
        <p>{'App Main Page'}</p>
      </div>
    </div>
  );
};

export default AppMainPage;
