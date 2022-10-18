import React, { useEffect } from 'react';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Layout } from '../components';
import { useLayoutProps } from '../hooks';

const ReportPage: NextPage = () => {
  const layoutProps = useLayoutProps();
  const { push } = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    !token ? push('/signin') : null;
  }, []);

  return (
    <Layout {...layoutProps}>
      <div>{'Hello world!'}</div>
    </Layout>
  );
};

export default ReportPage;
