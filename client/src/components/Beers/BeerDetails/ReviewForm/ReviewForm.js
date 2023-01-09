import { Button, Paper, TextField, Typography } from "@material-ui/core";
import React, { useEffect, useState } from "react";
import FileBase from 'react-file-base64';
import { useDispatch, useSelector } from "react-redux";
import { createReview } from "../../../../actions/reviews";

import useStyles from './styles';

const ReviewForm = ({ currentId }) => {
    const [reviewData, setReviewData] = useState({ title: '', message: '' });
    const beer = useSelector((state) => currentId ? (state.beers instanceof Array ? state.beers.find((p) => p._id ===currentId): state.beers.beers.find((p) => p._id ===currentId)) : null);
    const classes = useStyles();
    const dispatch = useDispatch();
    const user = JSON.parse(localStorage.getItem('profile'));

    /* useEffect(() => {
        if(beer) setReviewData(beer);
    }, [beer]) */

    const handleSubmit = (e) => {
        e.preventDefault(); //not to get refresh in the browser

        if(0==1) {
            //dispatch(updateBeer(currentId, { ...reviewData, name: user?.result?.name }));
        } else {
            dispatch(createReview({ ...reviewData, name: user?.result?.name, beer: currentId }));
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
        setReviewData({ title: '', message: '' });
    }

    return (
        <Paper className={classes.paper} elevation={6}>
            <form autoComplete="off" noValidate className={`${classes.root} ${classes.form}`} onSubmit={handleSubmit} >
                <Typography variant="h6">Adding Review</Typography>
                <TextField name="name" variant="outlined" label="Name" fullWidth value={reviewData.title} onChange={(e) => setReviewData({ ...reviewData, title: e.target.value })} />
                <TextField name="description" variant="outlined" label="Description" fullWidth value={reviewData.message} onChange={(e) => setReviewData({ ...reviewData, message: e.target.value })} />
                <Button className={classes.buttonSubmit} variant="contained" color="primary" size="large" type="submit" fullWidth>Submit</Button>
                <Button variant="contained" color="secondary" size="small" onClick={clear} fullWidth>Clear</Button>
            </form>
        </Paper>
    );
}

export default ReviewForm;