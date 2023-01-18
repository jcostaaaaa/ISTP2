import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";
import L from 'leaflet';
import axios from 'axios';

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());
    const [visibleGeo, setVisibleGeo] = useState([]);

    /**
     * Setup the event to update the bounds automatically
     */
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, []);

    /* Updates the data for the current bounds */

    useEffect(() => {
        if (!bounds) return;

        const visibleGeo = geom.filter(marker => {
            const point = L.latLng(marker.geometry.coordinates[0], marker.geometry.coordinates[1]);
            return bounds.contains(point);
        });
        setVisibleGeo(visibleGeo);
    }, [bounds, geom]);

    const  asyncFetch = async () => {
    await axios.get("http://localhost:20002/api/markers")
        .then((response) => {
            setGeom(response.data)
        })
        .catch((error) => {
        console.log('fetch data failed', error);
        });
    };
        useEffect(() => {
        asyncFetch();
        }, []);

    console.log(geom);

    return (
        <LayerGroup>
            {
                visibleGeo.map(games => <ObjectMarker key={games.properties.id} games={games}/>)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
