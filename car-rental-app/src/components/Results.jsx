import React from 'react';
import { Link, List, ListItem, ListItemText, Typography } from '@mui/material';
const Results = ({ data }) => {
  console.log('Received data:', data);
  return (
    <div>
      {data.map((item, index) => (
        <div>
          <h3>{data[index].company} Car Rentals</h3>
          {
            data[index].company === 'Hertz' ? <Link href="https://www.hertz.com/rentacar/reservation/">Hertz website</Link> : null
          }
          {
            data[index].company === 'Enterprise' ? <Link href="https://www.enterprise.com/en/home.html">Enterprise website</Link> : null
          }
          {
            data[index].company === 'Avis & Budget' ? <Link href="https://www.avis.com/en/home">Avis website</Link> : null
          }

          <List>
            {data[index].results.map((car, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={<Typography variant="h6">{car.model}</Typography>}
                  secondary={
                    <Typography variant="body2" color="textSecondary">
                      {car.price_total} USD
                    </Typography>
                  }
                />
              </ListItem>
            ))}
          </List>

        </div>
      ))}
    </div>
  );
};

export default Results;
