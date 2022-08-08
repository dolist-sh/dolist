import React, { useContext, useState, useEffect, CSSProperties } from 'react';
import { GlobalContext } from '../contexts/global';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { getAuthCode } from '../api';
import PanmanLoader from 'react-spinners/PacmanLoader';

const Spinner: React.FC = () => {
  const [spinnerColor, setSpinnerColor] = useState(null);

  const globalcontext = useContext(GlobalContext);
  const override: CSSProperties = {
    display: 'block',
    margin: '0 auto',
  };

  useEffect(() => {
    if (globalcontext.theme === 'dark') {
      setSpinnerColor('#E8E7E0');
    }
    if (globalcontext.theme === 'light') {
      setSpinnerColor('#1E2B3D');
    }
  }, [globalcontext.theme]);

  return (
    <>
      <PanmanLoader loading={true} size={30} color={spinnerColor} cssOverride={override} />
    </>
  );
};

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
    <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark flex flex-col justify-center w-11/12 h-screen m-auto">
      <div className="w-full h-20 content-center">
        <Spinner />
      </div>
      <p className="w-full text-center pl-6 text-dolist-darkblue dark:text-dolist-cream font-std">
        {'busy processing, hang tight..'}
      </p>
    </div>
  );
};

export default ProcessAuthPage;
