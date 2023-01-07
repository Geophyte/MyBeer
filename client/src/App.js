import React from 'react';
import { Container } from '@material-ui/core';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';
import Home from './components/Home/Home';
import Auth from './components/Auth/Auth';

const App = () => {
    const user = JSON.parse(localStorage.getItem('profile'));

    return (
        <BrowserRouter>
            <Container maxwidth="xl">
                <Navbar />
                <Routes>
                    <Route path="/" exact element={<Navigate to="/beers" replace={true} />} />
                    <Route path="/beers" exact element={<Home />} />
                    <Route path="/beers/search" exact element={<Home />} />
                    <Route path="/auth" exact element={!user ? <Auth/> : <Navigate to="/beers" />} />
                </Routes>
            </Container>
        </BrowserRouter>
    )
};

export default App;