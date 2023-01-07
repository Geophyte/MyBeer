import { Divider, Grid, Link, Paper, Typography } from '@material-ui/core'
import React from 'react'
import moment from 'moment';
import { useSelector } from 'react-redux';
import ReviewForm from './ReviewForm/ReviewForm'
import useStyles from './styles';

const BeerDetails = ({ currentId }) => {
    const classes = useStyles();
    const beer = useSelector((state) => currentId ? (state.beers instanceof Array ? state.beers.find((p) => p._id === currentId) : state.beers.beers.find((p) => p._id === currentId)) : null);
    console.log(beer)

    return (
        <Grid container justifyContent="space-between" alignItems="stretch" spacing={3} className={classes.gridContainer}>
            <Grid item xs={12} sm={6} md={9}>
                <Paper style={{ padding: '20px', borderRadius: '15px' }} elevation={6}>
                    <div className={classes.card}>
                        <div className={classes.section}>
                            <Typography variant="h3" component="h2">{beer.title}</Typography>
                            <Typography gutterBottom variant="h6" color="textSecondary" component="h2">{beer.categories.map((tag) => `#${tag} `)}</Typography>
                            <Typography gutterBottom variant="body1" component="p">{beer.message}</Typography>
                            <Typography variant="h6">Created by: {beer.name}</Typography>
                            <Typography variant="body1">{moment(beer.createdAt).fromNow()}</Typography>
                            <Divider style={{ margin: '20px 0' }} />
                        </div>
                        <div className={classes.imageSection}>
                            <img className={classes.media} src={beer.selectedFile || 'https://user-images.githubusercontent.com/194400/49531010-48dad180-f8b1-11e8-8d89-1e61320e1d82.png'} alt={beer.title} />
                        </div>
                    </div>
                </Paper>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
                <ReviewForm currentId={currentId} />
            </Grid>
        </Grid>
    )
}

export default BeerDetails