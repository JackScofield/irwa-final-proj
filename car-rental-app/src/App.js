// src/App.js

import React, { useState } from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './components/Home';
import Search from './components/Search';
import './App.css';

function App() {
  return (
    
    <React.StrictMode>
      <BrowserRouter>
        <Routes>
            <Route index path="/" element = {<Home/>} />
            <Route path="/search" element = {<Search/>}/>
        </Routes>

      </BrowserRouter>
    </React.StrictMode>
  );
}

export default App;
