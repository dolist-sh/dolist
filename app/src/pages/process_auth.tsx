import React, { useContext, useState, useEffect } from 'react';
import { GlobalContext } from '../contexts/global';
import { Loader } from '../components';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { getAuthCode } from '../api';

const ProcessAuthPage: NextPage = () => {
  const { query, push } = useRouter();
  const [loaderColor, setLoaderColor] = useState(null);
  const globalcontext = useContext(GlobalContext);

  useEffect(() => {
    const redirect = query.redirect;
    const tempCode = query.code;

    if (redirect && tempCode) {
      getAuthCode(tempCode as string).then((token) => {
        if (token) {
          localStorage.setItem('token', token);
          push('/', '/dashboard');
        } else {
          push('/signin');
        }
      });
    }
  }, [query]);

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setLoaderColor('#E8E7E0');
    }
    if (globalcontext.theme === 'light') {
      setLoaderColor('#1E2B3D');
    }
  }, [globalcontext.theme]);

  return (
    <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="w-full h-20 content-center">
        <Loader loaderColor={loaderColor} />
      </div>
      <p className="w-full text-center pl-6 text-dolist-darkblue dark:text-dolist-cream font-std">
        {'busy processing, hang tight..'}
      </p>
    </div>
  );
};

export default ProcessAuthPage;
