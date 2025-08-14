import { useState, useEffect } from 'react';
import { cloudfrontLink } from "../../links";
function useModels(){
    const [models, setModels] = useState([])
    const [selectedProduct, setSelectedProduct] = useState(null)

    useEffect(() =>{
    fetch(`${cloudfrontLink}/data/models.json`)
      .then(res => res.json())
      .then(data => {
        setModels(data);
        setSelectedProduct(data[0]);
      });
    }, [])

    return {models, selectedProduct, setSelectedProduct}
}

export default useModels