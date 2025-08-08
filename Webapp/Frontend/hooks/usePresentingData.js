import { useState, useEffect } from 'react';

function usePresentingData(selectedProductData){
    const [timeSpan, setTimeSpan] = useState(-365)
    const [presentingData, setPresentingData] = useState([])

    //slice the selected model data whenever timespan is changed or selected data changes
    useEffect(()=>{
        setPresentingData(selectedProductData.slice(timeSpan))
    }, [timeSpan, selectedProductData])

    return {presentingData, timeSpan, setTimeSpan}
}

export default usePresentingData