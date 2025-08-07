import { useState, useEffect } from 'react';

function useModels(){
    const [models, setModels] = useState([])
    const [selectedProduct, setSelectedProduct] = useState(null)

    useEffect(() =>{
    fetch('https://d3pprnqmx0m8l1.cloudfront.net/data/models.json')
      .then(res => res.json())
      .then(data => {
        setModels(data);
        setSelectedProduct(data[0]);
      });
    }, [])

    return {models, selectedProduct, setSelectedProduct}
}

export default useModels