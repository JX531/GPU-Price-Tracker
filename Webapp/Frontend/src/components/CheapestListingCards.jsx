import '../App.css'

function CheapestListingCards({selectedProductCheapest}){
    if (!selectedProductCheapest){
        return <div>Loading...</div>
    }

    return(
        selectedProductCheapest.slice(0, 3).map((product, index) => (
            <div key={index}>
                <div className="Card">
                    <img src={product.ImageLink}></img>
                    <h2>SGD ${product.Price}</h2>
                    <p>{product.Brand} {product.Model} {product.VRAM}GB</p>
                    <a href={product.Link} target="_blank" rel="noopener noreferrer">{product.Title}</a>
                </div>
            </div>
        ))
    )
}

export default CheapestListingCards
