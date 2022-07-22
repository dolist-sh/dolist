import React, { useEffect } from 'react';
import type { NextPage } from 'next';

const AppMainPage: NextPage = () => {
  useEffect(() => {
    const token = localStorage.getItem('token');

    const getUser = async (token: string) => {
      const response = await fetch(`http://localhost:8000/user`, {
        method: 'GET',
        mode: 'cors',
        headers: { Authorization: `token ${token}` },
      });
      return response.json();
    };

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
