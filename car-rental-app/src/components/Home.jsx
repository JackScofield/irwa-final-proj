import { Link, Navigate } from "react-router-dom";
import { Button, Container, Typography } from '@mui/material';
export default function Home(props) {
    const nextPage = '/search'
    return (
        <div>
            <Container maxWidth="sm">

                <h2>Rental Car Prices Comparison Bots</h2>
                <p>Simple web bot for you to compare price differences between different popular car rental companies</p>
                <p>Good tool before you travel and rent a car at the airport</p>
                <Button variant="contained" component={Link} to={nextPage}>Start Search</Button>
            </Container>

        </div>
    );
}