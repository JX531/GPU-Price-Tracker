import { apiLink } from "../../../links"

async function delUserAlerts(userEmail, model, price) {
    const url = new URL(apiLink)

    try{
        const res = await fetch(url, {
            method: 'DELETE',
            headers: {"Content-Type": "application/json"},
            body:JSON.stringify({
                "UserEmail": userEmail,
                "Model": model,
            })
        })

        return await res.json()
    } 
    catch(error){
        console.log("API DELETE FAILED: ", error);
        return null
    }
}

export default delUserAlerts