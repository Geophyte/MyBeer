import { Button, Paper, TextField, Typography } from "@material-ui/core";
import React, { useEffect, useState } from "react";
import FileBase from 'react-file-base64';
import { useDispatch, useSelector } from "react-redux";

import useStyles from './styles';
import { createBeer, updateBeer } from "../../actions/beers";

const Form = ({ currentId, setCurrentId }) => {
    const [beerData, setBeerData] = useState({ title: '', message: '', categories:'', selectedFile: '' });
    const beer = useSelector((state) => currentId ? (state.beers instanceof Array ? state.beers.find((p) => p._id ===currentId): state.beers.beers.find((p) => p._id ===currentId)) : null);
    console.log(beer)
    const classes = useStyles();
    const dispatch = useDispatch();
    const user = JSON.parse(localStorage.getItem('profile'));

    useEffect(() => {
        if(beer) setBeerData(beer);
    }, [beer])

    const handleSubmit = (e) => {
        e.preventDefault(); //not to get refresh in the browser

        if(currentId) {
            dispatch(updateBeer(currentId, { ...beerData, name: user?.result?.name }));
        } else {
            dispatch(createBeer({ ...beerData, name: user?.result?.name }));
        }
        clear();
    }

    if(!user?.result?.name) {
        return(
            <Paper className={classes.paper} align="center">
                Plesae sign in to add your own beers comment and like other beers!
            </Paper>
        )
    }

    const clear = () => {
        setCurrentId(null);
        setBeerData({ title: '', message: '', categories:'', selectedFile: '' });
    }

    return (
        <Paper className={classes.paper} elevation={6}>
            <form autoComplete="off" noValidate className={`${classes.root} ${classes.form}`} onSubmit={handleSubmit} >
                <Typography variant="h6">{currentId ? 'Editing' : 'Adding'} a Beer</Typography>
                <TextField name="name" variant="outlined" label="Name" fullWidth value={beerData.title} onChange={(e) => setBeerData({ ...beerData, title: e.target.value })} />
                <TextField name="description" variant="outlined" label="Description" fullWidth value={beerData.message} onChange={(e) => setBeerData({ ...beerData, message: e.target.value })} />
                <TextField name="categories" variant="outlined" label="Categories" fullWidth value={beerData.categories} onChange={(e) => setBeerData({ ...beerData, categories: e.target.value.split(",") })} />
                <div className={classes.fileInput}>
                    <FileBase
                        type="file"
                        multiple={false}
                        onDone={({base64}) => setBeerData({ ...beerData, selectedFile: base64})}
                    />
                </div>
                <Button className={classes.buttonSubmit} variant="contained" color="primary" size="large" type="submit" fullWidth>Submit</Button>
                <Button variant="contained" color="secondary" size="small" onClick={clear} fullWidth>Clear</Button>
            </form>
        </Paper>
    );
}

export default Form;