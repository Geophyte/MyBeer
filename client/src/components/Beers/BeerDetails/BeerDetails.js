import { Box, Divider, Grid, Link, List, ListItem, Paper, Typography } from '@material-ui/core'
import React, { useEffect } from 'react'
import moment from 'moment';
import { useDispatch, useSelector } from 'react-redux';
import ReviewForm from './ReviewForm/ReviewForm'
import useStyles from './styles';
import { createReview, getReviews } from '../../../actions/reviews';
import ListItemContent from '@mui/joy/ListItemContent';

const BeerDetails = ({ currentId }) => {
    const dispatch = useDispatch();
    const classes = useStyles();
    const beer = useSelector((state) => currentId ? (state.beers instanceof Array ? state.beers.find((p) => p._id === currentId) : state.beers.beers.find((p) => p._id === currentId)) : null);
    const reviews = useSelector((state) => state.beers.reviews.filter((p) => p.beer == beer._id));

    useEffect(() => {
        dispatch(getReviews());
    }, []);

    function Reviews(reviews) {
        return (
            <center>
                {reviews.map(e => (
                    <Paper style={{ padding: '20px', borderRadius: '15px' }} elevation={6} fullWidth>
                        <ListItem>
                            <ListItemContent>
                                <Typography>{e.title}</Typography>
                                <Typography level="body2" noWrap>
                                    {e.message}
                                </Typography>
                            </ListItemContent>
                        </ListItem>
                    </Paper>
                ))}
            </center>
        )
    }

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

            <Box sx={{ width: 320 }}>
                <List
                    aria-labelledby="ellipsis-list-demo"
                    sx={{ '--List-decorator-size': '56px' }}
                >
                    {[0, 1, 2, 3].forEach((e) => (<div>q</div>))}
                    {Reviews(reviews)}




                </List>
            </Box>
        </Grid>
    )
}

export default BeerDetails