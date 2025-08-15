import { useState, useEffect } from 'react';
import { cloudfrontLink } from "../../links";
function useModelCheapest(selectedProduct) {
    const [selectedProductCheapest, setSelectedProductCheapest] = useState([])

    if (!selectedProduct){
        console.log("useModelCheapest missing selectedProduct")
        return {selectedProductCheapest}
    }

    //fetch model data once each time selected product is changed
    useEffect(() => {
        fetch(`${cloudfrontLink}/data/dailyCheapest/${selectedProduct}_dailyCheapest.json`)
        .then(res => res.json())
        //convert from object to array for easier data presentation
        .then(objectData => {
            const dataArray = Object.keys(objectData.Listings).map(link => ({
                Link: link,
                Price: objectData.Listings[link].Price, 
                Model: objectData.Listings[link].Model,
                VRAM: objectData.Listings[link].VRAM,
                Brand: objectData.Listings[link].Brand,
                Title: objectData.Listings[link].Title,
                ImageLink: objectData.Listings[link].ImageLink
            }));
            setSelectedProductCheapest(dataArray);
        });
    }, [selectedProduct])

    return {selectedProductCheapest}
}

export default useModelCheapest