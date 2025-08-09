import '../App.css'

function Card({data}){
    if (!data){
        return <div>Loading...</div>
    }

    return(
        <div className="Card">
            <img src={data.ImageLink}></img>
            <h2>SGD ${data.Price}</h2>
            <p>{data.Brand} {data.Model} {data.VRAM}GB</p>
            <a href={data.Link} target="_blank" rel="noopener noreferrer">{data.Title}</a>
        </div>
    )
}

export default Card