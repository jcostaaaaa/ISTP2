import React, {useEffect, useState} from "react";
import {
    Box, Button,
    CircularProgress, Container, FormControl, InputLabel, MenuItem,
    Pagination,
    Paper, Select,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow, TextField
} from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DesktopDatePicker } from "@mui/x-date-pickers/DesktopDatePicker";
import dayjs from "dayjs";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import axios from "axios";



function JogosPor() {

    const [data,setData] = useState(null)
    const [input,setInput] = useState(null)
    const [dateBegin, setDateBegin] = useState(dayjs);

    const handleChange = (newValue) => {
    setDateBegin(newValue);
    };

     const getGamesPor = async () => {
   await axios.get("http://localhost:20004/api/gamesPor/" + input )
    .then((response) => {
        setData(response.data.gamePor)
    })
    .catch((error) => {
      console.log('fetch data failed', error);
    });
  };

    return (
        <>
            <h1>Jogos Competicao</h1>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DesktopDatePicker
                          label="Date"
                          inputFormat="MM/DD/YYYY"
                          value={dateBegin}
                          onChange={handleChange}
                          renderInput={(params) => <TextField {...params} />}
                        />
                    </LocalizationProvider>

                    <Button variant="contained" color="primary" onClick={() => getGamesPor()}>
                    Procurar por Data
                    </Button>

                        <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">Golos Casa</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Golos Fora</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Equipa Casa</TableCell>
                            <TableCell component="th" width={"1px"} align="center">Equipa Fora</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                             data ?
                                data.map((row) => (
                                    <TableRow
                                        key={row[0]}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{row[0]}</TableCell>
                                        <TableCell component="td" scope="row" align="center">
                                            {row[1]}
                                        </TableCell>
                                        <TableCell component="td" align="center">{row[2]}</TableCell>
                                        <TableCell component="td" align="center">{row[3]}</TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
        </>
    );
}

export default JogosPor;