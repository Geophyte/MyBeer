import { CircularProgress, Grid } from "@material-ui/core";
import React from "react";
import { useSelector } from 'react-redux';

import Beer from "./Beer/Beer";

import useStyles from './styles';

const Beers = ({ setCurrentId }) => {
    const { beers, isLoading } = useSelector((state) => state.beers);
    const classes = useStyles();

    if(!beers?.length && !isLoading) return 'No beers';

    return (
        isLoading ? <CircularProgress /> : (
            <Grid className={classes.container} container alignItems="stretch" spacing={3}>
                {beers.map((beer) => (
                        <Grid key={beer._id} item xs={12} sm={12} md={12} lg={12}>
                            <Beer beer={beer} setCurrentId={setCurrentId} />
                        </Grid>
                    ))}
            </Grid>
        )
    );
}

export default Beers;