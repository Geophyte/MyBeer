import { CircularProgress, Grid } from "@material-ui/core";
import React from "react";
import { useSelector } from 'react-redux';

import Beer from "./Beer/Beer";

import useStyles from './styles';

const Beers = ({ setCurrentId }) => {
    const { posts, isLoading } = useSelector((state) => state.posts);
    const classes = useStyles();

    if(!posts?.length && !isLoading) return 'No posts';

    return (
        isLoading ? <CircularProgress /> : (
            <Grid className={classes.container} container alignItems="stretch" spacing={3}>
                {posts.map((post) => (
                        <Grid key={post._id} item xs={12} sm={12} md={6} lg={3}>
                            <Beer post={post} setCurrentId={setCurrentId} />
                        </Grid>
                    ))}
            </Grid>
        )
    );
}

export default Beers;