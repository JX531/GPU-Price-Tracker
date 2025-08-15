import { useState, useEffect } from 'react';
import { cloudfrontLink } from "../../links";
function useModelData(selectedProduct) {
    const [selectedProductData, setSelectedProductData] = useState([])

    //fetch model data once each time selected product is changed
    useEffect(() => {

        if (!selectedProduct){
            console.log("useModelData missing selectedProduct")
            return
        }

        fetch(`${cloudfrontLink}/data/dailyAverages/${selectedProduct}_dailyAverage.json`)
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