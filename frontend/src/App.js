import React from 'react';
import { ConfigProvider } from 'antd';
import trTR from 'antd/locale/tr_TR';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <ConfigProvider locale={trTR}>
      <Dashboard />
    </ConfigProvider>
  );
}

export default App;