import { useState, useEffect } from 'react';

function useModelData(selectedProduct) {
    const [selectedProductData, setSelectedProductData] = useState([])

    //fetch model data once each time selected product is changed
    useEffect(() => {
        fetch(`https://d3pprnqmx0m8l1.cloudfront.net/data/dailyAverages/${selectedProduct}_dailyAverage.json`)
        .then(res => res.json())
        //convert from object to array for easier data presentation
        .then(objectData => {
            const dataArray = Object.keys(objectData).map(date => ({
            Date: date,
            AvgPrice: objectData[date].AvgPrice, 
            NumListings: objectData[date].NumListings
            }));
            setSelectedProductData(dataArray);
        });
    }, [selectedProduct])

    return {selectedProductData}
}

export default useModelData