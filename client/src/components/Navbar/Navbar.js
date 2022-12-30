import { AppBar, Avatar, Button, Toolbar, Typography } from '@material-ui/core'
import { Link, useLocation, useNavigate } from 'react-router-dom';
import React, { useEffect, useState } from 'react'
import useStyles from './styles';
import decode from 'jwt-decode';
import hintally from '../../images/hintally.png'
import { useDispatch } from 'react-redux';

const Navbar = () => {
    const classes = useStyles();
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('profile')));
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const location = useLocation();

    const logout = () => {
        dispatch({ type: 'LOGOUT' });
        navigate('/');
        setUser(null);
    };

    useEffect(() => {
        const token = user?.token;

        if(token){
            const decodedToken = decode(token);

            //logging out after amount of time inactivity
            if(decodedToken.exp * 1000 < new Date().getTime()) logout();
        }

        setUser(JSON.parse(localStorage.getItem('profile')))
    }, [location]);

    return (
        <div>
            <AppBar className={classes.appBar} position="static" color="inherit">
                <div className={classes.brandContainer}>
                    <Typography component={Link} to="/" className={classes.heading} variant="h2" align="center">XDXD</Typography>
                    <img className={classes.image} src={hintally} alt="memories" height="60" />
                </div>
                <Toolbar className={classes.toolbar}>
                    {user ? (
                        <div className={classes.profile}>
                            <Avatar className={classes.purple} alt={user.result.name} src={user.result.imageUrl}>{user.result.name.charAt(0)}</Avatar>
                            <Typography className={classes.userName} variant="h6">{user.result.name}</Typography>
                            <Button variant="contained" className={classes.logout} color="secondary" onClick={logout}>Logout</Button>
                        </div>
                    ) : (
                        <Button component={Link} to="/auth" variant="contained" color="primary">Sign in</Button>
                    )}
                </Toolbar>
            </AppBar>
        </div>
    )
}

export default Navbar