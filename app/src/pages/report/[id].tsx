import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../../contexts/global';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Layout, MonitoredRepoDetail } from '../../components';
import { useLayoutProps } from '../../hooks';
import { MonitoredRepo } from '../../types';

const ReportPage: NextPage = () => {
  const { push, query } = useRouter();
  const globalContext = useContext(GlobalContext);
  const layoutProps = useLayoutProps(globalContext);
  const [repo, setRepo] = useState<MonitoredRepo>(null);
  const { id } = query;

  useEffect(() => {
    const token = localStorage.getItem('token');
    !token ? push('/signin') : null;
  }, []);

  useEffect(() => {
    setRepo(globalContext.getMonitoredRepo(id as string));
  }, []);

  return (
    <Layout {...layoutProps}>
      {id && repo ? (
        <MonitoredRepoDetail theme={globalContext.theme} githubLogoUri={layoutProps.githubLogoUri} repo={repo} />
      ) : null}
    </Layout>
  );
};

export default ReportPage;
