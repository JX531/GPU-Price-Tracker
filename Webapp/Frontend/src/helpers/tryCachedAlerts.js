function tryCachedAlerts(userEmail){
    if (!userEmail){
        return 
    }

    const cacheExists = localStorage.getItem('userAlerts')
    if (cacheExists){
        try{
            let cachedAlerts = JSON.parse(cacheExists)
            if ((Date.now() - cachedAlerts.TimeStamp) < (5 * 60 * 1000) && cachedAlerts.Email === userEmail){
                return cachedAlerts.Data
            }
        }
        catch(e){
            console.log("Loading cachedAlerts failed: ", {e})
            return null
        }
    }
    return null
}

export default tryCachedAlerts