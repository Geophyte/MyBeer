import React, { useEffect } from 'react';
import { Pagination, PaginationItem } from '@material-ui/lab';
import { Link } from 'react-router-dom';

import useStyles from './styles';
import { useDispatch, useSelector } from 'react-redux';

import { getBeers } from '../actions/beers';

export const Paginate = ({ page }) => {
    const { numberOfPages } = useSelector((state) => state.beers);
    const classes = useStyles();
    const dispatch = useDispatch();

    useEffect(() => {
        if(page) dispatch(getBeers(page));
    }, [page]);

    return (
        <Pagination
            classes={{ ul: classes.ul }}
            count={numberOfPages}
            page={Number(page) || 1}
            variant="outlined"
            color="primary"
            renderItem={(item) => (
                <PaginationItem {...item} component={Link} to={`/beers?page=${item.page}`} />
            )}
        />
    )
}