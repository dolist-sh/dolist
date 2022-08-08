/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import React from 'react';
import '../styles/globals.css';
import { GlobalContextProvider } from '../contexts/global';
import type { AppProps } from 'next/app';
import Head from 'next/head';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet" />
        <script src="/scripts/getTheme.js"></script>
      </Head>
      <div className="bg-dolist-bg-light dark:bg-dolist-bg-dark">
        <GlobalContextProvider>
          <Component {...pageProps} />;
        </GlobalContextProvider>
      </div>
    </>
  );
}

export default MyApp;
