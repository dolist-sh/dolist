/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import React from 'react';
import App from 'next/app';
import { createGlobalStyle } from 'styled-components';
import reset from 'styled-reset';

const GlobalStyle = createGlobalStyle`
  ${reset}

   /* clears the 'X' from Internet Explorer */
   input.hide-clear[type=search]::-ms-clear,
    input.hide-clear[type=search]::-ms-reveal {
      display: none;
      width: 0;
      height: 0; 
    }
    /* clears the 'X' from Chrome */
    input.hide-clear[type="search"]::-webkit-search-decoration,
    input.hide-clear[type="search"]::-webkit-search-cancel-button,
    input.hide-clear[type="search"]::-webkit-search-results-button,
    input.hide-clear[type="search"]::-webkit-search-results-decoration {
        display: none; 
        -webkit-appearance:none;
    };
    /* add other global styles here */
    input[type="search"]::-webkit-search-decoration,
    input[type="search"]::-webkit-search-cancel-button,
    input[type="search"]::-webkit-search-results-button,
    input[type="search"]::-webkit-search-results-decoration {
      -webkit-appearance:none;
    };

    html {
        position: relative;
        min-height: 100%;
    };
    
    html, body {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        width: 100%;
        max-width: 100%;
        height: auto!important;
        overflow-x: hidden;
    };
    
    body {
        font-family: 'Roboto', sans-serif;
    };
`;

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props;

    return (
      <>
        <GlobalStyle />
        <Component {...pageProps} />
      </>
    );
  }
}

export default MyApp;
