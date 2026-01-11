import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chatbot from '@site/src/components/Chatbot';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
        <Chatbot apiUrl="https://book-1-3piy.onrender.com" />
      </OriginalLayout>
    </>
  );
}