import React, { useEffect, useState, useContext } from 'react';
import { GlobalContext } from '../../contexts/global';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { Layout, MonitoredRepoDetail } from '../../components';
import { getMonitoredRepo } from '../../api';
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
    if (globalContext.monitoredRepos.length === 0 && id) {
      const token = localStorage.getItem('token');

      getMonitoredRepo(token, id as string).then((result) => {
        if (!result) {
          //TODO: gracefully redirect to error page and log it
          throw new Error('Failed to load the data');
        }
        setRepo(result);
      });
    } else if (globalContext.monitoredRepos.length !== 0 && id) {
      const mrepo = globalContext.getMonitoredRepo(id as string);
      if (!mrepo) {
        //TODO: gracefully redirect to error page and log it
        throw new Error('Failed to load the data');
      }
      setRepo(mrepo);
    }
  }, [id]);

  return (
    <Layout {...layoutProps}>
      {id && repo ? (
        <MonitoredRepoDetail theme={globalContext.theme} githubLogoUri={layoutProps.githubLogoUri} repo={repo} />
      ) : null}
    </Layout>
  );
};

export default ReportPage;
