import React, { useEffect } from 'react';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { getAuthCode } from '../api';

const ProcessAuthPage: NextPage = () => {
  const { query, push } = useRouter();

  useEffect(() => {
    const redirect = query.redirect;
    const tempCode = query.code;

    if (redirect && tempCode) {
      getAuthCode(tempCode as string).then((token) => {
        if (token) {
          localStorage.setItem('token', token);
          push('/', '/main');
        } else {
          push('/signin');
        }
      });
    }
  }, [query]);

  return (
    <div className="flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="flex flex-row justify-center align-middle">
        <p>{'Process Auth'}</p>
      </div>
    </div>
  );
};

export default ProcessAuthPage;
