import { apiLink } from "../../../links"

async function putUserAlerts(userEmail, model, price) {
    const url = new URL(apiLink)
    try{
        const res = await fetch(url, {
            method: 'PUT',
            headers: {"Content-Type": "application/json"},
            body:JSON.stringify({
                "UserEmail": userEmail,
                "Model": model,
                "Price": price
            })
        })

        return await res.json()
    } 
    catch(error){
        console.log("API PUT FAILED: ", error);
        return null
    }
}

export default putUserAlerts