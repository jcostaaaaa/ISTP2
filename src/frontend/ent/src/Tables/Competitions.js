import {useEffect, useState} from "react";
import axios from 'axios';
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



function Competitions() {

    const PAGE_SIZE = 20;
    const [page, setPage] = useState(1);
    const [data, setData] = useState([]);

    const getComps = async () => {
   await axios.get("http://localhost:20001/api/competitions")
    .then((response) => {
        setData(response.data.competitions)
    })
    .catch((error) => {
      console.log('fetch data failed', error);
    });
  };

    useEffect(() => {
       getComps();
    }, []);

    console.log(data)

    const [maxDataSize, setMaxDataSize] = useState(20);


    return (
        <>
            <h1>Competitions</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Player Name</TableCell>
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
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }


        </>
    );
}

export default Competitions;
