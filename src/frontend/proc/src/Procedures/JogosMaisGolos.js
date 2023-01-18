import React, {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";
import axios from "axios";



function JogosMaisGolos() {

    const [data,setData] = useState(null)

     const getJogos = async () => {
   await axios.get("http://localhost:20004/api/getgolosjogo")
    .then((response) => {
        setData(response.data.procJogos)
    })
    .catch((error) => {
      console.log('fetch data failed', error);
    });
  };

    useEffect(() => {
       getJogos();
    }, []);


    return (
        <>
            <h1>Jogos</h1>

                        <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">Golos Marcados</TableCell>
                            <TableCell>Vitorias</TableCell>
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

export default JogosMaisGolos;