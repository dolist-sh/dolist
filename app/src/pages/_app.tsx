/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import React from 'react';
import '../styles/globals.css';
import { GlobalContextProvider } from '../contexts/global';
import type { AppProps } from 'next/app';
import Head from 'next/head';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark">
      <Head>
        <script src="/scripts/getTheme.js"></script>
      </Head>
      <GlobalContextProvider>
        <Component {...pageProps} />;
      </GlobalContextProvider>
    </div>
  );
}

export default MyApp;
