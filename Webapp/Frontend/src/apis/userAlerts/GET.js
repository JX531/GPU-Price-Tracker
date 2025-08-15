import { apiLink } from "../../../links"
import tryCachedAlerts from "../../helpers/tryCachedAlerts"
async function getUserAlerts(userEmail) {

    let cache = tryCachedAlerts(userEmail)
    if (cache){
        console.log("Loaded userAlerts from local storage cache: ", cache)
        return cache
    }


    const url = new URL(apiLink)
    url.searchParams.append("UserEmail",userEmail)
    try{
        const res = await fetch(url, {
            method: 'GET',
            mode: 'cors', // Explicitly request CORS
            headers: {"Content-Type": "application/json"}
        })

        console.log("Loaded userAlerts from API fetch instead")
        return res.json()
    } 

    catch(error){
        console.log("API GET FAILED: ", error)
        return null
    }
}

export default getUserAlerts