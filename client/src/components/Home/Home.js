import { Container, Grid, Grow, Paper, AppBar, TextField, Button } from '@material-ui/core';
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ChipInput from 'material-ui-chip-input';

import Beers from '../Beers/Beers';
import Form from '../Form/Form';
import { useDispatch } from 'react-redux';
import { getBeers, getBeersBySearch } from '../../actions/beers';
import { Paginate } from '../Paginate';
import { ClassNames } from '@emotion/react';

import useStyles from './styles';

function useQuery() {
    return new URLSearchParams(useLocation().search);
}

const Home = () => {
    const [currentId, setCurrentId] = useState(0);
    const dispatch = useDispatch();
    const query = useQuery();
    const navigate = useNavigate();
    const page = query.get('page') || 1;
    const searchQuery = query.get('searchQuery');
    const classes = useStyles();
    const [search, setSearch] = useState('');
    const [tags, setTags] = useState([]);

    const searchBeer = () => {
        if (search.trim() || tags) {
            dispatch(getBeersBySearch({ search, tags: tags.join(',') }));
            navigate(`/posts/search?searchQuery=${search || 'none'}&tags=${tags.join(',')}`);
        } else {
            navigate('/');
        }
    }

    const handleKeyPress = (e) => {
        if (e.keyCode === 13) {
            searchBeer();
        }
    }

    const handleAdd = (tagToAdd) => setTags([...tags, tagToAdd]);

    const handleDelete = (tagToDelete) => setTags(tags.filter((tag) => !(tag === tagToDelete)));

    return (
        <div>
            <Grow in>
                <Container maxWidth="xl">
                    <Grid container justifyContent="space-between" alignItems="stretch" spacing={3} className={classes.gridContainer}>
                        <Grid item xs={12} sm={6} md={9}>
                            <Beers setCurrentId={setCurrentId} />
                        </Grid>

                        <Grid item xs={12} sm={6} md={3}>
                            <AppBar className={classes.appBarSearch} position="static" color="inherit">
                                <TextField
                                    name="search"
                                    variant="outlined"
                                    label="Search Beers"
                                    onKeyPress={handleKeyPress}
                                    fullWidth
                                    value={search}
                                    onChange={(e) => { setSearch(e.target.value) }}
                                />
                                <ChipInput
                                    styles={{ margin: '10px 0' }}
                                    value={tags}
                                    onAdd={handleAdd}
                                    onDelete={handleDelete}
                                    label="Search Tags"
                                    variant="outlined"
                                />
                                <Button onClick={searchBeer} className={classes.searchButton} variant="contained" color="primary">Search</Button>
                            </AppBar>
                            <Form currentId={currentId} setCurrentId={setCurrentId} />
                            {(!searchQuery && !tags?.length) && (
                                <Paper elevation={6} className={classes.pagination} >
                                    <Paginate page={page} />
                                </Paper>
                            )}
                        </Grid>
                    </Grid>
                </Container>
            </Grow>
        </div>
    )
}

export default Home