import { Container, Grid, Grow, Paper, AppBar, TextField, Button } from '@material-ui/core';
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ChipInput from 'material-ui-chip-input';

import Beers from '../Beers/Beers';
import BeerForm from '../Beers/BeerForm/BeerForm';
import { useDispatch } from 'react-redux';
import { getBeersBySearch } from '../../actions/beers';
import { Paginate } from '../Paginate';

import useStyles from './styles';
import BeerDetails from '../Beers/BeerDetails/BeerDetails';

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
    const [categories, setCategories] = useState([]);
    const [isMainPage, setIsMainPage] = useState(true);

    const searchBeer = () => {
        if (search.trim() || categories) {
            dispatch(getBeersBySearch({ search, categories: categories.join(',') }));
            navigate(`/beers/search?searchQuery=${search || 'none'}&categories=${categories.join(',')}`);
        } else {
            navigate('/');
        }
    }

    const handleKeyPress = (e) => {
        if (e.keyCode === 13) {
            searchBeer();
        }
    }

    const handleAdd = (categoryToAdd) => setCategories([...categories, categoryToAdd]);

    const handleDelete = (categoryToDelete) => setCategories(categories.filter((category) => !(category === categoryToDelete)));

    return (
        <div>
            <Grow in>
                <Container maxWidth="xl">
                    {isMainPage ?
                        <Grid container justifyContent="space-between" alignItems="stretch" spacing={3} className={classes.gridContainer}>
                            <Grid item xs={12} sm={6} md={9}>
                                <Beers setCurrentId={setCurrentId} setIsMainPage={setIsMainPage} />
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
                                        value={categories}
                                        onAdd={handleAdd}
                                        onDelete={handleDelete}
                                        label="Search Categories"
                                        variant="outlined"
                                    />
                                    <Button onClick={searchBeer} className={classes.searchButton} variant="contained" color="primary">Search</Button>
                                </AppBar>
                                <BeerForm currentId={currentId} setCurrentId={setCurrentId} />
                                {(!searchQuery && !categories?.length) && (
                                    <Paper elevation={6} className={classes.pagination} >
                                        <Paginate page={page} />
                                    </Paper>
                                )}
                            </Grid>
                        </Grid>
                        : <BeerDetails currentId={currentId} />
                    }
                </Container>
            </Grow>
        </div>
    )
}

export default Home