import { CircularProgress, Grid } from "@material-ui/core";
import React from "react";
import { useSelector } from 'react-redux';

import BeerItem from "./BeerItem/BeerItem";

import useStyles from './styles';

const Beers = ({ setCurrentId, setIsMainPage }) => {
    const { beers, isLoading } = useSelector((state) => state.beers);
    const classes = useStyles();

    if(!beers?.length && !isLoading) return 'No beers';

    return (
        isLoading ? <CircularProgress /> : (
            <Grid className={classes.container} container alignItems="stretch" spacing={3}>
                {beers.map((beer) => (
                        <Grid key={beer._id} item xs={12} sm={12} md={12} lg={12}>
                            <BeerItem beer={beer} setCurrentId={setCurrentId} setIsMainPage={setIsMainPage} />
                        </Grid>
                    ))}
            </Grid>
        )
    );
}

export default Beers;