import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Results from './Results'
import { Button, Container, Box, CircularProgress } from '@mui/material';

function Search() {
  const [differentLocation, setDifferentLocation] = useState(false);
  const [companies, setCompanies] = useState([]);
  const [rentalData, setRentalData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const handleCompanyChange = (event) => {
    const companyName = event.target.value;
    const isChecked = event.target.checked;

    if (isChecked) {
      setCompanies((prevCompanies) => [...prevCompanies, companyName]);
    } else {
      setCompanies((prevCompanies) =>
        prevCompanies.filter((company) => company !== companyName)
      );
    }
  };
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setRentalData(null);
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    data.companies = companies;

    try {
      const response = await fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      setRentalData(responseData);
      console.log(responseData);

    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: '100px' }}>
      <h3>
        Type in search data
      </h3>
      <p>location can be city name and airport code</p>

      <form onSubmit={handleSubmit} >
        <div>
          <label>
            Pick-up Location:
            <input type="text" name="pickupLocation" required />
          </label>
          <label>
            <input
              type="checkbox"
              name="differentLocation"
              onChange={(e) => setDifferentLocation(e.target.checked)}
            />
            Return at different location
          </label>
          {differentLocation && (
            <label>
              Return Location:
              <input type="text" name="returnLocation" required />
            </label>
          )}
        </div>

        <div>
          <label>
            Age:
            <select name="age" required>
              <option value="18-19">18-19</option>
              <option value="20-24">20-24</option>
              <option value="25+">25+</option>
            </select>
          </label>
        </div>

        <div>
          <label>
            Pick-up Date:
            <input type="date" name="pickupDate" required />
          </label>
          <label>
            Pick-up Time:
            <select name="pickupTime" required>
              {Array.from({ length: 48 }, (_, i) => {
                const hour = Math.floor(i / 2);
                const minute = i % 2 === 0 ? '00' : '30';
                return (
                  <option key={i} value={`${hour}:${minute}`}>
                    {hour}:{minute}
                  </option>
                );
              })}
            </select>
          </label>
        </div>
        <div>
          <label>
            Return Date:
            <input type="date" name="returnDate" required />
          </label>
          <label>
            Return Time:
            <select name="returnTime" required>
              {Array.from({ length: 48 }, (_, i) => {
                const hour = Math.floor(i / 2);
                const minute = i % 2 === 0 ? '00' : '30';
                return (
                  <option key={i} value={`${hour}:${minute}`}>
                    {hour}:{minute}
                  </option>
                );
              })}
            </select>
          </label>
        </div>

        <div>
          <label>
            <input
              type="checkbox"
              value="Hertz"
              onChange={handleCompanyChange}
            />
            Hertz
          </label>
          <label>
            <input
              type="checkbox"
              value="Enterprise"
              onChange={handleCompanyChange}
            />
            Enterprise
          </label>
          <label>
            <input
              type="checkbox"
              value="Avis & Budget"
              onChange={handleCompanyChange}
            />
            Avis & Budget
          </label>
        </div>

        <Button type="submit" variant="contained">Submit</Button>
      </form>

      <Box>
        {rentalData ? (
          <Results data={rentalData}/>
        ) : (
          <Box display="flex" justifyContent="center">
            {
              isLoading ? (
                <CircularProgress />
              ) : (
                <></>
              )
            }

          </Box>
        )}
      </Box>
    </Container>
  );
}

export default Search;
