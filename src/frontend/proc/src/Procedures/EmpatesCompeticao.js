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
import axios from "axios";



function EmpatesCompeticao() {

    const [data,setData] = useState(null)
    const [input,setInput] = useState(null)

     const getDraws = async () => {
   await axios.get("http://localhost:20004/api/getdrawscomp/" + input )
    .then((response) => {
        setData(response.data.draws)
    })
    .catch((error) => {
      console.log('fetch data failed', error);
    });
  };

    return (
        <>
            <h1>Empates Competicao</h1>
                    <TextField
                        label="Competição"
                        onChange ={(e) => setInput(e.target.value)}
                        variant="outlined"
                    />

                    <Button variant="contained" color="primary" onClick={() => getDraws()}>
                    Procurar por Competição
                    </Button>

                        <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">Empates</TableCell>
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
                                        <TableCell component="td" scope="row">
                                            {row[1]}
                                        </TableCell>
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

export default EmpatesCompeticao;