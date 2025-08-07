import { useState, useEffect } from 'react';

function useModelCheapest(selectedProduct) {
    const [selectedProductCheapest, setSelectedProductCheapest] = useState([])

    //fetch model data once each time selected product is changed
    useEffect(() => {
        fetch(`https://d3pprnqmx0m8l1.cloudfront.net/data/dailyCheapest/${selectedProduct}_cheapestDaily.json`)
        .then(res => res.json())
        //convert from object to array for easier data presentation
        .then(objectData => {
            const dataArray = Object.keys(objectData.Listings).map(link => ({
                Link: link,
                Price: objectData[link].Price, 
                Model: objectData[link].Model,
                VRAM: objectData[link].VRAM,
                Brand: objectData[link].Brand,
                Title: objectData[link].Title
            }));
            setSelectedProductCheapest(dataArray);
        });
    }, [selectedProduct])

    return {selectedProductCheapest}
}

export default useModelCheapest