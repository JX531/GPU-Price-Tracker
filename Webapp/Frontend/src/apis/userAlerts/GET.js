import { apiLink } from "../../../links"

async function getUserAlerts(userEmail) {
    const url = new URL(apiLink)
    url.searchParams.append("UserEmail",userEmail)
    try{
        const res = await fetch(url, {
            method: 'GET',
            mode: 'cors', // Explicitly request CORS
            headers: {"Content-Type": "application/json"}
        })
        
        return await res.json()
    } 
    catch(error){
        console.log("API GET FAILED: ", error);
        return null
    }
}

export default getUserAlerts