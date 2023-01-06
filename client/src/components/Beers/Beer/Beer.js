import React from "react";
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import DeleteIcon from '@mui/icons-material/Delete';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import ThumbUpAltOutlined from '@material-ui/icons/ThumbUpAltOutlined';
import moment from 'moment';
import useStyles from './styles';
import { Button, Card, CardActions, CardContent, CardMedia, Typography } from "@mui/material";
import { useDispatch } from 'react-redux';

import { deleteBeer, likeBeer } from "../../../actions/beers";
import { Link } from "@material-ui/core";


const Beer = ({ beer, setCurrentId }) => {
    const classes = useStyles();
    const dispatch = useDispatch();
    const user = JSON.parse(localStorage.getItem('profile'));

    const Likes = () => {
        if (beer?.likes.length > 0) {
            return beer.likes.find((like) => like === (user?.result?.googleId || user?.result?._id))
                ? (
                    <><ThumbUpAltIcon fontSize="small" />&nbsp;{beer.likes.length > 2 ? `You and ${beer.likes.length - 1} others` : `${beer.likes.length} like${beer.likes.length > 1 ? 's' : ''}`}</>
                ) : (
                    <><ThumbUpAltOutlined fontSize="small" />&nbsp;{beer.likes.length} {beer.likes.length === 1 ? 'Like' : 'Likes'}</>
                );
        }

        return <><ThumbUpAltOutlined fontSize="small" />&nbsp;Like</>;
    };

    return (
        <Card className={classes.card} raised elevation={6}>
            <CardMedia className={classes.media} image={beer.selectedFile} title={beer.title} component='img' />
            <div className={classes.overlay}>
                <Typography variant="h6" style={{ color: 'black' }}>{beer.name}</Typography>
                <Typography variant="body2" style={{ color: 'black' }}>{moment(beer.createdAt).fromNow()}</Typography>
            </div>
            {(user?.result?.googleId === beer?.creator || user?.result?._id === beer?.creator) && (
                <div className={classes.overlay2}>
                    <Button onClick={() => setCurrentId(beer._id)} style={{ color: 'primary' }} size="small">
                        <MoreHorizIcon fontSize="default" />
                    </Button>
                </div>
            )}
            <div className={classes.details}>
                <Typography variant="body2" color="textSecondary">{beer.categories.map((category) => `#${category} `)}</Typography>
            </div>

            <Typography className={classes.title}  gutterBottom>
                <Link variant="h5" underline="none" color="inherit" onClick={()=>{}} tabIndex={0} component="button">
                    {beer.title}
                </Link>
            </Typography>

            <CardContent>
                <Typography variant="h5" color="textSecondary" component="p">{beer.message}</Typography>
            </CardContent>
            <CardActions className={classes.cardActions}>
                <Button size="small" color="primary" disabled={!user?.result} onClick={() => dispatch(likeBeer(beer._id))}>
                    <Likes />
                </Button>
                {(user?.result?.googleId === beer?.creator || user?.result?._id === beer?.creator) && (
                    <Button size="small" color="secondary" onClick={() => dispatch(deleteBeer(beer._id))}>
                        <DeleteIcon fontSize="small" /> Delete
                    </Button>
                )}
            </CardActions>
        </Card>
    );
}

export default Beer;