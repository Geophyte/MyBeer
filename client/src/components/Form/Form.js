import { Button, Paper, TextField, Typography } from "@material-ui/core";
import React, { useEffect, useState } from "react";
import FileBase from 'react-file-base64';
import { useDispatch, useSelector } from "react-redux";

import useStyles from './styles';
import { createBeer, updateBeer } from "../../actions/beers";

const Form = ({ currentId, setCurrentId }) => {
    const [postData, setPostData] = useState({ title: '', message: '', tags:'', selectedFile: '' });
    const post = useSelector((state) => currentId ? (state.posts instanceof Array ? state.posts.find((p) => p._id ===currentId): state.posts.posts.find((p) => p._id ===currentId)) : null);
    console.log(post)
    const classes = useStyles();
    const dispatch = useDispatch();
    const user = JSON.parse(localStorage.getItem('profile'));

    useEffect(() => {
        if(post) setPostData(post);
    }, [post])

    const handleSubmit = (e) => {
        e.preventDefault(); //not to get refresh in the browser

        if(currentId) {
            dispatch(updateBeer(currentId, { ...postData, name: user?.result?.name }));
        } else {
            dispatch(createBeer({ ...postData, name: user?.result?.name }));
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
        setPostData({ title: '', message: '', tags:'', selectedFile: '' });
    }

    return (
        <Paper className={classes.paper} elevation={6}>
            <form autoComplete="off" noValidate className={`${classes.root} ${classes.form}`} onSubmit={handleSubmit} >
                <Typography variant="h6">{currentId ? 'Editing' : 'Adding'} a Beer</Typography>
                <TextField name="name" variant="outlined" label="Name" fullWidth value={postData.title} onChange={(e) => setPostData({ ...postData, title: e.target.value })} />
                <TextField name="description" variant="outlined" label="Description" fullWidth value={postData.message} onChange={(e) => setPostData({ ...postData, message: e.target.value })} />
                <TextField name="tags" variant="outlined" label="Tags" fullWidth value={postData.tags} onChange={(e) => setPostData({ ...postData, tags: e.target.value.split(",") })} />
                <div className={classes.fileInput}>
                    <FileBase
                        type="file"
                        multiple={false}
                        onDone={({base64}) => setPostData({ ...postData, selectedFile: base64})}
                    />
                </div>
                <Button className={classes.buttonSubmit} variant="contained" color="primary" size="large" type="submit" fullWidth>Submit</Button>
                <Button variant="contained" color="secondary" size="small" onClick={clear} fullWidth>Clear</Button>
            </form>
        </Paper>
    );
}

export default Form;