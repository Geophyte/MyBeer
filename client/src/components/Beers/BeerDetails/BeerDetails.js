import { Grid } from '@material-ui/core'
import React, { useState } from 'react'
import CommentForm from './CommentForm/CommentForm'
import useStyles from './styles';

const BeerDetails = ({ currentId, setCurrentId }) => {
    const classes = useStyles();

    return (
        <Grid container justifyContent="space-between" alignItems="stretch" spacing={3} className={classes.gridContainer}>
            <Grid item xs={12} sm={6} md={9}>
                {/* <Beers setCurrentId={setCurrentId} /> */}
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
                <CommentForm currentId={currentId} setCurrentId={setCurrentId} />
            </Grid>
        </Grid>
    )
}

export default BeerDetails